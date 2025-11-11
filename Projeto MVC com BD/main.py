from core.models import StudentModel
from core.view import StudentView
from core.controller import StudentController
from core.login_view import LoginView
import customtkinter as ctk
import sys

# Define o tema da interface
ctk.set_appearance_mode("light")  # Aparência da interface
ctk.set_default_color_theme("blue")  # Cor dos botões


class App:
    def __init__(self):
        self.model = None
        self.controller = None
        self.main_view = None
        self.login_view = None

    # Função chamada após o login ser bem-sucedido.
    def start_main_app(self):
        print("Login bem-sucedido. Iniciando aplicação principal...")

        # Inicia o Model
        self.model = StudentModel()

        # Inicia o Controller (e passa o model para ele)
        self.controller = StudentController(self.model)

        # Inicia a View principal (a tela do CRUD)
        self.main_view = StudentView(self.controller)

        # Garante que a conexão com o BD seja fechada ao fechar a janela
        self.main_view.protocol("WM_DELETE_WINDOW", self.on_closing_main_app)

        # Inicia o loop da interface principal
        self.main_view.mainloop()

    # Função chamada ao fechar a interface principal
    def on_closing_main_app(self):
        print("Fechando conexão com o banco de dados...")
        if self.model:
            self.model.close_connection()
        if self.main_view:
            self.main_view.destroy()
        sys.exit()

    # Função chamada se o usuário fechar a janela de login.
    def on_login_close(self):
        print("Login cancelado. Encerrando.")
        if self.login_view:
            self.login_view.destroy()
        sys.exit()  # Termina o programa

    # Inicia o projeto
    def run(self):
        # 1. Cria a LoginView
        # 2. Passa a função 'start_main_app' como o callback de sucesso
        self.login_view = LoginView(on_login_success_callback=self.start_main_app)

        # Define o que acontece se o usuário fechar a janela de login no 'X'
        self.login_view.protocol("WM_DELETE_WINDOW", self.on_login_close)

        # 3. Inicia o loop do login
        self.login_view.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()