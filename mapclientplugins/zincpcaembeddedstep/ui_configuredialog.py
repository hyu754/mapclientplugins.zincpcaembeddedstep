# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\David Yu\Documents\mapclient\mapclientplugins.zincpcaembeddedstep\mapclientplugins\zincpcaembeddedstep\qt\configuredialog.ui'
#
# Created: Fri Apr 20 15:51:19 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        ConfigureDialog.setObjectName("ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QtGui.QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.configGroupBox = QtGui.QGroupBox(ConfigureDialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtGui.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label0)
        self.lineEdit0 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName("lineEdit0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit0)
        self.label1 = QtGui.QLabel(self.configGroupBox)
        self.label1.setObjectName("label1")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineEdit1 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit1.setObjectName("lineEdit1")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit1)
        self.label2 = QtGui.QLabel(self.configGroupBox)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label2)
        self.lineEdit2 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit2.setObjectName("lineEdit2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit2)
        self.label3 = QtGui.QLabel(self.configGroupBox)
        self.label3.setObjectName("label3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label3)
        self.lineEdit3 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit3.setObjectName("lineEdit3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit3)
        self.label4 = QtGui.QLabel(self.configGroupBox)
        self.label4.setObjectName("label4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label4)
        self.lineEdit4 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit4.setObjectName("lineEdit4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit4)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtGui.QApplication.translate("ConfigureDialog", "Configure Step", None, QtGui.QApplication.UnicodeUTF8))
        self.label0.setText(QtGui.QApplication.translate("ConfigureDialog", "identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("ConfigureDialog", "Embedding host:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("ConfigureDialog", "Embedding files:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("ConfigureDialog", "Embedding group names:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label4.setText(QtGui.QApplication.translate("ConfigureDialog", "Embedding type:  ", None, QtGui.QApplication.UnicodeUTF8))

