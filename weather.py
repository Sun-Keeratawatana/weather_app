
from PySide2.QtMultimedia import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyowm
import sys
class Weathering_with_me(QWidget):
    def __init__(self):
        self.owm = pyowm.OWM('a8cfa5cb694a9ed21d8c581df262cab7')
        QWidget.__init__(self,None)
        vbox = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setText("Enter the city: ")
        vbox.addWidget(self.label)
        self.city = QLineEdit(self)
        vbox.addWidget(self.city)
        self.dtb = QPushButton("search", self)
        self.dtb.clicked.connect(self.search)
        vbox.addWidget(self.dtb)
        self.setLayout(vbox)
        self.show()
    def search(self):
        try:
            self.observation = self.owm.weather_at_place(self.city.text())
            w = self.observation.get_weather()
            self.wind_speed = "Wind speed: "+str(w.get_wind()['speed'])+"m/s"
            self.humid = "Humidity: "+str(w.get_humidity())+"%"+"\t"+"Pressure:"+str(w.get_pressure()['press'])+"hPa"
            self.temp = "Temperature"+str(round(w.get_temperature('celsius')['temp'],1))+"c"
            self.visibility = "Visiblilty: "+str((w.get_visibility_distance())/1000)+"km"
            self.detail = w.get_detailed_status()
            self.ref = str(w.get_reference_time('date'))
            text = self.ref+'\n'+ self.detail+'\n'+ self.temp+'\n'+ self.humid+'\n'+ self.wind_speed+'\n'+ self.visibility
            dialog = QDialog(self)
            layout = QVBoxLayout()
            label = QLabel(self)  
            label.setText(text)
            layout.addWidget(label)
            close_button = QPushButton("Close window")
            close_button.clicked.connect(dialog.close)
            label2 = QLabel(self)
            layout.addWidget(label2)
            self.setLayout(layout)
            if "clouds" in self.detail:
                file = "weather/clouddy.gif"
                song = "weather/Windy.wav"
            elif "rain" in self.detail or "d rizzle" in self.detail:
                file = "weather/rain.gif"
                song = "weather/rain_sound.wav"
            elif "snow" in self.detail:
                file = "weather/snowwy.gif"
                song = "weather/Windy.wav"
            elif "mist" in self.detail or "fog" in self.detail or "haze" in self.detail:
                file = "weather/mist.gif"
                song = "weather/Windy.wav"
            else:
                file = "weather/clear.gif"
                song = "weather/Clear_sky.wav"
            self.movie = QMovie(file, QByteArray(), self)
            self.movie.setCacheMode(QMovie.CacheAll)
            label2.setMovie(self.movie)
            QSound.play(song)
            self.movie.start()
            layout.addWidget(close_button)
            dialog.setLayout(layout)
            dialog.show()
        except:
            print("Unable to retrieve data.\nPlease try again!")
            self.error()
    def error(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label = QLabel(self)
        label.setText("Unable to retrieve data.\nPlease try again!")
        layout.addWidget(label)
        close_button = QPushButton("Close window")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Weathering_with_me()
    sys.exit(app.exec_())
