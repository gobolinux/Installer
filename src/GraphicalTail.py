from PyQt4 import QtCore
from PyQt4 import QtGui
from GraphicalTailForm import *
from PyQt4.QtGui import QApplication, QDialog

import threading

class GraphicalTail(QtCore.QObject):
	output = None
	w = None
	
	textWrittenSignal = QtCore.pyqtSignal(str)
	
	def __init__(self) :
		QtCore.QObject.__init__(self)
		self.output = open('/tmp/GoboLinuxInstall.log', 'w')
		
		self.color = {}
		self.color['Gray']     =('\033[1;30m' , '<font color="#777777">')
		self.color['BoldBlue'] =('\033[1;34m' , '<font color="#777700">')
		self.color['Brown']    =('\033[33m'   , '<font color="#777700">')
		self.color['Yellow']   =('\033[1;33m' , '<font color="#777700">')
		self.color['BoldGreen']=('\033[1;32m' , '<font color="#005050">')
		self.color['BoldRed']  =('\033[1;31m' , '<font color="#FF0000">')
		self.color['Cyan']     =('\033[36m'   , '<font color="#005050">')
		self.color['BoldCyan'] =('\033[1;36m' , '<font color="#777700">')
		self.color['RedWhite'] =('\033[41;37m', '<font color="#777700">')
		self.color['Normal']   =('\033[0m'    , '</font>')#'"#000000"')
		self.color['LineBreak']=('\n'         , '<br>')

		self.textWrittenSignal.connect(self.textWritten)
		self.initQt()

	def enableOk(self) :
		self.output.close()
		self.w.okButton.setEnabled(1)

	def append(self, s):
		if not s.endswith('\n'):
			s += '\n'
		try :
			self.output.write(s)
		except :
			pass
		
		self.textWrittenSignal.emit(s)

	def textWritten(self, s) :		
		for key in self.color.keys() :
			terminal, html = self.color[key]
			s = s.replace(terminal, html)
		
		cursor = self.w.textWidget.textCursor()
		if self.w.autoScroll.isChecked():
			cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertHtml(s)
		if self.w.autoScroll.isChecked():
			self.w.textWidget.setTextCursor(cursor)
			self.w.textWidget.ensureCursorVisible()
		
	def initQt(self):
		self.app = QApplication([])
		self.window = QDialog()

		self.ui = Ui_GraphicalTailFormDialog()
		self.ui.setupUi(self.window)

		self.window.setGeometry(QtCore.QRect(50, 50, 600, 600))
		self.window.show()
		
		self.w = self.ui

	def exec_(self):
		self.app.exec_()
