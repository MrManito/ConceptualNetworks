from abc import abstractmethod
from abc import ABCMeta

class File(metaclass=ABCMeta):

    def __init__(self, name, url_file):
        self.name = name
        self.url_file = url_file
        self.path = ""
        #self.path = "../../Txts/"

    @abstractmethod
    def get_text(self):
        pass
