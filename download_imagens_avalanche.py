#baixa publicações de imagens no instagram

import instaloader
import requests
import os
import time
import random

contador_videos = 0

# Lista de hashtags para ser usada aleatoriamente
hashtags = ["#foco", "#resiliência", "#motivação", "#estudar",
            "#concursopublico", "#concurso", "#estudos", "#concurseiro",
            "#dicas", "#nopainnogain", "#disciplina", "#estudaqueavidamuda",
            "#provas", "#borapassar", "#compartilha", "#avalanche"]


def extrair_nome_por_emoticon(caption):

    if "@" in caption:
        partes_at = caption.split('@')  # Dividir a legenda com base no símbolo @

        # Itera sobre cada @ encontrado
        for i, parte in enumerate(partes_at[1:]):
            nome_usuario = parte.split()[0]  # Pega o nome logo após o @

            return f"@{nome_usuario}"

    # Seleciona 4 hashtags de forma aleatória
    hashtags_aleatorias = random.sample(hashtags, 4)

    return f"{' '.join(hashtags_aleatorias)}"


def baixar_imagens_com_compartilhamentos_altos(username):
    global contador_videos
    L = instaloader.Instaloader()

    try:
        perfil = instaloader.Profile.from_username(L.context, username)

        # Cria a pasta 'publis' se não existir
        if not os.path.exists(r'C:\Users\Matheus\Desktop\publis_dicas'):
            os.makedirs(r'C:\Users\Matheus\Desktop\publis_dicas')

        for post in perfil.get_posts():
            # Verifica se o post é uma imagem
            if post.typename == 'GraphImage':
                time.sleep(1)

                likes = post.likes
                if likes > 5000:  # Verifica se há mais de 5 mil compartilhamentos
                    print(f"\n-----------------------\n")
                    print(f"likes: {likes}")
                    legenda = post.caption or ""
                    print(f"legenda: {legenda}")
                    nome_video = extrair_nome_por_emoticon(legenda)

                    if nome_video:
                        print(f"Baixando: {nome_video}")
                        imagem_url = post.url

                        resposta = requests.get(imagem_url)
                        if resposta.status_code == 200:
                            contador_videos += 1
                            caminho_arquivo = f"C:/Users/Matheus/Desktop/publis_dicas/{contador_videos}_{nome_video}.jpg"
                            with open(caminho_arquivo, 'wb') as f:
                                f.write(resposta.content)
                            print(f"Salvo em: {caminho_arquivo}")
                        else:
                            print(f"Erro ao baixar {nome_video}")
                    else:
                        print(f"Legenda sem informações relevantes: {nome_video}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
baixar_imagens_com_compartilhamentos_altos("pequenasdicasde")