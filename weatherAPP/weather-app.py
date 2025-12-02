import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit )
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("30°C", self)
        self.emoji_label = QLabel("☀️", self)
        self.ddescription_label = QLabel("Sunny", self)

    def initUI(self):
        self.setWindowTitle("Weather App")

        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.ddescription_label)

        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.ddescription_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel, QPushButton {
                background-color: #87CEEB;
                font-family: Arial;
            }
            QLabel {
                font-size: 24px;
                color: #FFFFFF;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())