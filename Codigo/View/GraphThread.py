# PyQt6 dependencies
from PyQt6.QtCore import QThread, pyqtSignal

import time

# Class that create a thread to process the files
class GraphThread(QThread):

    finished = pyqtSignal()
    update_signal = pyqtSignal(str, float)
    error_signal = pyqtSignal(str)
    def __init__(self, file_list, main_controller):
        super().__init__()
        self.file_list = file_list
        self.main_controller = main_controller

    def run(self):
        self.main_controller.cleanText()
        count = 1
        fileCount = self.file_list.count()
        for i in range(fileCount):
            item = self.file_list.item(i)

            response = self.main_controller.addFiles(item.text())
            if response['response']:
                self.error_signal.emit(f"ERROR: {response['message']} in element {item.text()}")
                time.sleep(5)
            self.update_signal.emit(f"Finalizado: {item.text()}", (count/fileCount)*100)
            count +=1
            #time.sleep(1)

        self.main_controller.textAnalysis()
        self.finished.emit()