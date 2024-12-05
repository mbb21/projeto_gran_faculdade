#gera uma publicação com logo do avalanche contendo o texto de um txt

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# Função para converter um arquivo de texto em uma imagem
def converter_txt_para_imagem(caminho_arquivo_txt, pasta_destino, logo_path=None, largura_imagem=1080, altura_imagem=1080,
                              fonte_tamanho=45, espaçamento_entre_linhas=20):
    # Lê o conteúdo do arquivo de texto
    with open(caminho_arquivo_txt, 'r', encoding='utf-8') as file:
        texto = file.read()

    # Cria uma imagem em azul claro (fundo azul claro)
    imagem = Image.new('RGB', (largura_imagem, altura_imagem), (225, 246, 255))
    draw = ImageDraw.Draw(imagem)

    # Configura a fonte (você pode mudar o caminho para uma fonte de sua escolha)
    fonte = ImageFont.truetype("arial.ttf", fonte_tamanho)

    # Define as margens
    margem_esquerda_direita = 220
    margem_topo_inferior = 100

    # Calcula a área de texto disponível
    largura_texto = largura_imagem - 3 * margem_esquerda_direita
    altura_texto = altura_imagem - 2 * margem_topo_inferior

    # Quebra o texto em linhas de forma a caber na largura especificada
    linhas = textwrap.wrap(texto, width=(largura_texto / fonte.getbbox('A')[1]))

    # Ajusta o tamanho da fonte para caber o texto na altura especificada
    while draw.textbbox((0, 0), '\n'.join(linhas), font=fonte)[3] > altura_texto and fonte_tamanho > 10:
        fonte_tamanho -= 2
        fonte = ImageFont.truetype("arial.ttf", fonte_tamanho)
        linhas = textwrap.wrap(texto, width=int(largura_texto / fonte.getbbox('A')[2]))

    # Calcula a posição inicial para centralizar o texto
    altura_total_linhas = draw.textbbox((0, 0), '\n'.join(linhas), font=fonte)[3] + (espaçamento_entre_linhas * len(linhas))
    posicao_inicial_y = (altura_imagem - altura_total_linhas) / 2

    # Escreve cada linha na imagem com o espaçamento adicional entre linhas
    for linha in linhas:
        largura_linha = draw.textbbox((0, 0), linha, font=fonte)[2]
        altura_linha = draw.textbbox((0, 0), linha, font=fonte)[3] - draw.textbbox((0, 0), linha, font=fonte)[1]
        posicao_x = (largura_imagem - largura_linha) / 2  # Centraliza horizontalmente
        draw.text((posicao_x, posicao_inicial_y), linha, font=fonte, fill="black")
        posicao_inicial_y += altura_linha + espaçamento_entre_linhas

    # Adiciona a logo como marca d'água
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        # Redimensiona a logo para ocupar 50% da largura e altura da imagem
        nova_largura = largura_imagem
        nova_altura = altura_imagem
        logo = logo.resize((nova_largura, nova_altura))

        # Adiciona um canal alpha para manipular a transparência
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: p * 0.1)  # Ajusta a opacidade (30%)
        logo.putalpha(alpha)

        # Centraliza a logo
        posicao_logo = ((largura_imagem - nova_largura) // 2, (altura_imagem - nova_altura) // 2)
        imagem.paste(logo, posicao_logo, logo)  # A última parte é a máscara para transparência

    # Salva a imagem
    nome_arquivo_imagem = os.path.splitext(os.path.basename(caminho_arquivo_txt))[0] + '.jpg'
    caminho_imagem = os.path.join(pasta_destino, nome_arquivo_imagem)
    imagem.save(caminho_imagem, format='JPEG')
    print(f"Imagem salva como {caminho_imagem}")

    return caminho_imagem

# Função para converter todos os arquivos txt da pasta em imagens
def converter_todos_txt_para_imagem(pasta_txt, pasta_destino, logo_path=None):
    arquivos_txt = [f for f in os.listdir(pasta_txt) if f.endswith('.txt') and not f.startswith("PUBLICADO_")]

    for arquivo_txt in arquivos_txt:
        caminho_arquivo_txt = os.path.join(pasta_txt, arquivo_txt)
        converter_txt_para_imagem(caminho_arquivo_txt, pasta_destino, logo_path)

# Parâmetros
pasta_textos = r'C:\Users\Matheus\Desktop\publis'
pasta_imagens = r'C:\Users\Matheus\Desktop\publis\imagens'  # Pasta de destino para as imagens
logo_path = r'C:\Users\Matheus\Desktop\publis\logo original.png'  # Caminho para a logo

# Cria a pasta de destino, se não existir
if not os.path.exists(pasta_imagens):
    os.makedirs(pasta_imagens)

# Converte todos os arquivos de texto em imagens
converter_todos_txt_para_imagem(pasta_textos, pasta_imagens, logo_path)
