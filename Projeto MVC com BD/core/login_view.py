import customtkinter as ctk
import customtkinter.windows.widgets.font as ctk_font

class LoginAutomaton:

    def __init__(self):
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'}
        self.estado_inicial = 'q0'
        # O único estado final (aceitação) é 'q_accept'
        self.estados_finais = {'q_accept'}
        self.estado_atual = self.estado_inicial

    def reset(self):
        self.estado_atual = self.estado_inicial

    def transicao(self, char):
        estado = self.estado_atual

        if estado == 'q0':
            self.estado_atual = 'q1' if char == '0' else 'q_reject'
        elif estado == 'q1':
            self.estado_atual = 'q2' if char == '5' else 'q_reject'
        elif estado == 'q2':
            self.estado_atual = 'q3' if char == '2' else 'q_reject'
        elif estado == 'q3':
            self.estado_atual = 'q4' if char == '2' else 'q_reject'
        elif estado == 'q4':
            self.estado_atual = 'q_accept' if char == '2' else 'q_reject'
        elif estado == 'q_accept':
            # Se já aceitou (começa com "05222"), qualquer outro caractere mantém no estado de aceitação.
            self.estado_atual = 'q_accept'
        elif estado == 'q_reject':
            # Se já rejeitou, permanece no estado de rejeição (trap).
            self.estado_atual = 'q_reject'

    # Verifica a permissão processando a string inteira no autômato.
    def check_permission(self, ra_string):
        self.reset()

        for char in ra_string:
            self.transicao(char)
            if self.estado_atual == 'q_reject':
                return False

    # Após processar a string, verifica se o estado final é um de aceitação.
        return self.estado_atual in self.estados_finais

    # A janela de Login que aparece antes da interface principal.
class LoginView(ctk.CTk):

    def __init__(self, on_login_success_callback):
        super().__init__()

        # Callback: A função que deve ser chamada se o login for bem-sucedido
        self.on_login_success = on_login_success_callback

        # Instancia o autômato de verificação
        self.automaton = LoginAutomaton()

        self.title("Login - Acesso ao Sistema")
        self.geometry("400x250")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Acesso Restrito", font=ctk_font.CTkFont(size=20, weight="bold")).grid(row=0, column=0,
                                                                                                       pady=20, padx=10,
                                                                                                       sticky="n")

        self.ra_entry = ctk.CTkEntry(self, placeholder_text="Digite seu RA para permissão...", width=250)
        self.ra_entry.grid(row=1, column=0, pady=10, padx=10)
        # Permite apertar "Enter" para tentar o login
        self.ra_entry.bind("<Return>", self.attempt_login)

        self.login_button = ctk.CTkButton(self, text="Entrar", command=self.attempt_login)
        self.login_button.grid(row=2, column=0, pady=10, padx=10, sticky="n")

        self.log_label = ctk.CTkLabel(self, text="", text_color="darkred", font=ctk_font.CTkFont(weight="bold"))
        self.log_label.grid(row=3, column=0, pady=10, padx=10, sticky="s")

        # Centraliza a janela
        self.after(100, lambda: self.center_window)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    # Pega o RA digitado e usa autômato para verificar
    def attempt_login(self, event=None):
        ra = self.ra_entry.get()

        if self.automaton.check_permission(ra):
            # SUCESSO
            self.log_label.configure(text="")
            self.destroy()
            self.on_login_success()
        else:
            # ERRO
            self.log_label.configure(text="Erro: Aluno não possui permissão.")