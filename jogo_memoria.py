import random
import time
import os

# Define os pares: palavras e seus "imagens" representadas por emojis

PARES_BASE = [
    ("Cão", "🐕"), ("Gato", "🐈"), ("Pássaro", "🐦"), ("Peixe", "🐟"),
    ("Leão", "🦁"), ("Elefante", "🐘"), ("Macaco", "🐒"), ("Coelho", "🐇"),
    ("Cavalo", "🐴"), ("Vaca", "🐄"), ("Porco", "🐖"), ("Ovelha", "🐑"),
    ("Galinha", "🐔"), ("Pato", "🦆"), ("Raposa", "🦊"), ("Urso", "🐻"),
    ("Tigre", "🐅"), ("Girafa", "🦒"), ("Zebra", "🦓"), ("Hipopótamo", "🦛"),
    ("Rinoceronte", "🦏"), ("Crocodilo", "🐊"), ("Serpente", "🐍"), ("Sapo", "🐸"),
    ("Abelha", "🐝"), ("Borboleta", "🦋"), ("Aranha", "🕷️"), ("Carro", "🚗"),
    ("Avião", "✈️"), ("Barco", "🚤"), ("Trem", "🚆"), ("Bicicleta", "🚲")
]

NIVEIS = {
    "Iniciante": {"tamanho": 2, "pares": 2},
    "Intermediário": {"tamanho": 4, "pares": 8},
    "Profissional": {"tamanho": 6, "pares": 18},
    "Lendário": {"tamanho": 8, "pares": 32}
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print("Bem-vindo ao Jogo da Memória!")
    print("Escolha o nível de dificuldade:")
    for i, nivel in enumerate(NIVEIS.keys(), 1):
        print(f"{i}. {nivel}")
    while True:
        try:
            escolha = int(input("Digite o número do nível: "))
            niveis_lista = list(NIVEIS.keys())
            if 1 <= escolha <= len(niveis_lista):
                return niveis_lista[escolha - 1]
            print(f"Escolha um número entre 1 e {len(niveis_lista)}.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def preparar_tabuleiro(nivel):
    config = NIVEIS[nivel]
    num_pares = config["pares"]
    tamanho = config["tamanho"]
    
    pares_selecionados = random.sample(PARES_BASE, num_pares)
    cartas = []
    for palavra, imagem in pares_selecionados:
        cartas.append(palavra)
        cartas.append(imagem)
    
    random.shuffle(cartas)
    tabuleiro = [cartas[i*tamanho:(i+1)*tamanho] for i in range(tamanho)]
    revelado = [['| * |\t' for _ in range(tamanho)] for _ in range(tamanho)]
    matches = {palavra: imagem for palavra, imagem in pares_selecionados}
    matches.update({imagem: palavra for palavra, imagem in pares_selecionados})
    
    return tabuleiro, revelado, matches, tamanho

def exibir_tabuleiro(revelado, tamanho):
    print("  ", end="")
    for j in range(tamanho):
        print(f"{j:2}", end=" ")
    print()
    for i in range(tamanho):
        print(f"{i:2}", end=" ")
        for j in range(tamanho):
            print(f"{revelado[i][j]:<6}", end=" ")
        print()

def obter_posicao(mensagem, tamanho):
    while True:
        try:
            entrada = input(mensagem)
            linha, coluna = map(int, entrada.split(','))
            if 0 <= linha < tamanho and 0 <= coluna < tamanho:
                return linha, coluna
            print(f"Posição inválida. Deve ser entre 0 e {tamanho-1}.")
        except ValueError:
            print("Entrada inválida. Use o formato: linha,coluna (ex: 0,1)")

def jogar(nivel):
    inicio = time.time()
    tabuleiro, revelado, matches, tamanho = preparar_tabuleiro(nivel)
    pares_encontrados = 0
    tentativas = 0
    
    while pares_encontrados < NIVEIS[nivel]["pares"]:
        limpar_tela()
        exibir_tabuleiro(revelado, tamanho)
        print(f"\nNível: {nivel} | Tentativas: {tentativas} | Pares encontrados: {pares_encontrados}")
        
        pos1 = obter_posicao("Digite a posição da primeira carta (linha,coluna): ", tamanho)
        if revelado[pos1[0]][pos1[1]] != '*':
            print("Carta já revelada. Escolha outra.")
            time.sleep(1)
            continue
        
        revelado[pos1[0]][pos1[1]] = tabuleiro[pos1[0]][pos1[1]]
        limpar_tela()
        exibir_tabuleiro(revelado, tamanho)
        
        pos2 = obter_posicao("Digite a posição da segunda carta (linha,coluna): ", tamanho)
        if revelado[pos2[0]][pos2[1]] != '*' or pos1 == pos2:
            print("Escolha uma posição válida e diferente.")
            revelado[pos1[0]][pos1[1]] = '*'
            time.sleep(1)
            continue
        
        revelado[pos2[0]][pos2[1]] = tabuleiro[pos2[0]][pos2[1]]
        limpar_tela()
        exibir_tabuleiro(revelado, tamanho)
        
        tentativas += 1
        carta1 = tabuleiro[pos1[0]][pos1[1]]
        carta2 = tabuleiro[pos2[0]][pos2[1]]
        if matches.get(carta1) == carta2:
            print("Match encontrado!")
            pares_encontrados += 1
            time.sleep(2)
        else:
            print("Não é match. Tentando novamente...")
            time.sleep(2)
            revelado[pos1[0]][pos1[1]] = '*'
            revelado[pos2[0]][pos2[1]] = '*'
    
    limpar_tela()
    exibir_tabuleiro(revelado, tamanho)
    tempo_total = time.time() - inicio
    print(f"\nParabéns! Você completou o nível {nivel} em {tentativas} tentativas.")
    print(f"Tempo total: {tempo_total:.2f} segundos.")

def main():
    while True:
        nivel = exibir_menu()
        jogar(nivel)
        opcao = input("\nDeseja jogar novamente? (s/n): ").lower()
        if opcao != 's':
            print("Obrigado por jogar!")
            break

if __name__ == "__main__":
    main()