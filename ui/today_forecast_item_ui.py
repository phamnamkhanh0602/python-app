# Form implementation generated from reading ui file '/Users/pinxun/Documents/MindX/PTA/PTA07/FINAL PROJECT/NamKhanh/python-app/ui/today_forecast_item.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(80, 90)
        self.thoi_tiet = QtWidgets.QLabel(parent=Form)
        self.thoi_tiet.setGeometry(QtCore.QRect(-10, 30, 91, 71))
        self.thoi_tiet.setText("")
        self.thoi_tiet.setPixmap(QtGui.QPixmap("/Users/pinxun/Documents/MindX/PTA/PTA07/FINAL PROJECT/NamKhanh/python-app/ui/../img/clouds.png"))
        self.thoi_tiet.setScaledContents(True)
        self.thoi_tiet.setObjectName("thoi_tiet")
        self.thoi_gian = QtWidgets.QLabel(parent=Form)
        self.thoi_gian.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.thoi_gian.setObjectName("thoi_gian")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.thoi_gian.setText(_translate("Form", "6:00 AM"))
