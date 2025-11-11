import customtkinter as ctk
import customtkinter.windows.widgets.font as ctk_font

class StudentView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("Cadastro de Alunos")
        self.geometry("800x900")

       # Adicionar Aluno
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(pady=5, padx=5, fill="x")

        ctk.CTkLabel(add_frame, text="Adicionar Aluno").pack(pady=2)
        self.name_entry = ctk.CTkEntry(add_frame, placeholder_text='Nome do Aluno...')
        self.name_entry.pack(pady=5, padx=5)
        self.age_entry = ctk.CTkEntry(add_frame, placeholder_text='Idade...')
        self.age_entry.pack(pady=5, padx=5)
        self.ra_entry = ctk.CTkEntry(add_frame, placeholder_text='RA (Ex: 05123045)...')
        self.ra_entry.pack(pady=5, padx=5)
        self.add_button = ctk.CTkButton(add_frame, text='Adicionar aluno', command=self.add_student)
        self.add_button.pack(pady=5, padx=5)

        # Atualizar Aluno
        update_frame = ctk.CTkFrame(self)
        update_frame.pack(pady=5, padx=5, fill="x")

        ctk.CTkLabel(update_frame, text="Atualizar Aluno").pack(pady=2)
        self.id_update_entry = ctk.CTkEntry(update_frame, placeholder_text='Id p/ editar...')
        self.id_update_entry.pack(pady=5, padx=5)
        self.name_update_entry = ctk.CTkEntry(update_frame, placeholder_text='Novo Nome...')
        self.name_update_entry.pack(pady=5, padx=5)
        self.age_update_entry = ctk.CTkEntry(update_frame, placeholder_text='Nova Idade...')
        self.age_update_entry.pack(pady=5, padx=5)
        self.ra_update_entry = ctk.CTkEntry(update_frame, placeholder_text='Novo RA...')
        self.ra_update_entry.pack(pady=5, padx=5)
        self.update_button = ctk.CTkButton(update_frame, text='Atualizar aluno', command=self.update_student)
        self.update_button.pack(pady=10, padx=5)

        # Remover Aluno
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(pady=5, padx=5, fill="x")

        ctk.CTkLabel(delete_frame, text="Apagar Aluno").pack(pady=2)
        self.id_delete_entry = ctk.CTkEntry(delete_frame, placeholder_text='Id p/ apagar...')
        self.id_delete_entry.pack(pady=5, padx=5)
        self.delete_button = ctk.CTkButton(delete_frame, text='Apagar aluno', command=self.delete_student)
        self.delete_button.pack(pady=5, padx=5)

        # Apresenta a lista de Alunos
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.load_button = ctk.CTkButton(list_frame, text='Carregar alunos na tabela', command=self.load_student)
        self.load_button.pack(pady=5)
        self.name_table = ctk.CTkLabel(list_frame,text='Tabela de Alunos:').place(x=10,y=20)
        self.student_list = ctk.CTkTextbox(list_frame, width=500, height=60)
        self.student_list.pack(pady=5, padx=5, fill="both", expand=True)

        # LOG que informa as atualizações feitas ou erros
        self.log_label = ctk.CTkLabel(self, text="", text_color="white", font=ctk_font.CTkFont(weight="bold"))
        self.log_label.pack(pady=5, padx=5, fill="x")

        # Carrega os alunos ao iniciar
        self.load_student()
        # Limpa a mensagem do LOG ao iniciar a app pela primeira vez
        self.show_message("")

    # Atualiza o log_label com uma mensagem de sucesso (verde) ou erro (vermelho)
    def show_message(self, message, is_error=False):
        if is_error:
            self.log_label.configure(text=message, text_color="darkred")  # Vermelho
        else:
            self.log_label.configure(text=message, text_color="darkgreen")  # Verde

    # Limpa os campos de 'Adicionar'
    def clear_add_fields(self):
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.ra_entry.delete(0, "end")

    # Limpa os campos de 'Atualizar'
    def clear_update_fields(self):
        self.id_update_entry.delete(0, "end")
        self.name_update_entry.delete(0, "end")
        self.age_update_entry.delete(0, "end")
        self.ra_update_entry.delete(0, "end")

    # Adiciona o Aluno e verifica se todos os campos foram preenchidos
    def add_student(self):
        try:
            nome = self.name_entry.get()
            idade = self.age_entry.get()
            ra = self.ra_entry.get()

            if not nome or not idade or not ra:
                raise ValueError("Todos os campos de 'Adicionar Aluno' são obrigatórios.")

            self.controller.add_student(nome, idade, ra)

            self.show_message("Aluno adicionado com sucesso!", is_error=False)
            self.load_student()
            self.clear_add_fields()

        except Exception as e:
            self.show_message(f"Erro: {e}", is_error=True)

    # Carrega todos os alunos na interface
    def load_student(self):
        try:
            alunos = self.controller.get_all_students()
            self.student_list.delete(1.0, "end")
            if not alunos:
                self.student_list.insert("end", "Nenhum aluno cadastrado.")

            for aluno in alunos:
                self.student_list.insert("end",
                                         f"ID: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | RA: {aluno[3]}\n")
        except Exception as e:
            self.show_message(f"Erro ao carregar alunos: {e}", is_error=True)

    # Apaga o Aluno pelo ID informado
    def delete_student(self):
        try:
            index = self.id_delete_entry.get()

            if not index:
                raise ValueError("O campo 'Id p/ apagar...' é obrigatório.")

            self.controller.delete_student(index)

            self.show_message("Aluno apagado com sucesso!", is_error=False)
            self.load_student()
            self.id_delete_entry.delete(0, "end")

        except Exception as e:
            self.show_message(f"Erro ao apagar: {e}", is_error=True)

    # Atualiza o Aluno pelo ID informado e verifica se todos os campos foram preenchidos
    def update_student(self):
        try:
            index = self.id_update_entry.get()
            nome = self.name_update_entry.get()
            idade = self.age_update_entry.get()
            ra = self.ra_update_entry.get()

            if not index or not nome or not idade or not ra:
                raise ValueError("Todos os campos de 'Atualizar Aluno' são obrigatórios.")

            self.controller.update_student(nome, idade, ra, index)

            self.show_message("Aluno atualizado com sucesso!", is_error=False)
            self.load_student()
            self.clear_update_fields()

        except Exception as e:
            self.show_message(f"Erro ao atualizar: {e}", is_error=True)