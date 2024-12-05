import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from itertools import chain, zip_longest
import re

texto_inicial = "Siga a nossa página para se manter focado nos estudos, além de pegar sempre uma dica ou outra que farão a diferença até a sua aprovação." + \
    "\n\n" + "Comece a estudar ainda hoje e esteja preparado para os inúmeros editais que ainda estão por abrir. Foque no seu futuro." + "\n\n"

# Lista contendo 16 hashtags relacionadas a concursos públicos
hashtags_concursos = [
    "#concurseirolutador", "#concursopublico", "#concurseiros", "#concursando", "#focadonosestudos",
    "#rotinadeestudos", "#vidadeconcurseiro", "#concurseirosunidos", "#resiliência", "#estudoupassou",
    "#foco", "#nopainnogain", "#estudaqueavidamuda", "#estudos", "#objetivos", "#disciplina", "#questões",
    "#vencernavida", "#faculdade", "#ensino", "#formação", "#ler", "#aprendizado", "#rirpranaochorar"
]


# Função para iniciar o driver
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")
    chrome_options.add_argument("--disable-notifications")

    # Coloque o caminho para o ChromeDriver
    service = Service(
        'C:/Users/Matheus/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe')

    # Use o service para iniciar o ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Minimize a janela após inicializar o driver
    driver.set_window_position(-10000, 0)

    return driver


# Função para login no Instagram
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(10)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)


# Função para publicar no Instagram
def publicar(driver, caminho_arquivo, hora_atual):
    # Botão de upload
    upload_btn = driver.find_element(
        By.XPATH, '//*[@aria-label="Nova publicação"]')
    upload_btn.click()
    time.sleep(3)

    upload_btn = driver.find_element(By.XPATH, '//*[@aria-label="Publicar"]')
    upload_btn.click()
    time.sleep(2)

    # Upload de arquivo
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(caminho_arquivo)
    time.sleep(4)  # Aguarde o vídeo carregar

    try:
        link = driver.find_element(
            By.XPATH, "//button[contains(text(), 'OK')]")
        link.click()
        time.sleep(3)
    except Exception as e:
        print("O botão 'OK' não foi encontrado ou não pôde ser clicado.")

    next_btn = driver.find_element(
        By.XPATH, '//*[@aria-label="Selecionar corte"]')
    next_btn.click()
    time.sleep(2)

    next_btn = driver.find_element(
        By.XPATH, "//span[contains(text(), 'Original')]")
    next_btn.click()
    time.sleep(3)

    next_btn = driver.find_element(
        By.XPATH, "//div[contains(text(), 'Avançar')]")
    next_btn.click()
    time.sleep(2)

    next_btn = driver.find_element(
        By.XPATH, "//div[contains(text(), 'Avançar')]")
    next_btn.click()
    time.sleep(3)

    # Adiciona a legenda (nome do arquivo sem a extensão)
    if caminho_arquivo.endswith('.mp4'):
        legenda = os.path.splitext(os.path.basename(caminho_arquivo))[
            0].replace("tiktok-", "")
        legenda = texto_inicial + " ".join(random.sample(hashtags_concursos, 8)) + \
            "\n\nVia " + legenda + "\nPara remoção, entre em contato via direct."

    elif caminho_arquivo.endswith('.jpg'):
        legenda = extrair_nome_imagem(caminho_arquivo)
        legenda = " ".join(random.sample(hashtags_concursos, 8))

    else:
        legenda = ''

    caption_input = driver.find_element(By.XPATH, '//*[@role="textbox"]')
    caption_input.send_keys(legenda)

    # Compartilhar
    share_btn = driver.find_element(
        By.XPATH, "//div[contains(text(), 'Compartilhar')]")
    share_btn.click()

    time.sleep(30)
    print(f"Publicado {datetime.now()}")


# Função para renomear o arquivo
def renomear_arquivo(caminho_arquivo):
    caminho_novo = os.path.join(os.path.dirname(
        caminho_arquivo), "PUBLICADO_" + os.path.basename(caminho_arquivo))
    os.rename(caminho_arquivo, caminho_novo)
    print(f"Arquivo renomeado para: {caminho_novo}")
    return caminho_novo


def extrair_nome_imagem(nome_arquivo):
    # Usar expressão regular para encontrar o padrão
    padrao = r'@([^\.]+)'  # Captura tudo após @ até o ponto
    match = re.search(padrao, nome_arquivo)

    if match:
        return match.group(1)  # Retorna o grupo que foi capturado
    else:
        return ''  # Retorna em branco se não encontrar


# Função principal para automatizar o processo
def automatizar_publicacoes(folder_videos, folder_dicas, folder_motivacao, username, password):
    # Obter todos os arquivos de vídeo da pasta
    arquivos_videos = [f for f in os.listdir(folder_videos) if f.endswith(
        '.mp4') and not f.startswith("PUBLICADO_")]

    # Obter todos os arquivos de imagem da pasta dicas
    arquivos_dicas = [f for f in os.listdir(folder_dicas) if f.endswith(
        '.jpg') and not f.startswith("PUBLICADO_")]

    # Ordenar arquivos pela data de modificação (mais recentes primeiro)
    arquivos_dicas.sort(key=lambda x: os.path.getmtime(
        os.path.join(folder_dicas, x)), reverse=True)

   # Obter todos os arquivos de imagem da pasta motivacao
    arquivos_motivacao = [f for f in os.listdir(folder_motivacao) if f.endswith(
        '.jpg') and not f.startswith("PUBLICADO_")]

    # Combinar os arquivos (vídeos, dicas e motivacao separados para controle)
    arquivos = {"videos": arquivos_videos,
                "dicas": arquivos_dicas, "motivacao": arquivos_motivacao}

    print(arquivos)

    while arquivos["videos"] or arquivos["dicas"] or arquivos["motivacao"]:
        hora_atual = datetime.now().hour

        if hora_atual > 23 or hora_atual <= 5:
            # Se estiver entre 23h e 6h, aguardar até o próximo ciclo (1h)
            print("Está fora do horário permitido (23h-5h).")
            intervalo_segundos = random.randint(3600, 7200)
            print(f"Aguardando por {
                  intervalo_segundos // 60} minutos antes de tentar postar o próximo arquivo.\n")
            time.sleep(intervalo_segundos)

        elif ((6 <= hora_atual <= 8) or (18 <= hora_atual <= 20)):
            # Publicar vídeos
            if arquivos["videos"]:
                arquivo = arquivos["videos"].pop(0)
                caminho_arquivo = os.path.join(folder_videos, arquivo)

                driver = iniciar_driver()
                login_instagram(driver, username, password)
                publicar(driver, caminho_arquivo, hora_atual)
                driver.quit()

                # Renomear o arquivo
                renomear_arquivo(caminho_arquivo)

                intervalo_segundos = random.randint(
                    10800, 14400)  # 3 a 4 horas
                print(f"Aguardando por {
                      intervalo_segundos // 60} minutos antes de postar o próximo arquivo.\n")
                time.sleep(intervalo_segundos)
            else:
                print("Nenhum vídeo restante para publicar entre 6h e 8h.")
                time.sleep(3600)  # Aguarda 1 hora

        elif ((9 <= hora_atual <= 11) or (15 <= hora_atual <= 17)):
            # Publicar motivacao
            if arquivos["motivacao"]:
                arquivo = arquivos["motivacao"].pop(0)
                caminho_arquivo = os.path.join(folder_motivacao, arquivo)

                driver = iniciar_driver()
                login_instagram(driver, username, password)
                publicar(driver, caminho_arquivo, hora_atual)
                driver.quit()

                # Renomear o arquivo
                renomear_arquivo(caminho_arquivo)

                intervalo_segundos = random.randint(
                    3600, 7200)  # 3 a 4 horas
                print(f"Aguardando por {
                      intervalo_segundos // 60} minutos antes de postar o próximo arquivo.\n")
                time.sleep(intervalo_segundos)
            else:
                print("Nenhuma imagem restante para publicar entre 9h e 22h.")
                time.sleep(3600)  # Aguarda 1 hora

        elif ((12 <= hora_atual <= 14) or (21 <= hora_atual <= 23)):
            # Publicar dicas
            if arquivos["dicas"]:
                arquivo = arquivos["dicas"].pop(0)
                caminho_arquivo = os.path.join(folder_dicas, arquivo)

                driver = iniciar_driver()
                login_instagram(driver, username, password)
                publicar(driver, caminho_arquivo, hora_atual)
                driver.quit()

                # Renomear o arquivo
                renomear_arquivo(caminho_arquivo)

                intervalo_segundos = random.randint(
                    3600, 7200)  # 3 a 4 horas
                print(f"Aguardando por {
                      intervalo_segundos // 60} minutos antes de postar o próximo arquivo.\n")
                time.sleep(intervalo_segundos)
            else:
                print("Nenhuma imagem restante para publicar entre 9h e 22h.")
                time.sleep(3600)  # Aguarda 1 hora

        else:
            # Fora do horário de publicações
            print("Fora do horário de publicação. Aguardando até a próxima janela.\n")
            time.sleep(3600)  # Aguarda 1 hora


# Parâmetros
usuario_instagram = 'XXX'
senha_instagram = 'XXX'
pasta_videos = r'XXX'
pasta_dicas = r'XXX'
pasta_motivacao = r'XXX'

# Executa o programa
automatizar_publicacoes(pasta_videos, pasta_dicas, pasta_motivacao,
                        usuario_instagram, senha_instagram)
