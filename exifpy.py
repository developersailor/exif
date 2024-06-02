import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ExifTags import TAGS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EXIF Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.display_image(file_path)
                self.display_exif_data(file_path)
        else:
            event.ignore()

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def display_exif_data(self, file_path):
        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data:
                exif_text = ""
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    exif_text += f"{tag_name}: {value}\n"
                self.text_edit.setText(exif_text)
            else:
                self.text_edit.setText("EXIF verisi bulunamadı.")
        except Exception as e:
            self.text_edit.setText(f"Bir hata oluştu: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()