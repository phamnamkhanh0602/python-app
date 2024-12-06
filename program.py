from PyQt6.QtWidgets import QMainWindow,QApplication,QLineEdit,QMessageBox,QPushButton
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
        self.password_input = self.findChild(QLineEdit,'lineFullname')

        self.btn_login = self.findChild(QPushButton,'pushLogin')
        self.btn_register = self.findChild(QPushButton,'pushSignup')

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
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
      else:
         msg = Alert()
         msg.success_message('Invalid email or password')

    def show_register(self):
        register = Register()
        register.show()
   

class Register(QMainWindow):
    def __init__(self):
      super().__init__()
      uic.loadUi('ui/register.ui',self)

      self.email_input = self.findChild(QPushButton,'txt_email')
      self.name_input = self.findChild(QPushButton,'txt_name')
      self.password_input = self.findChild(QPushButton,'txt_password')
      self.confirm_password_inpt = self.findChild(QPushButton,'txt_confirm_password')

      self.btn_register = self.findChild(QPushButton, 'btn_register')
      self.btn_login = self.findChild(QPushButton,'btn_login')
    
    def register(self):
       email = self.email_input.text()
       name = self.name_input.text()
       password = self.password_input.text()
       confirm_password = self.confirm_password_inpt.text()

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
          self.confirm_password_inpt.setFocus()
          return
       user = database.find_user_by_email(email)
       if user:
          msg = Alert()
          msg.error_message('email already exists')
       else:
          database.create_user(email,name,password)
          msg = Alert()
          msg.success_message('registration successful')
          self.close()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())