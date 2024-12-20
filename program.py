from PyQt6.QtWidgets import QMainWindow,QApplication,QLineEdit,QMessageBox,QPushButton,QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import sys
import database

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

class MainWindow(QMainWindow):
   def __init__(self, user_id):
      super().__init__()
      uic.loadUi('ui/main.ui',self)
      self.user_id = user_id
      
      self.nav_main_btn = self.findChild(QPushButton,'nav_main_btn')
      self.nav_account_btn = self.findChild(QPushButton,'nav_account_btn')
      self.nav_save_btn = self.findChild(QPushButton,'nav_save_btn')
      self.nav_search_btn = self.findChild(QPushButton,'nav_search_btn')
      self.stackedWidget = self.findChild(QStackedWidget,'stackedWidget')
      self.stackedWidget.setCurrentIndex(0)
      
      
      self.nav_main_btn.clicked.connect(lambda: self.navigateScreen(0))
      self.nav_account_btn.clicked.connect(lambda: self.navigateScreen(2))
      self.nav_save_btn.clicked.connect(lambda: self.navigateScreen(3))
      self.nav_search_btn.clicked.connect(lambda: self.navigateScreen(1))

      
   def navigateScreen(self, page:int):
      self.stackedWidget.setCurrentIndex(page)

    
if __name__ == '__main__':
   app = QApplication(sys.argv)
   login = Login()
   login.show()
   app.exec()