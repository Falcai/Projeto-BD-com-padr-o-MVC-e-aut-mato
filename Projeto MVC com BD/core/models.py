import sqlite3
import re

class StudentModel:
    def __init__(self):
        self.conn = sqlite3.connect('alunos.db')
        self.ra_validate = re.compile(r'^05\d{3}0\d{2}$') # Definindo a regra do autômato
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL,
                    ra TEXT NOT NULL UNIQUE 
            )
            '''
                       )
        self.conn.commit()

    # Validação da entrada que o usuário fez no RA
    def validar_ra(self, ra):
        if not isinstance(ra, str) or not self.ra_validate.match(ra):
            return False
        return True

    # Verifica os dados digitados e adiciona o Aluno no BD
    def add_student(self, nome, idade, ra):
        ra = str(ra)
        if not self.validar_ra(ra):
            # erro para a View capturar
            raise ValueError(f"RA '{ra}' inválido. Padrão: 05XXX0XX.")

        # Deixa o try/except para o controller/view
        # Erros de 'UNIQUE constraint' serão levantados daqui
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO alunos (nome, idade, ra) VALUES (?,?,?)', (nome, idade, ra))
        self.conn.commit()

    # Verifica o ID digitado e remove o Aluno do BD
    def delete_student(self, index):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM alunos WHERE id = ?', (index,))
        if cursor.rowcount == 0:
            # erro caso ID não encontrado
            raise ValueError(f"ID {index} não encontrado.")
        self.conn.commit()

    # Verifica se o ID é existente e se os dados estão corretos e atualiza o Aluno desejado
    def update_student(self, nome, idade, ra, index):
        ra = str(ra)
        if not self.validar_ra(ra):
            # erro para a View capturar
            raise ValueError(f"RA '{ra}' inválido. Padrão: 05XXX0XX.")

        cursor = self.conn.cursor()
        cursor.execute('UPDATE alunos SET nome = ?, idade = ?, ra = ? WHERE id = ?', (nome, idade, ra, index))
        if cursor.rowcount == 0:
            # erro caso ID não encontrado
            raise ValueError(f"ID {index} não encontrado para atualização.")
        self.conn.commit()

    # Apresenta todos os Alunos já registrados no BD
    def get_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM alunos')
        return cursor.fetchall()

    # Encerra a conexão
    def close_connection(self):
        self.conn.close()