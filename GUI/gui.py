import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QStackedWidget, QProgressBar, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer

# Custom stylesheet for the application
stylesheet = """QWidget {
    background-color: #F2F4F5;
    color: #000000;
}
QPushButton {
    background-color: #005EBD;
    color: white;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #111111;
    font-family: Arial;  /* Change this to your desired font family */
    font-size: 16px;     /* Change this to your desired font size */
}
QPushButton:hover {
    background-color: #004A94;
}
QPushButton:pressed {
    background-color: #00376B;
}

#image_button {
    background-color: #e63946;
    color: white;
}

#video_button {
    background-color: #e63946;
    color: white;
}

#about_button {
    background-color: #e63946;
    color: white;
}

QLabel {
    font-size: 34px;
    color: white;
    background-color: #d9d9d9;
    border-radius: 10px;  /* Add border radius */
    padding: 5px; /* Optional: Add some padding */
}
QProgressBar {
    background-color: #1e1e1e;
    border-radius: 5px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    width: 20px;
}
QVideoWidget {
    border: 1px solid #005EBD;
}

"""


class MainPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Background image
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap('mainpage.png'))
        self.background_label.setScaledContents(True)  # Ensures the image is scaled to fit the label
        self.background_label.setGeometry(0, 0, 1366, 768)  # Adjust according to your window size

        # Image button
        self.image_button = QPushButton('Image', self)
        self.image_button.setObjectName("image_button")
        self.image_button.setGeometry(230, 400, 200, 50)  # Set position and size
        self.image_button.clicked.connect(self.show_image_page)

        # Video button
        self.video_button = QPushButton('Video', self)
        self.video_button.setObjectName("video_button")
        self.video_button.setGeometry(230, 500, 200, 50)  # Set position and size
        self.video_button.clicked.connect(self.show_video_page)

        # About button
        self.about_button = QPushButton('About', self)
        self.about_button.setObjectName("about_button")
        self.about_button.setGeometry(230, 600, 200, 50)  # Set position and size
        self.about_button.clicked.connect(self.show_about_page)

    def show_image_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_video_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_about_page(self):
        self.stacked_widget.setCurrentIndex(3)


class ImagePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.show_main_page)
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        layout.addLayout(top_layout)

        before_after_layout = QHBoxLayout()
        before_layout = QVBoxLayout()
        self.before_label = QLabel('Before')
        self.before_label.setAlignment(Qt.AlignCenter)
        self.before_label.setFixedHeight(20)  # Set a fixed height for the label
        self.before_pixmap = QLabel()
        self.before_pixmap.setFixedSize(500, 500)
        before_layout.addWidget(self.before_label)
        before_layout.addWidget(self.before_pixmap, alignment=Qt.AlignHCenter)
        before_after_layout.addLayout(before_layout)

        after_layout = QVBoxLayout()
        self.after_label = QLabel('After')
        self.after_label.setAlignment(Qt.AlignCenter)
        self.after_label.setFixedHeight(20)  # Set a fixed height for the label
        self.after_pixmap = QLabel()
        self.after_pixmap.setFixedSize(500, 500)
        after_layout.addWidget(self.after_label)
        after_layout.addWidget(self.after_pixmap, alignment=Qt.AlignHCenter)
        before_after_layout.addLayout(after_layout)

        layout.addLayout(before_after_layout)

        middle_layout = QHBoxLayout()
        self.upload_button = QPushButton('Upload Image')
        self.upload_button.clicked.connect(self.upload_image)
        self.retarget_button = QPushButton('Retarget')
        self.retarget_button.clicked.connect(self.retarget_image)
        middle_layout.addStretch()
        middle_layout.addWidget(self.upload_button)
        middle_layout.addWidget(self.retarget_button)
        middle_layout.addStretch()
        layout.addLayout(middle_layout)

        self.setLayout(layout)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Image", "",
                                                   "All Files (*);;Image Files (*.png;*.jpg;*.jpeg)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            if pixmap.width() > 600 or pixmap.height() > 600:
                pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio)
            self.before_pixmap.setPixmap(pixmap)
            print(f"Uploaded image: {file_name}")

    def retarget_image(self):
        # Placeholder for the image retargeting function
        print("Retargeting image...")
        # Update the 'after_pixmap' with the retargeted image
        self.after_pixmap.setPixmap(self.before_pixmap.pixmap())  # Just copying for now

    def show_main_page(self):
        self.stacked_widget.setCurrentIndex(0)


class VideoPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.is_playing = False

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.show_main_page)
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        layout.addLayout(top_layout)

        self.video_player_before = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget_before = QVideoWidget()
        self.video_player_before.setVideoOutput(self.video_widget_before)

        self.video_player_after = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget_after = QVideoWidget()
        self.video_player_after.setVideoOutput(self.video_widget_after)

        before_after_layout = QHBoxLayout()
        before_layout = QVBoxLayout()
        before_label = QLabel('Before')
        before_label.setAlignment(Qt.AlignCenter)
        before_label.setFixedHeight(20)  # Set a fixed height for the label
        before_layout.addWidget(before_label)
        before_layout.addWidget(self.video_widget_before)
        before_after_layout.addLayout(before_layout)

        after_layout = QVBoxLayout()
        after_label = QLabel('After')
        after_label.setAlignment(Qt.AlignCenter)
        after_label.setFixedHeight(20)  # Set a fixed height for the label
        after_layout.addWidget(after_label)
        after_layout.addWidget(self.video_widget_after)
        before_after_layout.addLayout(after_layout)

        layout.addLayout(before_after_layout)

        middle_layout = QHBoxLayout()
        self.upload_button = QPushButton('Upload Video')
        self.upload_button.clicked.connect(self.upload_video)
        self.retarget_button = QPushButton('Retarget')
        self.retarget_button.clicked.connect(self.retarget_video)
        middle_layout.addStretch()
        middle_layout.addWidget(self.upload_button)
        middle_layout.addWidget(self.retarget_button)
        middle_layout.addStretch()
        layout.addLayout(middle_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(100)  # Set to 100% for now
        layout.addWidget(self.progress_bar)

        play_buttons_layout = QHBoxLayout()
        self.play_button = QPushButton('Play Both')
        self.play_button.clicked.connect(self.toggle_play)
        play_buttons_layout.addWidget(self.play_button)

        layout.addLayout(play_buttons_layout)

        self.setLayout(layout)

    def upload_video(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Video", "", "All Files (*);;Video Files (*.mp4;*.avi)",
                                                   options=options)
        if file_name:
            media_content = QMediaContent(QUrl.fromLocalFile(file_name))
            self.video_player_before.setMedia(media_content)
            self.video_player_after.setMedia(media_content)  # Set the same video for "after" as a placeholder
            print(f"Uploaded video: {file_name}")

            # Play the videos to ensure they are loaded
            self.video_player_before.play()
            self.video_player_after.play()
            self.is_playing = True
            self.play_button.setText('Stop Both')

    def retarget_video(self):
        # Placeholder for the video retargeting function
        print("Retargeting video...")
        # Simulate a loading process
        self.progress_bar.setValue(50)
        QTimer.singleShot(2000, self.finish_retargeting)

    def finish_retargeting(self):
        # Placeholder to simulate that the video processing is done
        # Here you would replace the media of the 'after' player with the processed video
        self.progress_bar.setValue(100)
        print("Video retargeting complete")

    def toggle_play(self):
        if self.progress_bar.value() == 100:
            if self.is_playing:
                self.video_player_before.pause()
                self.video_player_after.pause()
                self.play_button.setText('Play Both')
            else:
                self.video_player_before.play()
                self.video_player_after.play()
                self.play_button.setText('Stop Both')
            self.is_playing = not self.is_playing
        else:
            print("Videos are not fully processed yet.")

    def show_main_page(self):
        self.stacked_widget.setCurrentIndex(0)


class AboutPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.show_main_page)
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        layout.addLayout(top_layout)

        self.label = QLabel('This is the About page.')
        layout.addWidget(self.label)
        self.setLayout(layout)

    def show_main_page(self):
        self.stacked_widget.setCurrentIndex(0)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()

        self.main_page = MainPage(self.stacked_widget)
        self.image_page = ImagePage(self.stacked_widget)
        self.video_page = VideoPage(self.stacked_widget)
        self.about_page = AboutPage(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.image_page)
        self.stacked_widget.addWidget(self.video_page)
        self.stacked_widget.addWidget(self.about_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)
        self.setWindowTitle('Media Viewer')
        self.setGeometry(100, 100, 1366, 768)  # Set to 16:9 aspect ratio


app = QApplication(sys.argv)
app.setStyleSheet(stylesheet)  # Apply the custom stylesheet
window = MainWindow()
window.show()
sys.exit(app.exec_())
