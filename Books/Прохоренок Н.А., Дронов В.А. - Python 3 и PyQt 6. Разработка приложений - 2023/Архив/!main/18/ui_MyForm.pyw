# Form implementation generated from reading ui file 'MyForm.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MyForm(object):
    def setupUi(self, MyForm):
        MyForm.setObjectName("MyForm")
        MyForm.resize(300, 70)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MyForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MyForm)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btnQuit = QtWidgets.QPushButton(MyForm)
        self.btnQuit.setObjectName("btnQuit")
        self.verticalLayout.addWidget(self.btnQuit)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MyForm)
        QtCore.QMetaObject.connectSlotsByName(MyForm)

    def retranslateUi(self, MyForm):
        _translate = QtCore.QCoreApplication.translate
        MyForm.setWindowTitle(_translate("MyForm", "Первая форма"))
        self.label.setText(_translate("MyForm", "Привет, мир!"))
        self.btnQuit.setText(_translate("MyForm", "&Закрыть"))
