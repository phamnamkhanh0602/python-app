from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
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

class NoteItem(QWidget):
   def __init__(self, note, timestamp, note_id, user_id):
      super().__init__()
      uic.loadUi('ui/note_item.ui', self)
      
      self.note_id = note_id
      self.user_id = user_id
      
      # Find widgets
      self.txt_note = self.findChild(QTextEdit,'txt_note')
      self.lb_time = self.findChild(QLabel,'lb_time')
      self.btn_edit = self.findChild(QPushButton,'btn_edit')
      self.btn_delete = self.findChild(QPushButton,'btn_delete')
      
      # Set content
      print(f"Setting note text: {note}")
      self.txt_note.setText(note)
      self.txt_note.setReadOnly(True)
      self.lb_time.setText(timestamp)
      
      # Connect buttons
      self.btn_edit.clicked.connect(self.edit_note)
      self.btn_delete.clicked.connect(self.delete_note)
      
      # Set minimum size but allow expanding
      self.setMinimumSize(240, 200)
      self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
      
      # Apply styles
      self.setStyleSheet("""
         QWidget#Form {
            background-color: #202c3c;
            color: white;
            border: 1px solid #1e90ff;
            border-radius: 4px;
         }
         QTextEdit {
            background-color: #2c3e50;
            color: white;
            border: 1px solid #1e90ff;
            border-radius: 3px;
            padding: 3px;
         }
         QPushButton {
            background-color: #1e90ff;
            color: white;
            border-radius: 3px;
            padding: 3px;
            border: none;
            min-width: 60px;
         }
         QPushButton:hover {
            background-color: #1873cc;
         }
         QLabel {
            color: white;
            background-color: transparent;
         }
      """)
      
   def edit_note(self):
      dialog = UpdateNoteDialog(self.user_id, self.note_id)
      dialog.load_note_data()
      if dialog.exec() == QDialog.DialogCode.Accepted:
         # Refresh the note data
         note = database.get_note_by_id(self.note_id)
         self.txt_note.setText(note["note"])
         self.lb_time.setText(note["timestamp"])
      
   def delete_note(self):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Icon.Question)
      msg.setText("Are you sure you want to delete this note?")
      msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
      if msg.exec() == QMessageBox.StandardButton.Yes:
         database.delete_note(self.note_id)
         self.deleteLater()  # Remove widget properly
         # Notify parent to refresh layout
         parent = self.parent()
         if parent:
            parent.update()

class AddNoteDialog(QDialog):
   def __init__(self, user_id):
      super().__init__()
      uic.loadUi('ui/add_note.ui',self)
      self.user_id = user_id
      
      self.txt_note = self.findChild(QTextEdit,'txt_note')
      self.dt_time = self.findChild(QDateTimeEdit,'dt_time')
      
      # Set current datetime as minimum and default
      current_dt = QDateTime.currentDateTime()
      self.dt_time.setDateTime(current_dt)
      self.dt_time.setMinimumDateTime(current_dt)
      self.dt_time.setCalendarPopup(True)
      self.dt_time.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
      
      self.buttonBox.accepted.connect(self.save_note)
      self.buttonBox.rejected.connect(self.close)

   def save_note(self):
      note = self.txt_note.toPlainText()
      if not note.strip():
         msg = Alert()
         msg.error_message('Please enter a note')
         return
         
      timestamp = self.dt_time.dateTime().toString("dd/MM/yyyy HH:mm:ss")
      database.create_note(self.user_id, note, timestamp)
      msg = Alert()
      msg.success_message("Add note success")
      self.accept()

class UpdateNoteDialog(QDialog):
   def __init__(self, user_id, note_id):
      super().__init__()
      uic.loadUi('ui/add_note.ui',self)

      self.setWindowTitle('Update Note')
      self.user_id = user_id
      self.note_id = note_id
      
      self.txt_note = self.findChild(QTextEdit,'txt_note')
      self.dt_time = self.findChild(QDateTimeEdit,'dt_time')
      
      # Set current datetime as minimum
      current_dt = QDateTime.currentDateTime()
      self.dt_time.setMinimumDateTime(current_dt)
      self.dt_time.setCalendarPopup(True)
      self.dt_time.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
      
      self.buttonBox.accepted.connect(self.update_note)
      self.buttonBox.rejected.connect(self.close)
   
   def load_note_data(self):
      note = database.get_note_by_id(self.note_id)
      self.txt_note.setText(note["note"])
      
      # Convert timestamp to QDateTime
      dt = QDateTime.fromString(note["timestamp"], "dd/MM/yyyy HH:mm:ss")
      if dt < QDateTime.currentDateTime():
         dt = QDateTime.currentDateTime()
      self.dt_time.setDateTime(dt)
   
   def update_note(self):
      note = self.txt_note.toPlainText()
      if not note.strip():
         msg = Alert()
         msg.error_message('Please enter a note')
         return
         
      timestamp = self.dt_time.dateTime().toString("dd/MM/yyyy HH:mm:ss")
      database.update_note(self.note_id, note, timestamp)
      self.accept()


class MainWindow(QMainWindow):
   def __init__(self, user_id):
      super().__init__()
      uic.loadUi('ui/main.ui',self)
      self.user_id = user_id
      self.user = database.find_user_by_id(user_id)
      
      # Navigation buttons
      self.nav_main_btn = self.findChild(QPushButton,'nav_main_btn')
      self.nav_account_btn = self.findChild(QPushButton,'nav_account_btn')
      self.nav_search_btn = self.findChild(QPushButton,'nav_search_btn')
      
      # Calendar widget
      self.calendar = self.findChild(QCalendarWidget,'calendarWidget')
      self.calendar.selectionChanged.connect(self.on_date_selected)
      
      # Search elements
      self.btn_search = self.findChild(QPushButton,'btn_search')
      self.txt_search = self.findChild(QLineEdit,'txt_search')
      
      # Notes elements
      self.note_container = self.findChild(QWidget, 'note_container')
      
      # Weather elements
      self.weather_container = self.findChild(QWidget, 'weather_container')
      self.lb_city_name = self.findChild(QLabel,'lb_city_name')
      self.lb_cloud = self.findChild(QLabel,'lb_cloud')
      self.lb_weather_img = self.findChild(QLabel,'lb_weather_img')
      self.lb_humidity = self.findChild(QLabel,'lb_humidity')
      self.lb_visibility = self.findChild(QLabel,'lb_visibility')
      self.lb_wind = self.findChild(QLabel,'lb_wind')
      self.lb_temp = self.findChild(QLabel,'lb_temp')
      self.lb_weather_name = self.findChild(QLabel,'lb_weather_name')
      self.lb_weather_desc = self.findChild(QLabel,'lb_weather_desc')
      
      # Account elements
      self.btn_avatar = self.findChild(QPushButton,'btn_avatar')
      self.txt_name = self.findChild(QLineEdit,'txt_name')
      self.txt_email = self.findChild(QLineEdit,'txt_email')
      self.txt_address = self.findChild(QLineEdit,'txt_address')
      self.d_dob = self.findChild(QDateEdit,'d_dob')
      self.cb_gender = self.findChild(QComboBox,'cb_gender')
      self.btn_update_info = self.findChild(QPushButton,'btn_update_info')
      
      
      # Stacked widget
      self.stackedWidget = self.findChild(QStackedWidget,'stackedWidget')
      self.stackedWidget.setCurrentIndex(0)
      
      # Connect signals
      self.nav_main_btn.clicked.connect(lambda: self.navigateScreen(0))
      self.nav_account_btn.clicked.connect(lambda: self.navigateScreen(1))
      self.nav_search_btn.clicked.connect(lambda: self.navigateScreen(2))
      self.btn_search.clicked.connect(self.search_weather)
      self.btn_avatar.clicked.connect(self.update_avatar)
      self.btn_add_note.clicked.connect(self.add_note)
      self.btn_update_info.clicked.connect(self.update_info)
      
      # Initialize layouts
      self.init_weather_layout()
      self.init_notes_layout()
      
      # Load initial data
      self.load_weather()
      self.load_user_info()
      self.load_notes()
      self.highlight_note_dates()

   def init_weather_layout(self):
      if not self.weather_container.layout():
         layout = QVBoxLayout(self.weather_container)
         layout.setSpacing(0)
         layout.setContentsMargins(0, 0, 0, 0)
         self.weather_container.setLayout(layout)

   def init_notes_layout(self):
      # Create scroll area if not exists
      self.scroll_area = QScrollArea(self.note_container)
      self.scroll_area.setWidgetResizable(True)
      self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
      self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
      self.scroll_area.setStyleSheet("""
         QScrollArea {
            border: none;
            background-color: transparent;
         }
         QScrollBar:vertical {
            border: none;
            background: #202c3c;
            width: 8px;
            margin: 0px;
         }
         QScrollBar::handle:vertical {
            background: #1e90ff;
            min-height: 20px;
            border-radius: 4px;
         }
         QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
         }
      """)
      
      # Create widget to hold notes
      self.notes_widget = QWidget()
      self.notes_widget.setStyleSheet("background-color: transparent;")
      
      # Create layout for notes
      self.notes_layout = QVBoxLayout(self.notes_widget)
      self.notes_layout.setSpacing(8)  # Space between notes
      self.notes_layout.setContentsMargins(4, 4, 4, 4)  # Small margins for container
      self.notes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
      
      # Set the widget to the scroll area
      self.scroll_area.setWidget(self.notes_widget)
      
      # Add scroll area to note container
      container_layout = QVBoxLayout(self.note_container)
      container_layout.setContentsMargins(0, 0, 0, 0)
      container_layout.addWidget(self.scroll_area)

   def load_weather(self):
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
      data = get_weather_forecast_by_name(name)
      weather_items = self.create_weather_list(data)
      
      # Clear existing items
      layout = self.weather_container.layout()
      while layout.count():
         item = layout.takeAt(0)
         if item.widget():
            item.widget().deleteLater()
      
      # Add new items
      for item in weather_items:
         layout.addWidget(item)

   def load_notes(self):
      # Update calendar highlighting
      self.highlight_note_dates()
      
      # Get all notes for the selected month
      selected_date = self.calendar.selectedDate()
      
      notes = database.get_all_notes(self.user_id)
      month_notes = []
      for note in notes:
         note_date = QDate.fromString(note["timestamp"].split()[0], "dd/MM/yyyy")
         if note_date.month() == selected_date.month() and note_date.year() == selected_date.year():
            month_notes.append(note)
      
      # Clear existing notes
      while self.notes_layout.count():
         item = self.notes_layout.takeAt(0)
         if item.widget():
            item.widget().deleteLater()
      
      # Calculate available width for notes
      available_width = self.note_container.width() - 24  # Account for scrollbar and margins
      
      # Add filtered notes
      for note in month_notes:
         note_item = NoteItem(note["note"], note["timestamp"], note["id"], self.user_id)
         note_item.setMinimumWidth(available_width)
         self.notes_layout.addWidget(note_item)
      
      # Add stretch at the end
      self.notes_layout.addStretch()
      
      # Update layouts
      self.notes_widget.adjustSize()
      self.scroll_area.updateGeometry()

   def add_note(self):
      dialog = AddNoteDialog(self.user_id)
      dialog.show()
      if dialog.exec() == QDialog.DialogCode.Accepted:
         self.load_notes()  # Reload notes after adding

   def search_weather(self):
      name = self.txt_search.text()
      if self.load_today_weather(name):
         self.load_weather_forecast(name)
      
   def navigateScreen(self, page:int):
      self.stackedWidget.setCurrentIndex(page)
      
   def load_user_info(self):
      self.txt_name.setText(self.user["name"])
      self.txt_email.setText(self.user["email"])
      self.txt_email.setReadOnly(True)
      self.txt_address.setText(self.user["address"])
      self.d_dob.setDate(QDate.fromString(self.user["dob"], "dd/MM/yyyy"))
      self.cb_gender.setCurrentText(self.user["gender"])
      self.btn_avatar.setIcon(QIcon(self.user["avatar"]))
      
   def update_info(self):
      name = self.txt_name.text()
      address = self.txt_address.text()
      dob = self.d_dob.date().toString("dd/MM/yyyy")
      gender = self.cb_gender.currentText()
      database.update_user(self.user_id, name, address, dob, gender)
      msg = Alert()
      msg.success_message("Update info success")
      self.load_user_info() 
      
   def update_avatar(self):
      file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *jpeg *.bmp)")
      if file:
         self.user["avatar"] = file
         self.btn_avatar.setIcon(QIcon(file))
         database.update_user_avatar(self.user_id, file)
      
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

   def highlight_note_dates(self):
      # Get all notes
      notes = database.get_all_notes(self.user_id)
      
      # Create a text format for dates with notes
      fmt = QTextCharFormat()
      fmt.setBackground(QColor("#1e90ff"))  # Blue background
      fmt.setForeground(QColor("white"))    # White text
      
      # Clear any existing highlighting
      self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
      
      # Highlight dates that have notes
      for note in notes:
         date = QDate.fromString(note["timestamp"], "dd/MM/yyyy HH:mm:ss")
         self.calendar.setDateTextFormat(date, fmt)
   
   def on_date_selected(self):
      selected_date = self.calendar.selectedDate()
      
      # Get all notes
      notes = database.get_all_notes(self.user_id)
      
      # Filter notes for the selected month
      month_notes = []
      for note in notes:
         note_date = QDate.fromString(note["timestamp"].split()[0], "dd/MM/yyyy")
         if note_date.month() == selected_date.month() and note_date.year() == selected_date.year():
            month_notes.append(note)
      
      # Update the notes display
      while self.notes_layout.count():
         item = self.notes_layout.takeAt(0)
         if item.widget():
            item.widget().deleteLater()
      
      # Add filtered notes
      available_width = self.note_container.width() - 24
      for note in month_notes:
         note_item = NoteItem(note["note"], note["timestamp"], note["id"], self.user_id)
         note_item.setMinimumWidth(available_width)
         self.notes_layout.addWidget(note_item)
      
      # Add stretch at the end
      self.notes_layout.addStretch()
      
      # Update layouts
      self.notes_widget.adjustSize()
      self.scroll_area.updateGeometry()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   # login = Login()
   # login.show()
   login = MainWindow(11)
   login.show()
   app.exec()