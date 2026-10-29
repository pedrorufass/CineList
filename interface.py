import tkinter as tk
from tkinter import ttk, messagebox

import database
import cache


class CineListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CineList")
        self.geometry("850x650")
        self.minsize(760, 560)
        self.configure(bg="#f4f4f4")

        self.filmes = []
        self.fonte = ""

        self.criar_estilo()
        self.criar_interface()
        self.carregar_filmes()

    def criar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Arial", 10),
            padding=8
        )

        style.configure(
            "Primary.TButton",
            font=("Arial", 10, "bold"),
            padding=9
        )

        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=34
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def criar_interface(self):
        titulo = tk.Label(
            self,
            text="CINELIST",
            font=("Arial", 11, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        )
        titulo.pack(anchor="w", padx=35, pady=(28, 2))

        subtitulo = tk.Label(
            self,
            text="Minha lista de filmes",
            font=("Arial", 25, "bold"),
            bg="#f4f4f4",
            fg="#171717"
        )
        subtitulo.pack(anchor="w", padx=35)

        descricao = tk.Label(
            self,
            text="Organize os filmes que você quer assistir ou já assistiu.",
            font=("Arial", 11),
            bg="#f4f4f4",
            fg="#666666"
        )
        descricao.pack(anchor="w", padx=35, pady=(4, 22))

        formulario = tk.Frame(self, bg="white", highlightbackground="#dddddd", highlightthickness=1)
        formulario.pack(fill="x", padx=35)

        tk.Label(formulario, text="Título", bg="white", fg="#333333", font=("Arial", 9, "bold")).grid(
            row=0, column=0, padx=(18, 8), pady=(16, 5), sticky="w"
        )
        tk.Label(formulario, text="Gênero", bg="white", fg="#333333", font=("Arial", 9, "bold")).grid(
            row=0, column=1, padx=8, pady=(16, 5), sticky="w"
        )
        tk.Label(formulario, text="Ano", bg="white", fg="#333333", font=("Arial", 9, "bold")).grid(
            row=0, column=2, padx=8, pady=(16, 5), sticky="w"
        )

        self.titulo_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.ano_var = tk.StringVar()

        self.titulo_entry = ttk.Entry(formulario, textvariable=self.titulo_var)
        self.genero_entry = ttk.Entry(formulario, textvariable=self.genero_var)
        self.ano_entry = ttk.Entry(formulario, textvariable=self.ano_var)

        self.titulo_entry.grid(row=1, column=0, padx=(18, 8), pady=(0, 18), sticky="ew")
        self.genero_entry.grid(row=1, column=1, padx=8, pady=(0, 18), sticky="ew")
        self.ano_entry.grid(row=1, column=2, padx=8, pady=(0, 18), sticky="ew")

        botao = ttk.Button(
            formulario,
            text="Adicionar filme",
            style="Primary.TButton",
            command=self.adicionar
        )
        botao.grid(row=1, column=3, padx=(8, 18), pady=(0, 18))

        formulario.columnconfigure(0, weight=4)
        formulario.columnconfigure(1, weight=3)
        formulario.columnconfigure(2, weight=1)

        barra = tk.Frame(self, bg="#f4f4f4")
        barra.pack(fill="x", padx=35, pady=(20, 10))

        tk.Label(
            barra,
            text="Pesquisar:",
            bg="#f4f4f4",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.pesquisa_var = tk.StringVar()
        self.pesquisa_var.trace_add("write", lambda *_: self.atualizar_tabela())

        ttk.Entry(
            barra,
            textvariable=self.pesquisa_var,
            width=35
        ).pack(side="left", padx=8)

        self.fonte_label = tk.Label(
            barra,
            text="",
            bg="#f4f4f4",
            fg="#555555",
            font=("Arial", 9)
        )
        self.fonte_label.pack(side="right")

        tabela_frame = tk.Frame(self, bg="#f4f4f4")
        tabela_frame.pack(fill="both", expand=True, padx=35)

        colunas = ("id", "title", "genre", "year", "watched")

        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("title", text="Título")
        self.tabela.heading("genre", text="Gênero")
        self.tabela.heading("year", text="Ano")
        self.tabela.heading("watched", text="Status")

        self.tabela.column("id", width=45, anchor="center")
        self.tabela.column("title", width=300)
        self.tabela.column("genre", width=180)
        self.tabela.column("year", width=70, anchor="center")
        self.tabela.column("watched", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela.yview
        )
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        botoes = tk.Frame(self, bg="#f4f4f4")
        botoes.pack(fill="x", padx=35, pady=15)

        ttk.Button(
            botoes,
            text="Marcar / desmarcar assistido",
            command=self.alternar_assistido
        ).pack(side="left")

        ttk.Button(
            botoes,
            text="Excluir selecionado",
            command=self.excluir
        ).pack(side="left", padx=8)

        ttk.Button(
            botoes,
            text="Atualizar lista",
            command=self.carregar_filmes
        ).pack(side="right")

    def carregar_filmes(self):
        try:
            filmes_cache = cache.buscar_cache()

            if filmes_cache is not None:
                self.filmes = filmes_cache
                self.fonte = "Redis"
            else:
                self.filmes = database.listar_filmes()
                cache.salvar_cache(self.filmes)
                self.fonte = "Supabase"

            self.fonte_label.config(text=f"Fonte dos dados: {self.fonte}")
            self.atualizar_tabela()

        except Exception as error:
            messagebox.showerror("Erro", str(error))

    def atualizar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        termo = self.pesquisa_var.get().strip().lower()

        for filme in self.filmes:
            if (
                termo in filme["title"].lower()
                or termo in filme["genre"].lower()
            ):
                status = "Assistido" if filme["watched"] else "Não assistido"

                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        filme["id"],
                        filme["title"],
                        filme["genre"],
                        filme["year"],
                        status
                    )
                )

    def adicionar(self):
        titulo = self.titulo_var.get().strip()
        genero = self.genero_var.get().strip()
        ano = self.ano_var.get().strip()

        if not titulo or not genero or not ano:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        if not ano.isdigit():
            messagebox.showwarning("Atenção", "O ano deve ser um número.")
            return

        try:
            ano_numero = int(ano)

            if ano_numero < 1888 or ano_numero > 2100:
                messagebox.showwarning("Atenção", "Digite um ano válido.")
                return

            database.adicionar_filme(titulo, genero, ano_numero)
            cache.limpar_cache()

            self.titulo_var.set("")
            self.genero_var.set("")
            self.ano_var.set("")

            self.carregar_filmes()

        except Exception as error:
            messagebox.showerror("Erro", str(error))

    def selecionar_id(self):
        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um filme.")
            return None

        valores = self.tabela.item(selecionado[0], "values")
        return int(valores[0])

    def encontrar_filme(self, movie_id):
        for filme in self.filmes:
            if filme["id"] == movie_id:
                return filme
        return None

    def alternar_assistido(self):
        movie_id = self.selecionar_id()

        if movie_id is None:
            return

        filme = self.encontrar_filme(movie_id)

        if filme is None:
            return

        try:
            database.atualizar_assistido(movie_id, not filme["watched"])
            cache.limpar_cache()
            self.carregar_filmes()

        except Exception as error:
            messagebox.showerror("Erro", str(error))

    def excluir(self):
        movie_id = self.selecionar_id()

        if movie_id is None:
            return

        filme = self.encontrar_filme(movie_id)

        if filme is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f'Deseja excluir "{filme["title"]}"?'
        )

        if not confirmar:
            return

        try:
            database.excluir_filme(movie_id)
            cache.limpar_cache()
            self.carregar_filmes()

        except Exception as error:
            messagebox.showerror("Erro", str(error))
