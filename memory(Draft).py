import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import time
import os

class MemoryGame:
    def __init__(self, master, level):
        self.master = master
        self.level = level
        self.master.title(f"Jogo da Memória - {level}")
        self.master.geometry("800x700")
        self.master.configure(bg='#2c3e50')
        
        # Dados do jogo
        self.cards = []
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0
        self.total_pairs = 0
        self.start_time = None
        self.elapsed_time = 0
        self.moves = 0
        
        # Definindo as palavras e caminhos das imagens
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Palavras e caminhos das imagens (substitua pelos seus caminhos reais)
        self.words_images = {
            "Gato": os.path.join(BASE_DIR, "images", "business-cat.png"),
            "Cachorro": os.path.join(BASE_DIR, "images", "happy-dog.png"),
            "Pássaro": os.path.join(BASE_DIR, "images", "bird-amazonian.png"),
            "Peixe": os.path.join(BASE_DIR, "images", "Koi-Fish.png"),
            "Leão": os.path.join(BASE_DIR, "images", "lion-head.png"),
            "Tigre": os.path.join(BASE_DIR, "images", "tiger-face.png"),
            "Elefante": os.path.join(BASE_DIR, "images", "elephant-icon.png"),
            "Urso": os.path.join(BASE_DIR, "images", "angry-bear-head.png"),
            "Cavalo": os.path.join(BASE_DIR, "images", "horse.png"),
            "Coelho": os.path.join(BASE_DIR, "images", "rabbit.png"),
            "Macaco": os.path.join(BASE_DIR, "images", "monkey.png"),
            "Girafa": os.path.join(BASE_DIR, "images", "giraffe.png"),
            "Zebra": os.path.join(BASE_DIR, "images", "zebra.png"),
            "Rinoceronte": os.path.join(BASE_DIR, "images", "rhino.png"),
            "Hipopótamo": os.path.join(BASE_DIR, "images", "hippo.png"),
            "Panda": os.path.join(BASE_DIR, "images", "panda.png")
        }
        
        # Imagem padrão para as cartas viradas
       
        self.card_back_image = self.load_and_resize_image("images/card_back.png", 100, 100)
        
        self.create_color_image(100, 100, "#3498db")
        self.create_game_interface()
        self.start_game()

    def load_and_resize_image(self, image_path, width, height):
        """Carrega e redimensiona uma imagem"""
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            # Fallback para um quadrado colorido se a imagem não existir
            return self.create_color_image(width, height, "#3498db")
    
    def create_color_image(self, width, height, color):
        """Cria uma imagem de cor sólida como fallback"""
        image = Image.new('RGB', (width, height), color)
        return ImageTk.PhotoImage(image)
    
    def create_game_interface(self):
        """Cria a interface do jogo"""
        # Frame principal
        main_frame = tk.Frame(self.master, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Painel de informações
        info_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(info_frame, text=f"Nível: {self.level}", 
                bg='#34495e', fg='white', font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10, pady=5)
        
        self.moves_label = tk.Label(info_frame, text="Movimentos: 0", 
                                   bg='#34495e', fg='white', font=('Arial', 12))
        self.moves_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.time_label = tk.Label(info_frame, text="Tempo: 00:00", 
                                  bg='#34495e', fg='white', font=('Arial', 12))
        self.time_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.pairs_label = tk.Label(info_frame, text="Pares: 0/0", 
                                   bg='#34495e', fg='white', font=('Arial', 12))
        self.pairs_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame do tabuleiro
        self.board_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.board_frame.pack(expand=True)
        
        # Botão de reinício
        restart_btn = tk.Button(main_frame, text="Reiniciar", command=self.restart_game,
                               bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=5)
        restart_btn.pack(pady=10)

    def start_game(self):
        """Inicia o jogo"""
        num_pairs = self.get_num_pairs()
        self.total_pairs = num_pairs
        
        # Seleciona pares aleatórios
        available_words = list(self.words_images.keys())
        selected_words = random.sample(available_words, num_pairs)
        
        # Cria pares de cartas
        self.cards = selected_words * 2
        random.shuffle(self.cards)
        
        self.create_board()
        self.start_timer()
        self.update_pairs_label()

    def get_num_pairs(self):
        """Retorna o número de pares baseado no nível"""
        levels = {
            "Iniciante": 4,
            "Intermediário": 6,
            "Profissional": 8,
            "Lendário": 12
        }
        return levels.get(self.level, 4)

    def create_board(self):
        """Cria o tabuleiro de cartas"""
        num_pairs = self.get_num_pairs()
        cols = 4 if num_pairs <= 8 else 6
        
        self.buttons = []
        for i in range((num_pairs * 2 + cols - 1) // cols):
            row = []
            for j in range(cols):
                if i * cols + j < len(self.cards):
                    card_text = self.cards[i * cols + j]
                    card_image = self.load_and_resize_image(self.words_images[card_text], 80, 80)
                    
                    btn = tk.Button(self.board_frame, image=self.card_back_image,
                                   compound=tk.CENTER, text=card_text, fg='#3498db',
                                   command=lambda i=i, j=j: self.card_click(i, j),
                                   bg='#3498db', relief=tk.RAISED, bd=2)
                    btn.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                    btn.config(width=100, height=100)
                    btn.image = self.card_back_image  # Mantém referência
                    btn.card_image = card_image  # Imagem da carta
                    btn.is_flipped = False
                    btn.is_matched = False
                    
                    row.append(btn)
                else:
                    # Espaço vazio
                    empty = tk.Label(self.board_frame, bg='#2c3e50')
                    empty.grid(row=i, column=j)
                    row.append(None)
            self.buttons.append(row)
        
        # Configura weight para centralizar
        for i in range(len(self.buttons)):
            self.board_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.board_frame.grid_columnconfigure(j, weight=1)

    def card_click(self, i, j):
        """Lida com o clique em uma carta"""
        if self.buttons[i][j] is None or self.buttons[i][j].is_matched or self.buttons[i][j].is_flipped:
            return
        
        if self.first_card is None:
            # Primeira carta
            self.flip_card(i, j)
            self.first_card = (i, j)
        elif self.second_card is None:
            # Segunda carta
            self.flip_card(i, j)
            self.second_card = (i, j)
            self.moves += 1
            self.update_moves_label()
            self.master.after(800, self.check_match)

    def flip_card(self, i, j):
        """Vira a carta"""
        btn = self.buttons[i][j]
        btn.config(image=btn.card_image)
        btn.is_flipped = True

    def check_match(self):
        """Verifica se as cartas são um par"""
        i1, j1 = self.first_card
        i2, j2 = self.second_card
        
        btn1 = self.buttons[i1][j1]
        btn2 = self.buttons[i2][j2]
        
        if btn1['text'] == btn2['text']:
            # Par encontrado!
            btn1.is_matched = True
            btn2.is_matched = True
            btn1.config(bg='#27ae60', state=tk.DISABLED,fg= "#f5f9fc")
            btn2.config(bg='#27ae60', state=tk.DISABLED, fg="#f5f9fc")
            self.matched_pairs += 1
            self.update_pairs_label()
            
            if self.matched_pairs == self.total_pairs:
                self.game_over()
        else:
            # Não é par, vira as cartas de volta
            btn1.config(image=self.card_back_image)
            btn2.config(image=self.card_back_image)
            btn1.config(state=tk.NORMAL)
            btn2.config(state=tk.NORMAL)
            btn1.is_flipped = False
            btn2.is_flipped = False
        
        self.first_card = None
        self.second_card = None

    def start_timer(self):
        """Inicia o cronômetro"""
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """Atualiza o cronômetro"""
        if self.start_time and self.matched_pairs < self.total_pairs:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            self.time_label.config(text=f"Tempo: {minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_timer)

    def update_moves_label(self):
        """Atualiza o contador de movimentos"""
        self.moves_label.config(text=f"Movimentos: {self.moves}")

    def update_pairs_label(self):
        """Atualiza o contador de pares"""
        self.pairs_label.config(text=f"Pares: {self.matched_pairs}/{self.total_pairs}")

    def game_over(self):
        """Finaliza o jogo e mostra resultados"""
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        
        message = (
            f"🎉 Parabéns! Você completou o jogo!\n\n"
            f"📊 Estatísticas:\n"
            f"• Nível: {self.level}\n"
            f"• Tempo: {minutes:02d}:{seconds:02d}\n"
            f"• Movimentos: {self.moves}\n"
            f"• Pares encontrados: {self.matched_pairs}/{self.total_pairs}\n\n"
            f"🏆 Desempenho: {self.calculate_performance()}"
        )
        
        messagebox.showinfo("Fim de Jogo", message)

    def calculate_performance(self):
        """Calcula a performance baseada em tempo e movimentos"""
        efficiency = self.moves / self.total_pairs if self.total_pairs > 0 else 0
        time_score = self.elapsed_time / 60  # minutos
        
        if efficiency <= 1.5 and time_score <= 2:
            return "Excelente! 🥇"
        elif efficiency <= 2.0 and time_score <= 3:
            return "Muito bom! 🥈"
        elif efficiency <= 2.5:
            return "Bom! 🥉"
        else:
            return "Continue praticando! 💪"

    def restart_game(self):
        """Reinicia o jogo"""
        # Limpa o tabuleiro atual
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Reseta variáveis
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0
        self.moves = 0
        self.start_time = None
        self.elapsed_time = 0
        
        # Atualiza labels
        self.update_moves_label()
        self.time_label.config(text="Tempo: 00:00")
        
        # Inicia novo jogo
        self.start_game()

def main_menu():
    """Menu principal para escolher o nível"""
    root = tk.Tk()
    root.title("Jogo da Memória")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(BASE_DIR, "images", "memory_icon.png")
    try:
        root.iconphoto(False, tk.PhotoImage(file=icon_path))
    except tk.TclError:
        pass  # Ignore if icon file is missing or fails to load
    root.geometry("500x650")
    root.configure(bg='#2c3e50')
    
    # Título
    title_label = tk.Label(root, text="🎮 Jogo da Memória", 
                          bg='#2c3e50', fg='white', 
                          font=('Arial', 20, 'bold'))
    title_label.pack(pady=30)
    
    # Instruções
    instructions = tk.Label(root, 
                          text="Encontre os pares de imagens com suas palavras correspondentes!\n\nEscolha o nível de dificuldade:",
                          bg='#2c3e50', fg='white', 
                          font=('Arial', 12), justify=tk.CENTER)
    instructions.pack(pady=20)
    
    # Frame dos botões
    button_frame = tk.Frame(root, bg='#2c3e50')
    button_frame.pack(pady=30)
    
    levels = [
        ("Iniciante", "4 pares - Fácil", "#27ae60"),
        ("Intermediário", "6 pares - Médio", "#f39c12"), 
        ("Profissional", "8 pares - Difícil", "#e74c3c"),
        ("Lendário", "12 pares - Extremo", "#9b59b6")
    ]
    
    for level, description, color in levels:
        frame = tk.Frame(button_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        btn = tk.Button(frame, text=f"{level}\n{description}", 
                       command=lambda l=level: [root.destroy(), start_game(l)],
                       bg=color, fg='white', font=('Arial', 12, 'bold'),
                       width=20, height=2, cursor='hand2')
        btn.pack(padx=10, pady=10)
    
    root.mainloop()

def start_game(level):
    """Inicia o jogo com o nível escolhido"""
    root = tk.Tk()
    game = MemoryGame(root, level)
    root.mainloop()

if __name__ == "__main__":
    # Cria diretório de imagens se não existir
    # if not os.path.exists('images'):
    #     os.makedirs('images')
    #     print("Diretório 'images' criado. Adicione suas imagens lá!")
    
    main_menu()

