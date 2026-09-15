import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import io
import urllib.request
from datetime import datetime

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

# ===================== ARQUIVOS =====================

ARQUIVO_CARDAPIO = "cardapio.json"
ARQUIVO_PEDIDOS = "pedidos.json"
ARQUIVO_USUARIOS = "usuarios.json"

# ===================== TEMAS =====================

TEMA_ESCURO = {
    "fundo": "#121212", "card": "#1E1E1E", "acento": "#693DE2",
    "texto": "#FFFFFF", "subtitulo": "#8B39E7",
    "entry_bg": "#2A2A2A", "entry_fg": "#FFFFFF",
    "btn_tema": "☀️ Modo Claro"
}

TEMA_CLARO = {
    "fundo": "#F4F4F9", "card": "#FFFFFF", "acento": "#1D46B9",
    "texto": "#222222", "subtitulo": "#0065D9",
    "entry_bg": "#FFFFFF", "entry_fg": "#000000",
    "btn_tema": "🌙 Modo Escuro"
}

# ===================== FONTES =====================

FONTE_TITULO = ("Segoe UI", 22, "bold")
FONTE_TAB = ("Segoe UI", 11, "bold")
FONTE_ITEM = ("Segoe UI", 11, "bold")
FONTE_DESC = ("Segoe UI", 9)
FONTE_TOTAL = ("Segoe UI", 16, "bold")
FONTE_BOTAO = ("Segoe UI", 11, "bold")

QUANTIDADE_COLUNAS = 4
TAMANHO_IMAGEM = (230, 130)

# ===================== IMAGENS =====================

IMAGENS_PRODUTOS = {
    "Poderoso Chefão": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80",
    "Clássico Smash": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&q=80",
    "Veggie Supreme": "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=500&q=80",
    "Duplo Bacon": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&q=80",
    "Chicken Crispy": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=500&q=80",
    "Monster Burger": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=500&q=80",
    "Calabresa": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&q=80",
    "Marguerita": "https://images.unsplash.com/photo-1579751626657-72bc17010498?w=500&q=80",
    "Quatro Queijos": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=500&q=80",
    "Frango Catupiry": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80",
    "Batata Rústica": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500&q=80",
    "Onion Rings": "https://images.unsplash.com/photo-1639024471283-03518883512d?w=500&q=80",
    "Batata Cheddar/Bacon": "https://images.unsplash.com/photo-1585109649139-366815a0d713?w=500&q=80",
    "Soda Artesanal": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=500&q=80",
    "Milkshake": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=500&q=80",
    "Refrigerante": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=500&q=80"
}

# ===================== CARDÁPIO =====================

CARDAPIO_PADRAO = {
    "cardapio": [
        {
            "categoria": "🍔 HAMBÚRGUERES",
            "itens": [
                {"id": 101, "nome": "Poderoso Chefão", "preco": 34.90,
                 "descricao": "Blend 180g, gorgonzola, cebola caramelizada e bacon."},
                {"id": 102, "nome": "Clássico Smash", "preco": 22.00,
                 "descricao": "Dois hambúrgueres smash de 80g, cheddar e picles."},
                {"id": 103, "nome": "Veggie Supreme", "preco": 29.90,
                 "descricao": "Hambúrguer de grão-de-bico, rúcula e maionese de ervas."},
                {"id": 104, "nome": "Duplo Bacon", "preco": 38.50,
                 "descricao": "Dois blends 180g, triplo bacon e molho barbecue."},
                {"id": 105, "nome": "Chicken Crispy", "preco": 25.90,
                 "descricao": "Frango crocante, salada coleslaw e maionese."},
                {"id": 106, "nome": "Monster Burger", "preco": 44.00,
                 "descricao": "Três blends 150g, quádruplo cheddar e anéis de cebola."}
            ]
        },
        {
            "categoria": "🍕 PIZZAS",
            "itens": [
                {"id": 201, "nome": "Calabresa", "preco": 45.00,
                 "descricao": "Molho de tomate pelati, calabresa fatiada e cebola."},
                {"id": 202, "nome": "Marguerita", "preco": 42.00,
                 "descricao": "Muçarela de búfala, tomate e manjericão fresco."},
                {"id": 203, "nome": "Quatro Queijos", "preco": 50.00,
                 "descricao": "Muçarela, provolone, gorgonzola e parmesão."},
                {"id": 204, "nome": "Frango Catupiry", "preco": 48.00,
                 "descricao": "Frango desfiado temperado com legítimo Catupiry."}
            ]
        },
        {
            "categoria": "🍟 ACOMPANHAMENTOS",
            "itens": [
                {"id": 301, "nome": "Batata Rústica", "preco": 18.00,
                 "descricao": "Corte caseiro com alecrim e páprica defumada."},
                {"id": 302, "nome": "Onion Rings", "preco": 20.00,
                 "descricao": "Anéis de cebola crocantes com molho barbecue."},
                {"id": 303, "nome": "Batata Cheddar/Bacon", "preco": 28.00,
                 "descricao": "Porção grande com cheddar cremoso e bacon."}
            ]
        },
        {
            "categoria": "🥤 BEBIDAS",
            "itens": [
                {"id": 401, "nome": "Soda Artesanal", "preco": 12.00,
                 "descricao": "Frutas vermelhas, limão siciliano e gás (500ml)."},
                {"id": 402, "nome": "Milkshake", "preco": 18.00,
                 "descricao": "Morango, Chocolate ou Ovaltine (400ml)."},
                {"id": 403, "nome": "Refrigerante", "preco": 6.50,
                 "descricao": "Lata 350ml (Coca, Guaraná ou Sprite)."}
            ]
        }
    ]
}

# ===================== ARQUIVOS =====================

def carregar_cardapio():
    if not os.path.exists(ARQUIVO_CARDAPIO):
        with open(ARQUIVO_CARDAPIO, "w", encoding="utf-8") as arquivo:
            json.dump(CARDAPIO_PADRAO, arquivo, ensure_ascii=False, indent=2)
        return CARDAPIO_PADRAO["cardapio"]

    try:
        with open(ARQUIVO_CARDAPIO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo).get("cardapio", [])
    except Exception:
        return CARDAPIO_PADRAO["cardapio"]


def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados if isinstance(dados, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)


def registrar_pedido(pedido):
    historico = []

    if os.path.exists(ARQUIVO_PEDIDOS):
        try:
            with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as arquivo:
                historico = json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            historico = []

    if not isinstance(historico, list):
        historico = []

    historico.append(pedido)

    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=2)


# ===================== SISTEMA =====================

class SistemaGourmetApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Gourmet Service")

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1200x800")

        self.modo_escuro = True
        self.cores = TEMA_ESCURO
        self.menu_data = carregar_cardapio()
        self.usuarios = carregar_usuarios()
        self.dados_cliente = {"nome": "", "usuario": "", "pagamento": "PIX"}
        self.pedidos = {}
        self.tela_atual = "login"

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.mostrar_tela_login()

    # ===================== TEMA =====================

    def alternar_tema(self):
        self.modo_escuro = not self.modo_escuro
        self.cores = TEMA_ESCURO if self.modo_escuro else TEMA_CLARO

        if self.tela_atual == "login":
            self.mostrar_tela_login()
        else:
            self.mostrar_tela_cardapio()

    def criar_botao_tema(self, parent):
        tk.Button(
            parent,
            text=self.cores["btn_tema"],
            command=self.alternar_tema,
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=("Segoe UI", 10, "bold"),
            relief="groove",
            cursor="hand2",
            padx=12,
            pady=4
        ).pack(side="right", padx=15)

    # ===================== LOGIN =====================

    def mostrar_tela_login(self):
        self.tela_atual = "login"
        self.root.configure(bg=self.cores["fundo"])

        for widget in self.container.winfo_children():
            widget.destroy()

        self.container.configure(bg=self.cores["fundo"])

        top = tk.Frame(self.container, bg=self.cores["fundo"])
        top.pack(fill="x", pady=10)
        self.criar_botao_tema(top)

        card = tk.Frame(
            self.container, bg=self.cores["card"],
            padx=45, pady=35, bd=1, relief="solid"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="🔥 GOURMET SERVICE 🔥", font=FONTE_TITULO,
            bg=self.cores["card"], fg=self.cores["acento"]
        ).pack(pady=(0, 5))

        tk.Label(
            card, text="LOGIN", font=("Segoe UI", 16, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack()

        tk.Label(
            card, text="Entre para acessar o cardápio",
            font=("Segoe UI", 10), bg=self.cores["card"],
            fg=self.cores["texto"]
        ).pack(pady=(3, 20))

        tk.Label(
            card, text="👤 Usuário", font=("Segoe UI", 10, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack(anchor="w")

        self.ent_login_usuario = tk.Entry(
            card, font=("Segoe UI", 11), width=32,
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"],
            insertbackground=self.cores["texto"]
        )
        self.ent_login_usuario.pack(pady=(3, 12))

        tk.Label(
            card, text="🔒 Senha", font=("Segoe UI", 10, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack(anchor="w")

        frame_senha = tk.Frame(card, bg=self.cores["card"])
        frame_senha.pack(fill="x", pady=(3, 5))

        self.ent_login_senha = tk.Entry(
            frame_senha, font=("Segoe UI", 11), width=25,
            show="*", bg=self.cores["entry_bg"],
            fg=self.cores["entry_fg"],
            insertbackground=self.cores["texto"]
        )
        self.ent_login_senha.pack(side="left")

        self.mostrar_senha = False

        self.btn_senha = tk.Button(
            frame_senha, text="👁", command=self.alternar_senha,
            bg=self.cores["entry_bg"], fg=self.cores["texto"],
            relief="flat", cursor="hand2"
        )
        self.btn_senha.pack(side="left", padx=5)

        tk.Button(
            card, text="ENTRAR ➜", command=self.fazer_login,
            bg=self.cores["acento"], fg="white",
            font=FONTE_BOTAO, relief="flat", cursor="hand2",
            padx=15, pady=9
        ).pack(fill="x", pady=(15, 8))

        tk.Button(
            card, text="📝 Criar nova conta",
            command=self.mostrar_tela_cadastro,
            bg=self.cores["card"], fg=self.cores["subtitulo"],
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2"
        ).pack()

        tk.Button(
            card, text="Limpar", command=self.limpar_login,
            bg=self.cores["card"], fg=self.cores["texto"],
            font=("Segoe UI", 9), relief="flat", cursor="hand2"
        ).pack(pady=(8, 0))

    def alternar_senha(self):
        self.mostrar_senha = not self.mostrar_senha
        self.ent_login_senha.config(show="" if self.mostrar_senha else "*")

    def limpar_login(self):
        self.ent_login_usuario.delete(0, tk.END)
        self.ent_login_senha.delete(0, tk.END)
        self.ent_login_usuario.focus()

    def fazer_login(self):
        usuario = self.ent_login_usuario.get().strip()
        senha = self.ent_login_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Login", "Digite o usuário e a senha.")
            return

        if usuario not in self.usuarios:
            messagebox.showerror(
                "Login",
                "Usuário não encontrado.\n\nCrie uma conta primeiro."
            )
            return

        dados = self.usuarios[usuario]

        if dados["senha"] != senha:
            messagebox.showerror("Login", "Senha incorreta.")
            return

        self.dados_cliente = {
            "nome": dados["nome"],
            "usuario": usuario,
            "pagamento": dados.get("pagamento", "PIX")
        }

        messagebox.showinfo(
            "Bem-vindo!",
            f"Olá, {dados['nome']}!\n\nLogin realizado com sucesso."
        )
        self.mostrar_tela_cardapio()

    # ===================== CADASTRO =====================

    def mostrar_tela_cadastro(self):
        self.tela_atual = "cadastro"
        self.root.configure(bg=self.cores["fundo"])

        for widget in self.container.winfo_children():
            widget.destroy()

        top = tk.Frame(self.container, bg=self.cores["fundo"])
        top.pack(fill="x", pady=10)
        self.criar_botao_tema(top)

        card = tk.Frame(
            self.container, bg=self.cores["card"],
            padx=45, pady=30, bd=1, relief="solid"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="📝 CRIAR CONTA", font=FONTE_TITULO,
            bg=self.cores["card"], fg=self.cores["acento"]
        ).pack(pady=(0, 20))

        tk.Label(
            card, text="Nome completo",
            font=("Segoe UI", 10, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack(anchor="w")

        self.ent_nome = tk.Entry(
            card, font=("Segoe UI", 11), width=32,
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"],
            insertbackground=self.cores["texto"]
        )
        self.ent_nome.pack(pady=(3, 12))

        tk.Label(
            card, text="Nome de usuário",
            font=("Segoe UI", 10, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack(anchor="w")

        self.ent_usuario = tk.Entry(
            card, font=("Segoe UI", 11), width=32,
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"],
            insertbackground=self.cores["texto"]
        )
        self.ent_usuario.pack(pady=(3, 12))

        tk.Label(
            card, text="Senha",
            font=("Segoe UI", 10, "bold"),
            bg=self.cores["card"], fg=self.cores["texto"]
        ).pack(anchor="w")

        self.ent_senha = tk.Entry(
            card, font=("Segoe UI", 11), width=32, show="*",
            bg=self.cores["entry_bg"], fg=self.cores["entry_fg"],
            insertbackground=self.cores["texto"]
        )
        self.ent_senha.pack(pady=(3, 12))

        tk.Button(
            card, text="CRIAR CONTA ➜", command=self.criar_conta,
            bg=self.cores["acento"], fg="white",
            font=FONTE_BOTAO, relief="flat", cursor="hand2",
            padx=15, pady=9
        ).pack(fill="x", pady=(0, 8))

        tk.Button(
            card, text="⬅ Voltar para Login",
            command=self.mostrar_tela_login,
            bg=self.cores["card"], fg=self.cores["subtitulo"],
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2"
        ).pack()

    def criar_conta(self):
        nome = self.ent_nome.get().strip()
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()

        if not nome or not usuario or not senha:
            messagebox.showwarning("Cadastro", "Preencha todos os campos.")
            return

        if len(usuario) < 3:
            messagebox.showwarning(
                "Cadastro",
                "O usuário precisa ter pelo menos 3 caracteres."
            )
            return

        if len(senha) < 4:
            messagebox.showwarning(
                "Cadastro",
                "A senha precisa ter pelo menos 4 caracteres."
            )
            return

        if usuario in self.usuarios:
            messagebox.showerror(
                "Cadastro",
                "Esse nome de usuário já existe."
            )
            return

        self.usuarios[usuario] = {
            "nome": nome,
            "senha": senha,
            "pagamento": "PIX"
        }

        salvar_usuarios(self.usuarios)

        messagebox.showinfo(
            "Conta criada!",
            f"Conta de @{usuario} criada com sucesso!\n\nAgora faça login."
        )

        self.mostrar_tela_login()
        self.ent_login_usuario.insert(0, usuario)
        self.ent_login_senha.focus()

    # ===================== CARDÁPIO =====================

    def mostrar_tela_cardapio(self):
        self.tela_atual = "cardapio"
        self.root.configure(bg=self.cores["fundo"])

        for widget in self.container.winfo_children():
            widget.destroy()

        header = tk.Frame(
            self.container, bg=self.cores["acento"], height=90
        )
        header.pack(fill="x")

        frame_top = tk.Frame(header, bg=self.cores["acento"])
        frame_top.pack(fill="x")

        tk.Label(
            frame_top, text="🔥 GOURMET SERVICE 🔥",
            font=FONTE_TITULO, bg=self.cores["acento"],
            fg="white"
        ).pack(side="left", padx=20, pady=(10, 0))

        self.criar_botao_tema(frame_top)

        info = (
            f"👤 {self.dados_cliente['nome']} "
            f"(@{self.dados_cliente['usuario']})"
            f"  |  💳 {self.dados_cliente['pagamento']}"
        )

        tk.Label(
            header, text=info, font=("Segoe UI", 10, "bold"),
            bg=self.cores["acento"], fg="white"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TNotebook",
            background=self.cores["fundo"],
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=self.cores["card"],
            foreground=self.cores["texto"],
            font=FONTE_TAB,
            padding=[15, 6]
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.cores["acento"])],
            foreground=[("selected", "white")]
        )

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(
            fill="both", expand=True, padx=15, pady=10
        )

        self.construir_abas()

        footer = tk.Frame(
            self.container, bg=self.cores["card"], height=100
        )
        footer.pack(fill="x", side="bottom")

        self.lbl_total = tk.Label(
            footer, text="TOTAL: R$ 0.00",
            font=FONTE_TOTAL, bg=self.cores["card"],
            fg=self.cores["acento"]
        )
        self.lbl_total.pack(pady=5)

        frame_botoes = tk.Frame(footer, bg=self.cores["card"])
        frame_botoes.pack()

        tk.Button(
            frame_botoes, text="⬅ Sair",
            command=self.mostrar_tela_login,
            bg="#555555", fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2",
            padx=15, pady=6
        ).pack(side="left", padx=10)

        tk.Button(
            frame_botoes, text="🛒 FINALIZAR PEDIDO",
            command=self.finalizar_pedido,
            bg=self.cores["acento"], fg="white",
            font=FONTE_BOTAO, relief="flat",
            cursor="hand2", padx=18, pady=6
        ).pack(side="left", padx=10)

        self.atualizar_total()

    def carregar_imagem_produto(self, nome):
        if Image is None or ImageTk is None:
            return None

        if not hasattr(self, "imagens_cache"):
            self.imagens_cache = {}

        if nome in self.imagens_cache:
            return self.imagens_cache[nome]

        url = IMAGENS_PRODUTOS.get(nome)
        if not url:
            return None

        try:
            requisicao = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(requisicao, timeout=5) as resposta:
                dados = resposta.read()

            imagem = Image.open(io.BytesIO(dados)).convert("RGB")
            imagem.thumbnail(TAMANHO_IMAGEM)

            fundo = Image.new("RGB", TAMANHO_IMAGEM)
            x = (TAMANHO_IMAGEM[0] - imagem.width) // 2
            y = (TAMANHO_IMAGEM[1] - imagem.height) // 2
            fundo.paste(imagem, (x, y))

            foto = ImageTk.PhotoImage(fundo)
            self.imagens_cache[nome] = foto
            return foto

        except Exception:
            return None

    def construir_abas(self):
        self.pedidos = {}

        for bloco in self.menu_data:
            categoria = bloco["categoria"]
            itens = bloco["itens"]

            frame_aba = tk.Frame(
                self.notebook, bg=self.cores["fundo"]
            )
            self.notebook.add(frame_aba, text=categoria)

            canvas = tk.Canvas(
                frame_aba, bg=self.cores["fundo"],
                highlightthickness=0
            )

            scrollbar = ttk.Scrollbar(
                frame_aba, orient="vertical",
                command=canvas.yview
            )

            scrollable = tk.Frame(
                canvas, bg=self.cores["fundo"]
            )

            scrollable.bind(
                "<Configure>",
                lambda e, c=canvas:
                c.configure(scrollregion=c.bbox("all"))
            )

            canvas.create_window(
                (0, 0), window=scrollable, anchor="nw"
            )
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(
                side="left", fill="both", expand=True
            )
            scrollbar.pack(
                side="right", fill="y"
            )

            for col in range(QUANTIDADE_COLUNAS):
                scrollable.grid_columnconfigure(col, weight=1)

            for index, item in enumerate(itens):
                nome = item["nome"]
                preco = item["preco"]
                descricao = item["descricao"]

                linha = index // QUANTIDADE_COLUNAS
                coluna = index % QUANTIDADE_COLUNAS

                card = tk.Frame(
                    scrollable, bg=self.cores["card"],
                    padx=12, pady=10
                )
                card.grid(
                    row=linha, column=coluna,
                    padx=8, pady=6, sticky="nsew"
                )

                foto = self.carregar_imagem_produto(nome)

                if foto:
                    label_imagem = tk.Label(
                        card, image=foto,
                        bg=self.cores["card"]
                    )
                    label_imagem.image = foto
                    label_imagem.pack(
                        fill="x", pady=(0, 8)
                    )
                else:
                    tk.Label(
                        card, text="🍽️",
                        font=("Segoe UI", 42),
                        bg=self.cores["card"],
                        fg=self.cores["texto"], height=2
                    ).pack(fill="x", pady=(0, 8))

                tk.Label(
                    card,
                    text=f"{nome}\nR$ {preco:.2f}",
                    font=FONTE_ITEM,
                    bg=self.cores["card"],
                    fg=self.cores["subtitulo"],
                    justify="left"
                ).pack(anchor="w")

                tk.Label(
                    card, text=descricao,
                    font=FONTE_DESC,
                    bg=self.cores["card"],
                    fg=self.cores["texto"],
                    wraplength=260, justify="left"
                ).pack(anchor="w", pady=(4, 8))

                controle = tk.Frame(
                    card, bg=self.cores["card"]
                )
                controle.pack(fill="x")

                tk.Label(
                    controle, text="Quantidade:",
                    bg=self.cores["card"],
                    fg=self.cores["texto"]
                ).pack(side="left")

                spin = tk.Spinbox(
                    controle, from_=0, to=99, width=4,
                    font=FONTE_ITEM,
                    bg=self.cores["entry_bg"],
                    fg=self.cores["entry_fg"],
                    buttonbackground=self.cores["acento"],
                    justify="center",
                    command=self.atualizar_total
                )
                spin.pack(side="right")

                spin.bind(
                    "<KeyRelease>",
                    lambda event: self.atualizar_total()
                )

                self.pedidos[nome] = (spin, preco)

    # ===================== TOTAL =====================

    def atualizar_total(self):
        if not hasattr(self, "lbl_total"):
            return

        total = 0

        for spin, preco in self.pedidos.values():
            try:
                quantidade = int(spin.get())
                total += quantidade * preco
            except ValueError:
                pass

        self.lbl_total.config(
            text=f"TOTAL: R$ {total:.2f}"
        )

    # ===================== FINALIZAR PEDIDO =====================

    def finalizar_pedido(self):
        itens_selecionados = []
        total = 0

        for nome, (spin, preco) in self.pedidos.items():
            try:
                quantidade = int(spin.get())
            except ValueError:
                quantidade = 0

            if quantidade > 0:
                subtotal = quantidade * preco
                total += subtotal

                itens_selecionados.append({
                    "item": nome,
                    "quantidade": quantidade,
                    "preco_unitario": preco,
                    "subtotal": round(subtotal, 2)
                })

        if not itens_selecionados:
            messagebox.showwarning(
                "Pedido",
                "Selecione pelo menos um produto."
            )
            return

        pedido = {
            "id_pedido": int(datetime.now().timestamp()),
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": {
                "nome": self.dados_cliente["nome"],
                "usuario": self.dados_cliente["usuario"],
                "forma_pagamento": self.dados_cliente["pagamento"]
            },
            "itens": itens_selecionados,
            "total": round(total, 2)
        }

        registrar_pedido(pedido)

        resumo = (
            "✅ PEDIDO FINALIZADO!\n\n"
            f"Cliente: {self.dados_cliente['nome']}\n"
            f"Pagamento: {self.dados_cliente['pagamento']}\n\n"
        )

        for item in itens_selecionados:
            resumo += (
                f"{item['quantidade']}x {item['item']} "
                f"= R$ {item['subtotal']:.2f}\n"
            )

        resumo += (
            f"\nTOTAL: R$ {total:.2f}\n\n"
            "Pedido salvo automaticamente."
        )

        messagebox.showinfo(
            "Pedido realizado!",
            resumo
        )

        self.mostrar_tela_cardapio()


# ===================== INICIAR =====================

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGourmetApp(root)
    root.mainloop()
