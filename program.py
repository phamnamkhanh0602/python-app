from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
import database 
from weather_api import *
from datetime import datetime

class Alert(QMessageBox):
   def error_message(self,message):
      self.setIcon(QMessageBox.Icon.Critical)
      self.setText(message)
      self.setWindowTitle('error')
      self.exec()

   def success_message(self,message):
      self.setIcon(QMessageBox.Icon.Information)
      self.setText(message)
      self.setWindowTitle('success')
      self.exec()

class Login(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui/login.ui',self)

      self.email_input = self.findChild(QLineEdit,'lineFullname')
      self.password_input = self.findChild(QLineEdit,'linePassword')

      self.btn_login = self.findChild(QPushButton,'pushLogin')
      self.btn_register = self.findChild(QPushButton,'pushSignup')
      
      self.btn_eye = self.findChild(QPushButton, "pushEye")
      
      self.btn_login.clicked.connect(self.login)
      self.btn_register.clicked.connect(self.show_register)
      
      self.btn_eye.clicked.connect(lambda: self.hiddenOrShow(self.password_input, self.btn_eye))
      
   def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
      if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-regular.svg"))
      else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-regular.svg"))
   
   def login(self):
      email = self.email_input.text()
      password = self.password_input.text()

      if email == '':
         msg = Alert()
         msg.error_message('Please enter email address')
         self.email_input.setFocus()
         return
      
      if password == '':
         msg = Alert()
         msg.error_message('Please enter password')
         self.password_input.setFocus()
         return
      
      user = database.find_user_by_email_and_password(email,password)
      if user:
         msg = Alert()
         msg.success_message('login successful')
         self.show_main(user["id"])
      else:
         msg = Alert()
         msg.success_message('Invalid email or password')

   def show_register(self):
      self.register = Register()
      self.register.show()
      self.close()
      
   def show_main(self, user_id):
      self.mainWindow = MainWindow(user_id)
      self.mainWindow.show()
      self.close()
      
class FutureWeatherItem(QWidget):
   def __init__(self, description, time, icon):
      super().__init__()
      uic.loadUi('ui/future_forecase_item.ui', self)
      
      self.setMinimumWidth(210)
      self.setMinimumHeight(45)
      
      self.lb_description = self.findChild(QLabel,'lb_description')
      self.lb_time = self.findChild(QLabel,'lb_time')
      self.lb_img = self.findChild(QLabel,'lb_img')
      
      self.lb_description.setText(description)
      self.lb_time.setText(time)
      self.lb_img.setPixmap(QPixmap(f"weather_icons/{icon}.png"))
      
      # Add horizontal line
      line = QFrame(self)
      line.setFrameShape(QFrame.Shape.HLine)
      line.setFrameShadow(QFrame.Shadow.Sunken)
      line.setStyleSheet("background-color: #1E90FF;")  # Blue color for the line
      line.setFixedHeight(2)
      
      # Get the existing layout
      layout = self.layout()
      if not layout:
         layout = QVBoxLayout(self)
         layout.setSpacing(10)  # Space between elements inside the item
         layout.setContentsMargins(15, 10, 15, 10)  # Left, Top, Right, Bottom margins
      
      # Add line to bottom with some spacing
      layout.addSpacing(5)  # Space before line
      layout.addWidget(line)
      layout.addSpacing(5)  # Space after line
      
      print(f"FutureWeatherItem created: {time} - {description}")
      
class Register(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui/register.ui',self)

      self.email_input = self.findChild(QLineEdit,'lineEmail')
      self.name_input = self.findChild(QLineEdit,'lineFullname')
      self.password_input = self.findChild(QLineEdit,'linePassword')
      self.confirm_password_input = self.findChild(QLineEdit,'lineConPassword')

      self.btn_register = self.findChild(QPushButton, 'pushSignup')
      self.btn_login = self.findChild(QPushButton,'pushLogin')
      
      self.btn_eye1 = self.findChild(QPushButton, "pushEye1")
      self.btn_eye2 = self.findChild(QPushButton, "pushEye2")
      
      self.btn_register.clicked.connect(self.register)
      self.btn_login.clicked.connect(self.showLogin)
      
      self.btn_eye1.clicked.connect(lambda: self.hiddenOrShow(self.password_input, self.btn_eye1))
      self.btn_eye2.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password_input, self.btn_eye2))
      
   def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
      if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-regular.svg"))
      else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-regular.svg"))
    
   def register(self):
      email = self.email_input.text()
      name = self.name_input.text()
      password = self.password_input.text()
      confirm_password = self.confirm_password_input.text()

      if email == '':
         msg = Alert()
         msg.error_message('please enter email address')
         self.email_input.setFocus()
         return

      if name == '':
         msg = Alert()
         msg.error_message('please enter name')
         self.name_input.setFocus()
         return
      
      if password == '':
         msg = Alert()
         msg.error_message('please enter password')
         self.password_input.setFocus()
         return
      if password != confirm_password:
         msg = Alert()
         msg.error_message('password and confirm password does not match')
         self.confirm_password_input.setFocus()
         return
      user = database.find_user_by_email(email)
      if user:
         msg = Alert()
         msg.error_message('email already exists')
      else:
         database.create_user(email,name,password)
         msg = Alert()
         msg.success_message('registration successful')
         self.showLogin()
         
   def showLogin(self):
      self.login = Login()
      self.login.show()
      self.close()

class MainWindow(QMainWindow):
   def __init__(self, user_id):
      super().__init__()
      uic.loadUi('ui/main.ui',self)
      self.user_id = user_id
      self.user = database.find_user_by_id(user_id)
      
      self.nav_main_btn = self.findChild(QPushButton,'nav_main_btn')
      self.nav_account_btn = self.findChild(QPushButton,'nav_account_btn')
      self.nav_save_btn = self.findChild(QPushButton,'nav_save_btn')
      self.nav_search_btn = self.findChild(QPushButton,'nav_search_btn')
      self.btn_search = self.findChild(QPushButton,'btn_search')
      self.txt_search = self.findChild(QLineEdit,'txt_search')
      self.weather_container = self.findChild(QWidget, 'weather_container')
      self.btn_avatar = self.findChild(QPushButton,'btn_avatar')
      
      # Clear any existing layout
      if self.weather_container.layout():
         old_layout = self.weather_container.layout()
         while old_layout.count():
            item = old_layout.takeAt(0)
            if item.widget():
               item.widget().deleteLater()
         QWidget().setLayout(old_layout)
      
      # Initialize weather container layout
      layout = QVBoxLayout()
      layout.setSpacing(0)
      layout.setContentsMargins(0, 0, 0, 0)
      self.weather_container.setLayout(layout)
      
      self.stackedWidget = self.findChild(QStackedWidget,'stackedWidget')
      self.stackedWidget.setCurrentIndex(0)
      
      self.nav_main_btn.clicked.connect(lambda: self.navigateScreen(0))
      self.nav_account_btn.clicked.connect(lambda: self.navigateScreen(2))
      self.nav_save_btn.clicked.connect(lambda: self.navigateScreen(3))
      self.nav_search_btn.clicked.connect(lambda: self.navigateScreen(1))
      self.btn_avatar.clicked.connect(self.update_avatar)
      self.btn_search.clicked.connect(self.search_weather)
      
      self.load_weather()
      
   def search_weather(self):
      name = self.txt_search.text()
      if self.load_today_weather(name):
         self.load_weather_forecast(name)
      
   def navigateScreen(self, page:int):
      self.stackedWidget.setCurrentIndex(page)
      
   def load_user_info(self):
      self.lb_name = self.findChild(QLabel, 'lb_name')
      self.lb_email = self.findChild(QLabel,'lb_email')
      self.lb_name.setText(self.user["name"])
      self.lb_email.setText(self.user["email"])
      self.btn_avatar.setIcon(QIcon(self.user["avatar"]))
      
   def update_avatar(self):
      file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *jpeg *.bmp)")
      if file:
         self.user["avatar"] = file
         self.btn_avatar.setIcon(QIcon(file))
         database.update_user_avatar(self.user_id, file)
      
   def load_weather(self):
      self.lb_city_name = self.findChild(QLabel,'lb_city_name')
      self.lb_cloud = self.findChild(QLabel,'lb_cloud')
      self.lb_weather_img = self.findChild(QLabel,'lb_weather_img')
      self.lb_humidity = self.findChild(QLabel,'lb_humidity')
      self.lb_visibility = self.findChild(QLabel,'lb_visibility')
      self.lb_wind = self.findChild(QLabel,'lb_wind')
      self.lb_temp = self.findChild(QLabel,'lb_temp')
      self.lb_weather_name = self.findChild(QLabel,'lb_weather_name')
      self.lb_weather_desc = self.findChild(QLabel,'lb_weather_desc')
      
      self.load_today_weather("SaiGon")
      self.load_weather_forecast("SaiGon")

   def load_today_weather(self, name):
      data = get_weather_by_name(name)
      if data["cod"] != 200:
         msg = Alert()
         msg.error_message(data["message"])
         return False

      self.lb_city_name.setText(data["name"])
      self.lb_weather_name.setText(data["weather"][0]["main"])
      visibility = data["visibility"] /1000
      self.lb_visibility.setText(f"{visibility} km")
      self.lb_weather_desc.setText(data["weather"][0]["description"])
      temp = data["main"]["temp"]
      self.lb_temp.setText(f"{temp} ℃")
      humidity = data["main"]["humidity"]
      self.lb_humidity.setText(f"{humidity} %")
      cloud = data["clouds"]["all"]
      self.lb_cloud.setText(f"{cloud} %")
      wind = data["wind"]["speed"]
      self.lb_wind.setText(f"{wind} km/h")
      return True

   def load_weather_forecast(self, name):
      time_labels = [self.findChild(QLabel, f'lb_time_{i+1}') for i in range(6)]
      img_labels = [self.findChild(QLabel, f'lb_img_{i+1}') for i in range(6)]
      temp_labels = [self.findChild(QLabel, f'lb_temp_{i+1}') for i in range(6)]
      
      data = get_weather_forecast_by_name(name)
      for i in range(6):
         dt = data["list"][i]["dt_txt"]
         date_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
         formatted_date = date_obj.strftime("%a %m/%d\n%H:%M")
         time_labels[i].setText(formatted_date)
         img_labels[i].setPixmap(QPixmap(f"weather_icons/{data['list'][i]['weather'][0]['icon']}.png"))
         temp_labels[i].setText(f"{data['list'][i]['main']['temp']} ℃")

      # Clear any existing layout
      if self.weather_container.layout():
         old_layout = self.weather_container.layout()
         while old_layout.count():
            item = old_layout.takeAt(0)
            if item.widget():
               item.widget().deleteLater()
      
      # Create and add weather items
      weather_items = self.create_weather_list(data)
      for item in weather_items:
         self.weather_container.layout().addWidget(item)

   def create_weather_list(self, data):
      weather_items = []
      
      # Get the time from first forecast
      first_dt = data["list"][0]["dt_txt"]
      first_date = datetime.strptime(first_dt, "%Y-%m-%d %H:%M:%S")
      target_hour = first_date.hour
      
      # Keep track of days we've seen
      seen_days = set()
      
      # Go through all forecasts
      for forecast in data["list"]:
         dt = forecast["dt_txt"]
         date_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
         
         # Only process if it's at our target hour and we haven't seen this day yet
         if date_obj.hour == target_hour and date_obj.date() not in seen_days:
            seen_days.add(date_obj.date())
            
            time_str = date_obj.strftime("%a")  # Day name
            description = forecast["weather"][0]["main"]
            icon = forecast["weather"][0]["icon"]
            
            # Create weather item
            weather_item = FutureWeatherItem(description, time_str, icon)
            weather_items.append(weather_item)
            
            # Stop if we have 7 days
            if len(weather_items) >= 7:
               break
      
      return weather_items

if __name__ == '__main__':
   app = QApplication(sys.argv)
   # login = Login()
   # login.show()
   login = MainWindow(11)
   login.show()
   app.exec()