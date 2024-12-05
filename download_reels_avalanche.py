import instaloader
import requests
import os
import time

contador_videos = 0

def extrair_nome_por_emoticon(caption):
    global contador_videos

    # 1. Verifica se há o emoticon 📽️ na legenda
    if "📽️" in caption:
        partes = caption.split("📽️", 1)
        if len(partes) > 1:
            return partes[1].strip().split()[0].replace('/', '-')

    # 2. Se não houver o emoticon, verificar a presença de um @
    if "@" in caption:
        partes_at = caption.split('@')  # Dividir a legenda com base no símbolo @

        # Itera sobre cada @ encontrado
        for i, parte in enumerate(partes_at[1:], start=1):  # Começa a partir do segundo elemento
            nome_usuario = parte.split()[0]  # Pega o nome logo após o @

            if nome_usuario == "aprendizagem_avancada":
                # Se o primeiro @ for @aprendizagem_avancada, continuar procurando o próximo @
                if i < len(partes_at) - 1:
                    proximo_nome_usuario = partes_at[i + 1].split()[0]
                    return f"@{proximo_nome_usuario}"
            else:
                # Se não for @aprendizagem_avancada, retornar o @ encontrado
                return f"@{nome_usuario}"

    # 3. Caso não encontre nenhum @ ou 📽️, retorna 'Vídeo X'
    contador_videos += 1  # Incrementa o contador global
    return f"#foco #resiliência #motivação #estudar #concursopublico #concurso #estudos #concurseiro #{contador_videos}"

def baixar_reels_com_taxa_curtida_alta(username):
    L = instaloader.Instaloader()

    try:
        perfil = instaloader.Profile.from_username(L.context, username)

        if not os.path.exists(r'C:\Users\Matheus\Desktop\reels'):
            os.makedirs(r'C:\Users\Matheus\Desktop\reels')

        for post in perfil.get_posts():
            if post.is_video and post.typename == 'GraphVideo':
                time.sleep(1)
                #visualizacoes = post.video_view_count
                #print(f"visualizacoes: {visualizacoes}")
                curtidas = post.likes
                if curtidas > 5000:
                    print(f"\n-----------------------\n")
                    print(f"curtidas: {curtidas}")
                    legenda = post.caption or ""
                    print(f"legenda: {legenda}")
                    nome_video = extrair_nome_por_emoticon(legenda)
                    print(f"nome_video: {nome_video}")

                    if nome_video:
                        print(f"Baixando: {nome_video}")
                        video_url = post.video_url

                        resposta = requests.get(video_url)
                        if resposta.status_code == 200:
                            caminho_arquivo = f"C:/Users/Matheus/Desktop/reels/{nome_video}.mp4"
                            with open(caminho_arquivo, 'wb') as f:
                                f.write(resposta.content)
                            print(f"Salvo em: {caminho_arquivo}")
                        else:
                            print(f"Erro ao baixar {nome_video}")
                    else:
                        print(f"Legenda sem o emoticon 🎥: {post.shortcode}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
baixar_reels_com_taxa_curtida_alta("aprendizagem_avancada")
