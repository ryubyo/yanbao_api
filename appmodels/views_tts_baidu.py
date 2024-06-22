from rest_framework.views import APIView
from django.http import HttpResponse
import os
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from urllib.parse import quote_plus
import tempfile
from yanbao_api import settings, utils_yml
log = settings.log 
config_model = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'model.yml'), mode="r")
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r")


def get_token(client_id, client_secret, scope='audio_tts_post',  timeout=5):
    url = 'http://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = urlencode(params).encode('utf-8')
    req = Request(url, data)
    f = urlopen(req, timeout=timeout)
    fr = f.read().decode()
    resp = json.loads(fr)
    if 'access_token' in resp.keys() and 'scope' in resp.keys():
        if scope in resp['scope'].split(' '):
            return resp['access_token']
    log.warning(f'tts baidu error: token {resp}')
    return None


def tts(token, text, file, per=0, spd=5, pit=5, vol=5, aue=3, cuid='123456PYTHON'):
    url = 'http://tsn.baidu.com/text2audio'
    params = {
        'tok': token, 
        'tex': quote_plus(str(text)), 
        'per': per, 
        'spd': spd, 
        'pit': pit, 
        'vol': vol, 
        'aue': aue, 
        'cuid': cuid,
        'lan': 'zh', 
        'ctp': 1
    }  # lan ctp 固定参数
    data = urlencode(params)
    req = Request(url, data.encode('utf-8'))
    f = urlopen(req)
    headers = dict((name.lower(), value) for name, value in f.headers.items())
    if 'content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0:
        log.warning(f'tts baidu error: tts {headers}')
    else:
        file.write(f.read())


class BigmodelsTtsBaiduView(APIView):
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="baidu.mp3"'
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        try:
            token = get_token(
                client_id=config_model.get("erniebotchat", {}).get("for_tts", {}).get("client_id"),
                client_secret=config_model.get("erniebotchat", {}).get("for_tts", {}).get("client_secret"),
                scope=config_model.get("erniebotchat", {}).get("for_tts", {}).get("scope"),
                timeout=config_model.get("erniebotchat", {}).get("for_tts", {}).get("timeout")
            )
        except Exception as e:
            log.warning(f'tts baidu error: response {e}')
            response.status_code = 400
            return response
        if token is None:
            log.warning(f'tts baidu error: token is None')
            response.status_code = 400
            return response
        file = tempfile.TemporaryFile()
        try:
            tts(
                token=token,
                text=text,
                file=file,
                per=int(request.data.get("voice", config_tts.get("baidu", {}).get("per", "0"))),
                spd=request.data.get("spd", config_tts.get("baidu", {}).get("spd", 5)),
                pit=request.data.get("pit", config_tts.get("baidu", {}).get("pit", 5)),
                vol=request.data.get("vol", config_tts.get("baidu", {}).get("vol", 5)),
                aue=request.data.get("aue", config_tts.get("baidu", {}).get("aue", 3)),
                cuid=request.data.get("cuid", config_tts.get("baidu", {}).get("cuid", '123456PYTHON'))
            )
        except Exception as e:
            log.warning(f'tts baidu error: tts {e}')
            response.status_code = 400
            return response
        file.seek(0)
        data = file.read()
        file.close()
        if len(data) > 0:
            response.write(data)
            return response
        else:
            log.warning(f'tts azure error: 文件为生成{file}')
            response.status_code = 400
            return response
