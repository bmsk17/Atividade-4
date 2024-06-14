import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

def cromossomo_para_dataframe(cromossomo):
    container = list(range(30))
    posicao_inicial = cromossomo[:30]
    posicao_final = cromossomo[30:60]
    ordem_movimentacao = cromossomo[60:90]
    
    df = pd.DataFrame({
        'Container': container,
        'Posição Inicial': posicao_inicial,
        'Posição Final': posicao_final,
        'Ordem de Movimentação': ordem_movimentacao
    })
        
    df = df.sort_values(by='Ordem de Movimentação')
    
    return df

def Simular_preencher_porto(df_cromossomo):
    # Inicializar o porto e balsa
    porto = np.zeros((2, 5, 3), dtype=int)
    balsa = np.zeros((3, 4, 3), dtype=int)
    porto_preenchido = np.ones((2, 5, 3), dtype=int)
    
    # Preencher o porto com os dados do cromossomo
    ordem_inicial = []
    ordem_final = []

    df_cromossomo = df_cromossomo.sort_values(by='Posição Inicial')
    for _, linha in df_cromossomo.iterrows():
        ordem_inicial.append(linha['Container'])
    idx = 0
    for andar in range(2):
        for x in range(5):
            for y in range(3):
                if idx < 30:
                    porto[andar, x, y] = ordem_inicial[idx]
                    idx += 1

    df_cromossomo = df_cromossomo.sort_values(by='Ordem de Movimentação')

    # Diretório para salvar os frames
    save_dir = 'frames_porto_balsa'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    frame_index = 0

    # Função para salvar o estado atual como imagem
    def save_frame(porto, balsa, frame_index, text):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(porto.reshape(-1, 3), cmap='gray', vmin=0, vmax=1)
        axes[0].set_title('Porto')
        axes[1].imshow(balsa.reshape(-1, 3), cmap='gray', vmin=0, vmax=1)
        axes[1].set_title('Balsa')
        plt.suptitle(text)
        plt.savefig(f'{save_dir}/frame_{frame_index}.png')
        plt.close()

    # Salvar estado inicial
    save_frame(porto_preenchido, balsa, frame_index, "Estado Inicial")
    frame_index += 1

    # Realizar movimentações
    for _, linha in df_cromossomo.iterrows():
        container = linha['Container']
        a_pos_inicial = linha['Posição Inicial']
        a_pos_final = linha['Posição Final']
        pos_inicial = linha['Posição Inicial'] 
        pos_final = linha['Posição Final'] 

        andar_ini, x_ini, y_ini = pos_inicial // 15, (pos_inicial % 15) // 3, (pos_inicial % 15) % 3
        andar_fin, x_fin, y_fin = pos_final // 12, (pos_final % 12) // 3, (pos_final % 12) % 3

        # Verificar se podemos remover do porto preenchido
        pode_mover = True
        if andar_ini < 1:
            if porto_preenchido[andar_ini + 1, x_ini, y_ini] == 1:
                pode_mover = False

        # Verificar se podemos adicionar à balsa
        if andar_fin > 0:
            if balsa[andar_fin - 1, x_fin, y_fin] == 0:
                pode_mover = False

        if pode_mover:
            # Atualizar porto_preenchido e balsa
            porto_preenchido[andar_ini, x_ini, y_ini] = 0
            balsa[andar_fin, x_fin, y_fin] = 1
            
            move_text = f"Movendo container {container} de {a_pos_inicial} para {a_pos_final}"
            print(move_text)
            save_frame(porto_preenchido, balsa, frame_index, move_text)
            frame_index += 1
        else:
            move_text = f"Não moveu container {container} de {a_pos_inicial} para {a_pos_final}"
            print(move_text)

    # Criar o GIF
    frames = []
    for i in range(frame_index):
        frame = Image.open(f'{save_dir}/frame_{i}.png')
        frames.append(frame)

    # Tamanho da sprite sheet
    rows = (frame_index // 4) + 1
    sprite_sheet_width = 4 * frames[0].width
    sprite_sheet_height = rows * frames[0].height

    # Criar a sprite sheet
    sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height))

    # Adicionar frames na sprite sheet
    for index, frame in enumerate(frames):
        x = (index % 4) * frame.width
        y = (index // 4) * frame.height
        sprite_sheet.paste(frame, (x, y))

    sprite_sheet.save("sprite_sheet.png")

    return frames, frame_index

melhor_cromossomo = [4, 27, 24, 2, 6, 25, 8, 7, 3, 22, 23, 18, 26, 20, 10, 29, 21, 14, 1, 15, 9, 0, 5, 16, 13, 12, 11, 28, 17, 19,
                     16, 3, 15, 26, 19, 11, 20, 7, 24, 18, 8, 12, 23, 17, 21, 2, 9, 29, 13, 0, 22, 25, 28, 1, 10, 6, 27, 5, 14, 4,
                     14, 0, 16, 24, 25, 2, 10, 20, 28, 12, 3, 17, 19, 6, 15, 21, 8, 26, 13, 1, 18, 27, 29, 9, 5, 11, 22, 4, 23, 7]

# Simular e gerar frames
df_cromossomo = cromossomo_para_dataframe(melhor_cromossomo)
frames, frame_index = Simular_preencher_porto(df_cromossomo)

# Criar GIF a partir da sprite sheet
def create_gif_from_spritesheet(sprite_sheet_path, frame_width, frame_height, frame_count, output_path):
    sprite_sheet = Image.open(sprite_sheet_path)
    frames = []

    for i in range(frame_count):
        x = (i % 4) * frame_width
        y = (i // 4) * frame_height
        frame = sprite_sheet.crop((x, y, x + frame_width, y + frame_height))
        frames.append(frame)

    frames[0].save(output_path, format='GIF',
                   append_images=frames[1:], save_all=True, duration=500, loop=0)

create_gif_from_spritesheet('sprite_sheet.png', frames[0].width, frames[0].height, frame_index, 'simulacao_porto_balsa.gif')

# Salvar o GIF
gif_path = "simulacao_porto_balsa.gif"
gif_path
