import pyktok as pyk
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import os

# Caminho do arquivo de texto que contém as URLs
file_path = r'XXX'

# Pasta de destino para mover os vídeos
output_folder = r'XXX'

# Ler o arquivo e carregar as URLs na variável videos_videos
with open(file_path, 'r') as file:
    videos_videos = [line.strip() for line in file if line.strip()]


# Loop para processar os vídeos
for video in videos_videos:
    tt_json = pyk.alt_get_videos_json(video)
    data_slot = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']

    try:
        nickname = data_slot['author']['uniqueId']
    except Exception:
        try:
            nickname = data_slot['author']['nickname']
        except Exception:
            nickname = ''

    # Baixar o vídeo do videos
    pyk.save_videos(video, True, output_folder, 'videos-' + nickname)

    print(f"Vídeo {
          nickname} baixado, concatenado com o logo e o arquivo original foi deletado com sucesso!")
