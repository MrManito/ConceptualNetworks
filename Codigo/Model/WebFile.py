from abc import ABC
from Codigo.Model.File import File
import requests, random, string
from bs4 import BeautifulSoup
import re

def generar_nombre_aleatorio(longitud):
    caracteres = string.ascii_letters + string.digits
    nombre_aleatorio = ''.join(random.choice(caracteres) for _ in range(longitud))
    return nombre_aleatorio

class WebFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        try:
            # Se obtiene la pagina web
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(self.name, headers=headers)
            response.raise_for_status()
            html = response.text
            page = BeautifulSoup(html, 'html.parser')
            for script in page(['script', 'style']):
                script.extract()

            #name_txt = page.title.string.replace(' ', '_')
            self.url_file = generar_nombre_aleatorio(10) + ".txt"
            text = page.get_text()
            pattern = r'[a-zA-ZáéíóúüÑÁÉÍÓÚÜñ]+'
            letters = re.findall(pattern, text)
            text = "\n".join(letters)

            # Se crea el archivo .txt y se guarda con la información de la página
            with open(self.path + self.url_file, "w", encoding="utf-8") as f:
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
        except requests.exceptions.RequestException as e:
            return {
                'response': True,
                'message': f"{e}",
            }
        except Exception as e:
            return {
                'response': True,
                'message': "Error: No se logró cargar el archivo.",
            }
