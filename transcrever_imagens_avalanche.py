#transforma o que está escrito nas imagens em um arquivo txt

import os
import easyocr
from PIL import Image
import re


def limpar_texto(texto):
    # Remove espaços duplicados
    texto = re.sub(r'\s+', ' ', texto)

    # Remove espaços antes de ponto final e vírgula
    texto = re.sub(r'\s+([.,;?!])', r'\1', texto)

    # Junta palavras que têm um espaço antes da pontuação
    texto = re.sub(r'(\w+)\s+([!.?])', r'\1\2', texto)

    # Insere espaço antes de vírgulas e pontos que estão colados à próxima palavra
    texto = re.sub(r'([,.])([^\s])', r'\1 \2', texto)

    # Altera todos os ';' para ','
    texto = texto.replace(';', ',')

    # Adiciona ponto final se a última palavra não terminar com ponto final, exclamação ou interrogação
    if not texto.endswith(('.', '!', '?')):
        texto += '.'

    # Capitaliza a primeira letra do texto, caso não esteja capitalizada
    texto = texto.strip()
    if texto:
        texto = texto[0].upper() + texto[1:]

    # Substituições adicionais, evitando substituir '0' quando precedido por outro número
    texto = re.sub(r'(?<!\d)0', 'o', texto)
    texto = texto.replace('66', '"')
    texto = texto.replace("'", '"')
    texto = texto.replace('@motivacao_estudar', '')

    return texto.strip()


def limpar_texto_final(texto):
    # Remove espaços antes da primeira palavra
    texto = texto.lstrip()

    # Coloca a primeira letra de cada nova frase em maiúscula
    texto = re.sub(r'(?<=[.!?])\s*([a-z])', lambda m: ' ' + m.group(1).upper(), texto)

    # Adiciona ponto final após palavras iniciadas por maiúscula que não possuem ponto final após a palavra predecessora
    def adicionar_ponto_final(match):
        palavra = match.group(0)
        return f'. {palavra}' if not match.group(1) else palavra

    # Expressão regular para encontrar palavras iniciadas por maiúscula que não estão precedidas por ponto
    texto = re.sub(r'(?<![.!?\-\"\'])\s+([A-Z]\w*)', lambda m: '. ' + m.group(1), texto)

    return texto.strip()

def processar_imagens(diretorio):
    # Instancia o leitor do EasyOCR (use 'pt' para português)
    leitor = easyocr.Reader(['pt'])

    # Inicializa um contador para o nome das publicações
    contador = 1

    # Percorre todos os arquivos da pasta
    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".jpg"):  # Verifica se o arquivo é JPG
            caminho_arquivo = os.path.join(diretorio, arquivo)

            try:
                # Abre a imagem para verificar se o arquivo é uma imagem válida
                Image.open(caminho_arquivo).verify()

                # Realiza a leitura de texto na imagem usando o EasyOCR
                resultado = leitor.readtext(caminho_arquivo, detail=0)

                # Cria um nome para o arquivo .txt usando o contador
                nome_txt = f"publicacao {contador}.txt"
                caminho_txt = os.path.join(diretorio, nome_txt)

                print(resultado)

                # Une as linhas de texto e limpa o texto
                resultado_unificado = ' '.join(resultado)
                resultado_limpo = limpar_texto(resultado_unificado)
                resultado_limpo = limpar_texto_final(resultado_limpo)

                print(resultado_limpo)

                with open(caminho_txt, 'w', encoding='utf-8') as txt:
                    if resultado_limpo:
                        txt.write(resultado_limpo)
                    else:
                        txt.write("Nenhum texto detectado na imagem.")

                print(f"Processado: {arquivo} -> {nome_txt}")
                contador += 1  # Incrementa o contador para a próxima imagem

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

# Caminho para a pasta contendo as imagens
diretorio_imagens = r"C:\Users\Matheus\Desktop\publis"
processar_imagens(diretorio_imagens)
