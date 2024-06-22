from rest_framework.views import APIView
from django.http import HttpResponse
import tempfile
import os 
from openai import OpenAI
from yanbao_api import settings, utils_yml
log = settings.log 
config_model = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'model.yml'), mode="r")
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r")
client= OpenAI(
    api_key=config_model.get("chatopenai", {}).get("for_tts", {}).get("api_key"),
    base_url=config_model.get("chatopenai", {}).get("for_tts", {}).get("base_url")
)


class BigmodelsTtsChatopenaiView(APIView):
    """openai tts"""
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="chatopenai.mp3"'
        voice = request.data.get("voice", config_tts.get("chatopenai", {}).get("voice", "onyx"))
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        response_tts = client.audio.speech.create(
            model=config_model.get("chatopenai", {}).get("for_tts", {}).get("model", "tts-1"), 
            voice=voice, 
            input=text
        )
        file = tempfile.TemporaryFile()
        file.write(response_tts.read())
        file.seek(0)
        data = file.read()
        file.close()
        if len(data) > 0:
            response.write(data)
            return response
        else:
            response.status_code = 500
            return response
