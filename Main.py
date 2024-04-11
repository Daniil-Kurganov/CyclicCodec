import sys
from GUI import *

def start_codec_working() -> None:
    '''Начало работы кодека'''
    if ui.RadioButtonPlynom.isChecked():
        ui.SpinBoxR.setEnabled(True)
        ui.LabelN.setEnabled(True)
        # .toPlainText()
    elif ui.RadioButtonMatrix.isChecked():
        ui.SpinBoxR.setEnabled(False)
        ui.LabelN.setEnabled(False)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())