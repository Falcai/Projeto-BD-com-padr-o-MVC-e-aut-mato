import sqlite3  # Caso ocorra erros específicos relacionados ao sqlite

class StudentController:
    def __init__(self, model):
        self.model = model

    def add_student(self, nome, idade_str, ra_str):
        try:
            idade_int = int(idade_str)
            if idade_int <= 0:
                raise ValueError("Idade deve ser um número positivo.")

            # O model fará a validação do RA e do BD
            self.model.add_student(nome, idade_int, ra_str)

        except ValueError as e:
            # Repassa o erro (de int() ou do model) para a View
            raise e
        except sqlite3.Error as e:
            # Trata erros específicos do banco
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O RA '{ra_str}' já está cadastrado.")
            else:
                raise e  # Repassa outros erros do BD

    def get_all_students(self):
        return self.model.get_all_students()

    def delete_student(self, index_str):
        try:
            index_int = int(index_str)
            self.model.delete_student(index_int)
        except ValueError as e:
            # Repassa o erro (de int() ou do model)
            raise ValueError(f"ID '{index_str}' inválido. {e}")

    def update_student(self, nome, idade_str, ra_str, index_str):
        try:
            idade_int = int(idade_str)
            index_int = int(index_str)
            if idade_int <= 0:
                raise ValueError("Idade deve ser um número positivo.")

            self.model.update_student(nome, idade_int, ra_str, index_int)

        except ValueError as e:
            # Repassa o erro (de int() ou do model)
            raise e
        except sqlite3.Error as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O RA '{ra_str}' já está cadastrado.")
            else:
                raise e