from rest_framework.views import APIView
from django.http import HttpResponse
import os
import azure.cognitiveservices.speech as speechsdk
from yanbao_api import settings, utils, utils_yml
log = settings.log 
config_model = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'model.yml'), mode="r")
config_tts = utils_yml.operate(file=os.path.join(settings.DIR_DATA, 'configs', 'tts.yml'), mode="r")
# pip install azure-cognitiveservices-speech


class BigmodelsTtsAzureView(APIView):
    def post(self, request):
        response = HttpResponse(content_type='audio/mp3')
        response['Content-Disposition'] = 'attachment; filename="azure.mp3"'
        subscription = config_model.get("azure", {}).get("for_tts", {}).get("subscription")
        region = config_model.get("azure", {}).get("for_tts", {}).get("region") 
        voice = request.data.get("voice", config_tts.get("azure", {}).get("voice", "zh-CN-XiaochenNeural"))
        text = request.data.get("text", None)
        if text is None:
            response.status_code = 400
            return response
        log.debug(f'subscription:{subscription}, region:{region} voice:{voice}')
        file = os.path.join(settings.DIR_TMP, f'tts_azure_{utils.get_strftime(fmt="%Y%m%d%H%M%S%f")}.mp3')
        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=subscription, region=region
            )
            speech_config.speech_synthesis_voice_name = voice
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3
            )
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config
            )
            result = speech_synthesizer.speak_text_async(text).get()
            stream = speechsdk.AudioDataStream(result)
            stream.save_to_wav_file(file)
        except Exception as e:
            log.warning(f'tts azure error: {e}')
            response.status_code = 400
            return response
        if os.path.exists(file):
            with open(file, 'rb') as f:
                data = f.read()
            response.write(data)
            return response
        else:
            log.warning(f'tts azure error: 文件为生成{file}')
            response.status_code = 400
            return response