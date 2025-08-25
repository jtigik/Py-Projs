import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Definindo as palavras e caminhos das imagens
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
words_images = {
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

class MemoryGame:
    def __init__(self, master, level):
        self.master = master
        self.level = level
        self.cards = []
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0
        self.photo_images = {}  # Para manter referências às imagens
        self.load_images()
        self.create_game_board()

    def load_images(self):
        """Carrega e redimensiona todas as imagens"""
        for word, image_path in words_images.items():
            
            try:
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                self.photo_images[word] = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Erro ao carregar imagem {image_path}: {e}")
                # Fallback: criar imagem com texto
                image = Image.new('RGB', (100, 100), color='lightblue')
                try:
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.load_default()
                    text = word
                    text_width, text_height = draw.textsize(text, font=font)
                    x = (100 - text_width) // 2
                    y = (100 - text_height) // 2
                    draw.text((x, y), text, fill='black', font=font)
                except Exception:
                    pass
                self.photo_images[word] = ImageTk.PhotoImage(image)

    def create_game_board(self):
        self.frame = tk.Frame(self.master, bg='#2c3e50')
        self.frame.pack(pady=20)
        
        num_pairs = self.get_num_pairs()
        available_words = list(words_images.keys())
        selected_words = random.sample(available_words, num_pairs)
        self.cards = selected_words * 2
        random.shuffle(self.cards)

        self.buttons = []
        rows, cols = self.get_grid_size(num_pairs)
        
        # Imagem padrão para cartas viradas (back)
        back_image = Image.new('RGB', (100, 100), color='#3498db')
        back_photo = ImageTk.PhotoImage(back_image)
        
        for i in range(rows):
            row = []
            for j in range(cols):
                index = i * cols + j
                if index < len(self.cards):
                    button = tk.Button(
                        self.frame, 
                        image=back_photo,
                        width=100,
                        height=100,
                        command=lambda i=i, j=j: self.card_click(i, j),
                        bg='#3498db',
                        relief='raised',
                        bd=3
                    )
                    button.grid(row=i, column=j, padx=5, pady=5)
                    button.image = back_photo  # Manter referência
                    row.append(button)
            self.buttons.append(row)

    def get_num_pairs(self):
        if self.level == "Iniciante":
            return 4
        elif self.level == "Intermediário":
            return 6
        elif self.level == "Profissional":
            return 8
        elif self.level == "Lendário":
            return 12

    def get_grid_size(self, num_pairs):
        total_cards = num_pairs * 2
        if total_cards <= 8:
            return (2, 4)
        elif total_cards <= 12:
            return (3, 4)
        elif total_cards <= 16:
            return (4, 4)
        else:
            return (4, 6)

    def card_click(self, i, j):
        if self.buttons[i][j]['state'] == 'disabled':
            return
            
        if self.first_card is None:
            self.first_card = (i, j)
            word = self.cards[i * len(self.buttons[0]) + j]
            self.buttons[i][j].config(image=self.photo_images[word])
        elif self.second_card is None and (i, j) != self.first_card:
            self.second_card = (i, j)
            word = self.cards[i * len(self.buttons[0]) + j]
            self.buttons[i][j].config(image=self.photo_images[word])
            self.master.after(1000, self.check_match)

    def check_match(self):
        i1, j1 = self.first_card
        i2, j2 = self.second_card
        
        index1 = i1 * len(self.buttons[0]) + j1
        index2 = i2 * len(self.buttons[0]) + j2
        
        word1 = self.cards[index1]
        word2 = self.cards[index2]
        
        if word1 == word2:
            # Cartas combinam - desabilitar os botões
            self.buttons[i1][j1].config(state='disabled', relief='sunken')
            self.buttons[i2][j2].config(state='disabled', relief='sunken')
            self.matched_pairs += 1
            
            if self.matched_pairs == len(self.cards) // 2:
                messagebox.showinfo("Parabéns!", "Você completou o jogo da memória!")
                self.master.destroy()
                main_menu()
        else:
            # Cartas não combinam - virar de volta
            back_image = Image.new('RGB', (100, 100), color='#3498db')
            back_photo = ImageTk.PhotoImage(back_image)
            
            self.buttons[i1][j1].config(image=back_photo)
            self.buttons[i1][j1].image = back_photo
            self.buttons[i2][j2].config(image=back_photo)
            self.buttons[i2][j2].image = back_photo
        
        self.first_card = None
        self.second_card = None

def start_game(level):
    root = tk.Tk()
    root.title(f"Jogo da Memória - Nível {level}")
    root.configure(bg='#2c3e50')
    root.resizable(False, False)
    
    # Centralizar a janela
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    game = MemoryGame(root, level)
    root.mainloop()

def main_menu():
    menu = tk.Tk()
    menu.title("Jogo da Memória")
    menu.configure(bg='#34495e')
    menu.resizable(False, False)
    
    # Centralizar a janela
    window_width = 400
    window_height = 600
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    menu.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Título
    title_label = tk.Label(
        menu,
        text="Jogo da Memória", 
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#34495e"
    )
    title_label.pack(pady=30)
    
    # Instruções
    instructions = tk.Label(
        menu,
        text="Encontre os pares de imagens correspondentes!\n\nEscolha o nível de dificuldade:",
        font=("Arial", 12),
        fg="white",
        bg="#34495e",
        justify="center"
    )
    instructions.pack(pady=20)
    
    # Botões de nível
    levels = ["Iniciante", "Intermediário", "Profissional", "Lendário"]
    colors = ["#27ae60", "#f39c12", "#e74c3c", "#9b59b6"]
    
    for level, color in zip(levels, colors):
        button = tk.Button(
            menu, 
            text=level,
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            bg=color,
            fg="white",
            relief="raised",
            bd=3,
            command=lambda l=level: [menu.destroy(), start_game(l)]
        )
        button.pack(pady=10)

    menu.mainloop()

if __name__ == "__main__":
    # Criar diretório de imagens se não existir
    # if not os.path.exists('./images/'):
    #     os.makedirs('./images/')
    #     print("Diretório 'images' criado. Por favor, adicione as imagens:")
    #     for word in words_images.keys():
    #         print(f"- {words_images[word]}")
    
    main_menu()
