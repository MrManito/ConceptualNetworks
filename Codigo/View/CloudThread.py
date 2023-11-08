# PyQt6 dependencies
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib import pyplot as plt
from wordcloud import WordCloud

import os
# Class that create a thread to process the files
class CloudThread(QThread):

    finished = pyqtSignal()

    def __init__(self, cloud_parameters, main_controller, num_func_words):
        super().__init__()
        self.num_func_words = num_func_words
        self.cloud_parameters = cloud_parameters
        self.main_controller = main_controller

    def run(self):
        cloud = self.main_controller.get_cloud_words(self.num_func_words)
        try:
            wordcloud = WordCloud(**self.cloud_parameters).generate_from_frequencies(cloud)

            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            # Save temporality the cloud in a png then is show it
            path = os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks'))
            plt.savefig(path + "/wordcloud.png", bbox_inches='tight', pad_inches=0, transparent=True)
            self.finished.emit()

        except Exception as e:
            print(e)