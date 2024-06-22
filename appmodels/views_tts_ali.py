from rest_framework.views import APIView
from django.http import HttpResponse
import tempfile
import os
import nls
from nls.token import getToken
# 安装nls /opt/alibabacloud-nls-python-sdk-1.0.0
# D:\ProjectPython\ali\alibabacloud-nls-python-sdk-1.0.0\alibabacloud-nls-python-sdk-1.0.0
# conda activate 
# python -m pip install -r requirements.txt
# python -m pip install .
from yanbao_api import settings, utils, utils_yml
log = settings.log 
config_model = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'model.yml'), mode="r")
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r")


def on_data(data, *args):
    file = args[0]
    file.write(data)

def tts(token, appkey, url, voice, sample_rate, volume, speech_rate, pitch_rate, text, file):
    tts_obj = nls.NlsSpeechSynthesizer(
        url=url,
        token=token,
        appkey=appkey,
        on_data=on_data,
        callback_args=[file]
    )
    tts_obj.start(
        text=text, 
        voice=voice, 
        aformat='mp3', 
        sample_rate=sample_rate,
        volume=volume,
        speech_rate=speech_rate,
        pitch_rate=pitch_rate,
        ex={"enable_ptts": True}
    )

class BigmodelsTtsAliView(APIView):
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="ali.mp3"'
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        try:
            token = getToken(
                akid=config_model.get("ali", {}).get("for_tts", {}).get("akid"),
                aksecret=config_model.get("ali", {}).get("for_tts", {}).get("aksecret")
            )
        except Exception as e:
            log.warning(f'tts ali error: token {e}')
            response.status_code = 400
            return response
        file = tempfile.TemporaryFile()
        try:
            tts(
                token=token,
                appkey=config_model.get("ali", {}).get("for_tts", {}).get("appkey"),
                url=config_model.get("ali", {}).get("for_tts", {}).get("url"), 
                voice=request.data.get("voice", config_tts.get("ali", {}).get("voice", "xiaoyun")),
                sample_rate=request.data.get("sample_rate", config_tts.get("ali", {}).get("sample_rate", 16000)),
                volume=request.data.get("volume", config_tts.get("ali", {}).get("volume", 50)),
                speech_rate=request.data.get("speech_rate", config_tts.get("ali", {}).get("speech_rate", 10)),
                pitch_rate=request.data.get("pitch_rate", config_tts.get("ali", {}).get("pitch_rate", 0)),
                text=text, 
                file=file
            )
        except Exception as e:
            log.warning(f'tts ali error: tts {e}')
            response.status_code = 400
            return response
        file.seek(0)
        data = file.read()
        file.close()
        if len(data) > 0:
            response.write(data)
            return response
        else:
            log.warning(f'tts ali error: 文件为生成{file}')
            response.status_code = 400
            return response
