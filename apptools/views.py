from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, StreamingHttpResponse
from pydub import AudioSegment
from pydub.silence import split_on_silence
import zipfile
import os 
from yanbao_api import settings, utils
log = settings.log 


# Create your views here.
def split_audio(upload_file, min_silence_len, silence_thresh, keep_silence, seek_step):
    original_file = os.path.join(settings.DIR_TMP, f'split_{utils.get_strftime(fmt="%Y%m%d%H%M%S%f")}.mp3')
    with open(original_file, "wb") as fw:
        fw.write(upload_file.read())
    sound = AudioSegment.from_mp3(original_file)
    chunks = split_on_silence(
        sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence, seek_step=seek_step
    )
    file_name, file_extension = os.path.splitext(os.path.basename(original_file))
    splitfiles = []
    for i, chunk in enumerate(chunks):
        splitfile = os.path.join(settings.DIR_TMP, f'{file_name}_{i}{file_extension}')
        chunk.export(splitfile)
        splitfiles.append(splitfile)
    print(splitfiles)
    zip_file = os.path.join(settings.DIR_TMP, f'{file_name}.zip')
    zip_file_obj = zipfile.ZipFile(file=zip_file, mode="w", compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    for splitfile in splitfiles:
        zip_file_obj.write(filename=splitfile, arcname=os.path.basename(splitfile))
    if not os.path.exists(zip_file):
        raise Exception('zip文件不存在')
    return zip_file


class FfmpegAudioSplitView(APIView):
    def post(self, request):
        response = HttpResponse(content_type="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=splits.zip'
        min_silence_len = request.data.get("min_silence_len", 100)
        silence_thresh = request.data.get("silence_thresh", -64)
        keep_silence = request.data.get("keep_silence", 100)
        seek_step = request.data.get("seek_step", 1)
        upload_file = request.FILES.get("file", None)
        if upload_file is None:
            return Response(data="未上传文件", status=400)
        try:
            zip_file = split_audio(
                upload_file=upload_file,
                min_silence_len=int(min_silence_len),
                silence_thresh=int(silence_thresh),
                keep_silence=int(keep_silence),
                seek_step=int(seek_step)
            )
        except Exception as e:
            return Response(data=f"拆分音频出错{e}", status=400)
        def iterator(file, chunk_size=512):
            with open(file, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        response = StreamingHttpResponse(iterator(zip_file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename={file}'.format(file=os.path.basename(zip_file))
        return response

