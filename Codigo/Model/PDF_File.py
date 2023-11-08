import re

from pdfminer.high_level import extract_text
from abc import ABC
from Codigo.Model.File import File


def replace(match):
    vocal = match.group(1)
    if vocal == 'a':
        return 'á'
    elif vocal == 'e':
        return 'é'
    elif vocal == 'ı':
        return 'í'
    elif vocal == 'o':
        return 'ó'
    elif vocal == 'u':
        return 'ú'


def replace2(match):
    vocal = match.group(1)
    if vocal == 'a':
        return 'ä'
    elif vocal == 'e':
        return 'ë'
    elif vocal == 'ı':
        return 'ï'
    elif vocal == 'o':
        return 'ö'
    elif vocal == 'u':
        return 'ü'


def modifyText(text):
    # Método para documentos generados en Látex

    pattern = r'´([aeıou])'
    text = re.sub(pattern, replace, text)

    pattern2 = r'¨([aeıou])'
    text = re.sub(pattern2, replace2, text)

    pattern4 = r'˜([n])'
    text = re.sub(pattern4, "ñ", text)

    text = text.replace("-\n", "")
    text = text.replace("", "")

    return text


class PDFFile(File, ABC):

    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        try:
            text = extract_text(self.url_file, codec=' utf8').lower()
            text = modifyText(text)

            # Escribe el texto en un archivo de texto
            path = self.path + self.name + ".txt"
            with open(path, "w", encoding="utf8") as f:
                f.write(text)
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
                'message': f"Error: No se logró cargar el archivo.{e}",
            }


#x = PDFFile("1", "1.pdf")
#x = PDFFile("2", "2.pdf")
#x = PDFFile("3", "3.pdf")
#print(x.get_text())
