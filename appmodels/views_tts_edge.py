from rest_framework.views import APIView
from django.http import HttpResponse
import tempfile
import asyncio
import os 
import edge_tts 
from yanbao_api import settings, utils_yml
log = settings.log 
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r")


async def tts(voice, rate, volume, text, file):
    tts_obj = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    async for message in tts_obj.stream():
        if message["type"] == "audio":
            file.write(message["data"])


class BigmodelsTtsEdgeView(APIView):
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="edge.mp3"'
        voice = request.data.get("voice", config_tts.get("edge", {}).get("voice", "zh-TW-HsiaoChenNeural"))
        rate = request.data.get("rate", config_tts.get("edge", {}).get("rate", "+10%"))
        volume = request.data.get("volume", config_tts.get("edge", {}).get("volume", "+0%"))
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        file = tempfile.TemporaryFile()
        try:
            asyncio.run(tts(voice, rate, volume, text, file))
        except Exception as e:
            log.warning(f'tts edge error: {e}')
            response.status_code = 400
            return response
        file.seek(0)
        data = file.read()
        file.close()
        if len(data) > 0:
            response.write(data)
            return response
        else:
            log.warning(f'tts edge file: 文件为空')
            response.status_code = 400
            return response
