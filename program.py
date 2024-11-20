import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
import math
from PIL import Image
from PIL import Image, ImageDraw
import numpy as np

class MainApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_user_interface()

   
    
    def save_plot_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', 
                                                   '', 
                                                   'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.plot_figure.savefig(file_name)

    def load_image_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', 
                                                   '', 
                                                   'Images (*.png *.xpm *.jpg *.bmp)')
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_display_label.setPixmap(pixmap)

    def generate_plot(self):
        x = range(0, 20)
        y = [math.exp(i) for i in x]
    
        self.plot_figure.clear()
        ax = self.plot_figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        image_path = self.image_display_label.pixmap().toImage().save('image.png')
        img = Image.open('image.png')
        width, height = img.size
        cropped_img = img.crop((width // 4, height // 4, width // 1.33, height // 1.33))
        arr = np.array(cropped_img)
        image = OffsetImage(arr, zoom=0.5)
        ab = AnnotationBbox(image, (10, 80000000), frameon=False)
        ax.add_artist(ab)
    
        self.plot_canvas.draw()

    def initialize_user_interface(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Лабораторная 7')
        
        self.setStyleSheet("background-color: white;")  # Установить цвет фона окна
        
        self.left_side_layout = QVBoxLayout()
        self.right_side_layout = QVBoxLayout()
        
        self.load_image_button = QPushButton('Открыть изображение')
        self.load_image_button.clicked.connect(self.load_image_from_file)
        self.load_image_button.setStyleSheet("background-color: white; color: gray;")  # Установить цвет фона кнопки и текста
        
        self.image_display_label = QLabel()
        self.image_display_label.setStyleSheet("background-color: white;")  # Установить цвет фона метки
        
        self.button_layout = QHBoxLayout()  # Создать горизонтальный макет для кнопок
        
        self.generate_plot_button = QPushButton('Создать график')
        self.generate_plot_button.clicked.connect(self.generate_plot)
        self.generate_plot_button.setStyleSheet("background-color: white; color: gray;")  # Установить цвет фона кнопки и текста
        
        self.save_plot_button = QPushButton('Сохранить график')
        self.save_plot_button.clicked.connect(self.save_plot_to_file)
        self.save_plot_button.setStyleSheet("background-color: white; color: gray;")  # Установить цвет фона кнопки и текста
        
        self.button_layout.addWidget(self.generate_plot_button)  # Добавить кнопку "Создать график" в горизонтальный макет
        self.button_layout.addWidget(self.save_plot_button)  # Добавить кнопку "Сохранить график" в горизонтальный макет
        
        self.plot_figure = plt.figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        
        self.left_side_layout.addWidget(self.load_image_button)
        self.left_side_layout.addWidget(self.image_display_label)
        
        self.right_side_layout.addLayout(self.button_layout)  # Добавить горизонтальный макет с кнопками в вертикальный макет
        self.right_side_layout.addWidget(self.plot_canvas)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.left_side_layout)
        main_layout.addLayout(self.right_side_layout)
        
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApplicationWindow()
    window.show()
    sys.exit(app.exec_())