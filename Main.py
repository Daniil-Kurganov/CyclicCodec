import sys
import re
import sympy
from sympy import poly
from GUI import *
from PyQt5.QtWidgets import QMessageBox

def show_error_message(int_error_key: str) -> None:
    '''Вывод ошибок'''
    dictionary_error_texts = {6: 'Некорректный ввод.', 13: '', 666: ''}
    message_error = QMessageBox()
    message_error.setIcon(QMessageBox.Critical)
    message_error.setText("Ошибка")
    message_error.setInformativeText(dictionary_error_texts[int_error_key])
    message_error.setWindowTitle("Ошибка!")
    message_error.exec_()
    return None
def checking_the_polynomial_generation_line(string_polynom_generating: str) -> bool:
    '''Проверка корректности вводимой строки генерации полинома'''
    list_checking = string_polynom_generating.split(' ')
    if (len(list_checking) - 1) % 2 != 0: return False
    else:
        for int_index, string_element in enumerate(list_checking):
            if int_index % 2 == 0 or int_index == 0:
                if string_element in ['x', '1']: pass
                elif re.fullmatch('x\*\*\d', string_element): pass
                else: return False
            elif string_element != '+': return False
        return True
def creating_generator_matrix(list_matrix_first_string: list) -> list:
    '''Создание порождающей матрицы путём циклического сдвига 1 строки'''
    list_generator_matrix = [list_matrix_first_string]
    list_current_format = list_matrix_first_string
    for int_iteration in range(int_information_subwords_length - 1):
        list_current_format = [list_current_format[-1]] + list_current_format[:-1]
        list_generator_matrix.append(list_current_format)
    return list_generator_matrix
def start_codec_working() -> None:
    '''Начало работы кодека'''
    global int_information_subwords_length, symbol_x
    symbol_x = sympy.symbols('x')
    if ui.RadioButtonPlynom.isChecked():
        int_code_subwords_length = int(ui.SpinBoxR.value())
        string_polynom_generating = str(ui.TextEditInputPolynomOrMatrixLine.toPlainText())
        if checking_the_polynomial_generation_line(string_polynom_generating) and len(string_polynom_generating) != 0:
            if string_polynom_generating in ['x', '1']:
                show_error_message(6)
                return None
            try: polynom_generating = poly(string_polynom_generating, symbol_x)
            except:
                show_error_message(6)
                return None
            int_information_subwords_length = int_code_subwords_length - sympy.degree(polynom_generating)
            if sympy.degree(polynom_generating) >= int_code_subwords_length - 1: show_error_message(6)
            list_polynom_dergees = [tuple_current_degree[0] for tuple_current_degree in
                                    polynom_generating.as_dict().keys()]
            string_matrix_first_string = '0' * int_code_subwords_length
            for int_current_polynom_degree in list_polynom_dergees:
                string_matrix_first_string = (string_matrix_first_string[:int_current_polynom_degree] + '1' +
                                              string_matrix_first_string[int_current_polynom_degree + 1:])
            list_generator_matrix = creating_generator_matrix(list(string_matrix_first_string))
        else:
            show_error_message(6)
            return None
    elif ui.RadioButtonMatrix.isChecked(): pass
    return None
def enable_code_subwords_length() -> None:
    '''Активация ввода длины кодовых подслов'''
    ui.SpinBoxR.setEnabled(True)
    ui.LabelN.setEnabled(True)
    return None
def disable_code_subwords_length() -> None:
    '''Деактивация ввода длины кодовых подслов'''
    ui.SpinBoxR.setEnabled(False)
    ui.LabelN.setEnabled(False)
    return None

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.RadioButtonPlynom.clicked.connect(enable_code_subwords_length)
ui.RadioButtonMatrix.clicked.connect(disable_code_subwords_length)
ui.PushButtonStart.clicked.connect(start_codec_working)
sys.exit(app.exec_())
