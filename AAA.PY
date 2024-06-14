import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def Simular_preencher_porto(df_cromossomo):
    # Inicializar o porto e balsa
    porto = np.zeros((2, 5, 3), dtype=int)
    balsa = np.zeros((3, 4, 3), dtype=int)
    porto_preenchido = np.ones((2, 5, 3), dtype=int)

    # Preencher o porto com os dados do cromossomo
    df_cromossomo = df_cromossomo.sort_values(by='Posição Inicial')
    idx = 0
    for andar in range(2):
        for x in range(5):
            for y in range(3):
                if idx < 30:
                    porto[andar, x, y] = df_cromossomo.iloc[idx]['Container']
                    idx += 1

    df_cromossomo = df_cromossomo.sort_values(by='Ordem de Movimentação')

    movimentos = []
    
    # Realizar movimentações
    for _, linha in df_cromossomo.iterrows():
        container = linha['Container']
        pos_inicial = linha['Posição Inicial'] 
        pos_final = linha['Posição Final']
        
        andar_ini, x_ini, y_ini = pos_inicial // 15, (pos_inicial % 15) // 3, (pos_inicial % 15) % 3
        andar_fin, x_fin, y_fin = pos_final // 12, (pos_final % 12) // 3, (pos_final % 12) % 3
        
        # Verificar se podemos mover
        pode_mover = True
        if andar_ini < 1:
            if porto_preenchido[andar_ini + 1, x_ini, y_ini] == 1:
                pode_mover = False
        if andar_fin > 0:
            pode_mover = False
        
        if pode_mover:
            # Atualizar porto_preenchido e balsa
            porto_preenchido[andar_ini, x_ini, y_ini] = 0
            balsa[andar_fin, x_fin, y_fin] = 1
            movimentos.append((container, (andar_ini, x_ini, y_ini), (andar_fin, x_fin, y_fin)))

    return movimentos, porto, balsa

# Função para converter o cromossomo em DataFrame
def cromossomo_para_dataframe(cromossomo):
    data = {'Container': list(range(30)),
            'Posição Inicial': cromossomo[:30],
            'Posição Final': cromossomo[30:60],
            'Ordem de Movimentação': cromossomo[60:]}
    return pd.DataFrame(data)

# Exemplo de cromossomo
melhor_cromossomo = [4, 27, 24, 2, 6, 25, 8, 7, 3, 22, 23, 18, 26, 20, 10, 29, 21, 14, 1, 15, 9, 0, 5, 16, 13, 12, 11, 28, 17, 19,
                     16, 3, 15, 26, 19, 11, 20, 7, 24, 18, 8, 12, 23, 17, 21, 2, 9, 29, 13, 0, 22, 25, 28, 1, 10, 6, 27, 5, 14, 4,
                     14, 0, 16, 24, 25, 2, 10, 20, 28, 12, 3, 17, 19, 6, 15, 21, 8, 26, 13, 1, 18, 27, 29, 9, 5, 11, 22, 4, 23, 7]

df_cromossomo = cromossomo_para_dataframe(melhor_cromossomo)
movimentos, porto, balsa = Simular_preencher_porto(df_cromossomo)

# Função para visualizar o porto e a balsa
def plot_estado(porto, balsa, movimentos):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes[0, 0].imshow(porto[0], cmap='Greys', interpolation='nearest')
    axes[0, 0].set_title('Porto Andar 1')
    axes[1, 0].imshow(porto[1], cmap='Greys', interpolation='nearest')
    axes[1, 0].set_title('Porto Andar 2')
    axes[0, 1].imshow(balsa[0], cmap='Greys', interpolation='nearest')
    axes[0, 1].set_title('Balsa Andar 1')
    axes[1, 1].imshow(balsa[1], cmap='Greys', interpolation='nearest')
    axes[1, 1].set_title('Balsa Andar 2')
    plt.show()

# Animação do carregamento
def animar(movimentos, porto, balsa):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    def update(frame):
        container, pos_inicial, pos_final = movimentos[frame]
        andar_ini, x_ini, y_ini = pos_inicial
        andar_fin, x_fin, y_fin = pos_final
        
        porto[andar_ini, x_ini, y_ini] = 0
        balsa[andar_fin, x_fin, y_fin] = container
        
        axes[0, 0].cla()
        axes[1, 0].cla()
        axes[0, 1].cla()
        axes[1, 1].cla()
        
        axes[0, 0].imshow(porto[0], cmap='Greys', interpolation='nearest')
        axes[0, 0].set_title('Porto Andar 1')
        axes[1, 0].imshow(porto[1], cmap='Greys', interpolation='nearest')
        axes[1, 0].set_title('Porto Andar 2')
        axes[0, 1].imshow(balsa[0], cmap='Greys', interpolation='nearest')
        axes[0, 1].set_title('Balsa Andar 1')
        axes[1, 1].imshow(balsa[1], cmap='Greys', interpolation='nearest')
        axes[1, 1].set_title('Balsa Andar 2')

    ani = animation.FuncAnimation(fig, update, frames=len(movimentos), repeat=False)
    plt.show()

# Visualizar o estado inicial
plot_estado(porto, balsa, movimentos)
# Animar o carregamento
animar(movimentos, porto, balsa)
