from rest_framework.views import APIView
from django.http import HttpResponse
import requests
import os 
from yanbao_api import settings, utils_yml
log = settings.log 
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r").get("openai", {})


class BigmodelsTtsChatopenaiView(APIView):
    """openai tts"""
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="openai.mp3"'
        voice = request.data.get("voice", config_tts.get("voice"))
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        tts_response = requests.post(
            url=config_tts.get("url"), 
            headers=config_tts.get("headers"), 
            params=config_tts.get("params"), 
            json={
                "model": config_tts.get("model"),
                "input": text,
                "voice": voice
            }
        )
        if tts_response.status_code != 200:
            response.status_code = 400
            return response
        if len(tts_response.content) == 0:
            response.status_code = 400
            return response
        response.write(tts_response.content)
        return response
