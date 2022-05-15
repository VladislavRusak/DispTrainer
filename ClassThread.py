import sys
import os
import urllib
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ReportsThread(QThread):
    mysignal = pyqtSignal(QImage, str)
    def __init__(self, data):
        super().__init__()
        
        self.data = data
    
    def __del__(self):
        self.wait()
    
    def getImage(self, report):
        url = report['cover']['generated_image_path']
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.abspath(os.path.join(dir_path, os.pardir))
        directory = dir + '\\files\\albums'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        album_dir = dir + '\\files\\albums\\' + report['album_id']
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)
        
        my_file = Path(album_dir + '\\' + report['cover']['photo_id'] + '.jpg')
        if my_file.is_file(): 
            with open(album_dir + '\\' + report['cover']['photo_id'] + '.jpg', 'rb') as f:
                content = f.read()

            img = QImage()

            img.loadFromData(content)
        else:
            data = urllib.request.urlopen(url)
            img_data = data.read()
            img = QImage()
            img.loadFromData(img_data)
            img.save(album_dir + '\\' + report['cover']['photo_id'] + '.jpg')
        return img
    
    def run(self):
        for report in self.data:
            img_data = self.getImage(report)
            self.mysignal.emit(img_data, report['album_id'] + '')
            
            

            
class STr(QThread):
    def __init__(self, data):
        super().__init__()
        
        
class ReportThread(QThread):
    mysignal = pyqtSignal(QImage, str)
    def __init__(self, data):
        super().__init__()

        self.data = data

    def __del__(self):
        self.wait()

    def getImage(self, photo):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.abspath(os.path.join(dir_path, os.pardir))
        directory = dir + '\\files\\albums\\' + photo['album_id']
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory = directory + '\\thumbs'
        if not os.path.exists(directory):
            os.makedirs(directory)

        my_file = Path(directory + '\\' + photo['photo_id'] + '.jpg')
        if my_file.is_file():
            with open(directory + '\\' + photo['photo_id'] + '.jpg', 'rb') as f:
                content = f.read()

            img = QImage()

            img.loadFromData(content)
        else:
            url = photo['mini_path']
            data = urllib.request.urlopen(url)
            img_data = data.read()
            img = QImage()
            img.loadFromData(img_data)
            img.save(directory + '\\' + photo['photo_id'] + '.jpg')
        return img

    def run(self):
        for photo in self.data:
            img_data = self.getImage(photo)
            self.mysignal.emit(img_data, photo['photo_id'] + '')