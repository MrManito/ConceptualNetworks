from abc import ABC
from Codigo.Model.File import File

class TextFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        path = self.path + self.name + ".txt"
        try:
            with open(self.url_file, 'r', encoding="utf8") as input_file:
                # Lee el contenido del archivo de entrada
                text = input_file.read()

            with open(path, 'w', encoding="utf8") as output_file:
                # Escribe el contenido en el archivo de salida
                output_file.write(text)

            return {
                'response': False,
                'message': text,

            }
        except FileNotFoundError as e:
            return {
                'response': True,
                'message': f"Error: El archivo {self.url_file} no se encontró.",
            }
        except Exception as e:
            return {
                'response': True,
                'message': f"Error: No se logró cargar el archivo. {e}",
            }

