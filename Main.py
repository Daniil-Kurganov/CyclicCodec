import sys
import re
import sympy
import math
import random
from sympy import poly
from GUI import *
from PyQt5.QtWidgets import QMessageBox

def show_error_message(int_error_key: str) -> None:
    '''Вывод ошибок'''
    dictionary_error_texts = {6: 'Некорректный ввод.', 13: 'Переполнение памяти', 666: '', 451: ''}
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
                elif re.fullmatch('x\*\*\d(\d)*', string_element): pass
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
def creating_polynom(string_subword: str) -> sympy.Poly:
    '''Перевод бинарного сообщения в полином'''
    string_polynom = ''
    for int_index_of_current_1 in find_all_1(string_subword):
        if int_index_of_current_1 == 0: string_polynom += '1'
        elif int_index_of_current_1 == 1: string_polynom += 'x'
        else: string_polynom += 'x**{}'.format(int_index_of_current_1)
        string_polynom += ' + '
    return poly(string_polynom[:-3], symbol_x, domain='GF(2)')
def find_all_1(string_search_base: str) -> list:
    '''Нахождение индексов 1 в строке'''
    list_indices_of_1 = []
    for int_index, string_current_number in enumerate(string_search_base):
        if string_current_number == '1': list_indices_of_1.append(int_index)
    return list_indices_of_1
def error_processing(string_current_code_subword: str) -> str:
    '''Внесение ошибок в текущем кодовом подслове'''
    list_indices_of_1 = find_all_1(string_current_code_subword)
    if len(list_indices_of_1) == 0: return string_current_code_subword
    elif len(list_indices_of_1) > 1: int_position_of_error = random.randint(0, len(string_current_code_subword) - 1)
    else:
        while True:
            int_position_of_error = random.randint(0, len(string_current_code_subword) - 1)
            if int_position_of_error != list_indices_of_1[0]: break
    return (string_current_code_subword[:int_position_of_error] + changing_the_bit(string_current_code_subword[int_position_of_error]) +
        string_current_code_subword[int_position_of_error + 1:])
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    if int(string_bit): return '0'
    else: return '1'
def division_of_polynomials(polynom_dividend: sympy.Poly, polynom_divider: sympy.Poly) -> (sympy.Poly, sympy.Poly):
    '''Деление полиномов'''
    polynom_dividend = sympy.poly(polynom_dividend, symbol_x, domain='GF(2)')
    polynom_divider = sympy.poly(polynom_divider, symbol_x, domain='GF(2)')
    polynom_quotient, polynom_remainder = sympy.div(polynom_dividend, polynom_divider, symbol_x)
    return polynom_quotient, polynom_remainder
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
            try: polynom_generating = poly(string_polynom_generating, symbol_x, domain = 'GF(2)')
            except:
                show_error_message(6)
                return None
            int_information_subwords_length = int_code_subwords_length - sympy.degree(polynom_generating)
            if sympy.degree(polynom_generating) >= int_code_subwords_length - 1:
                show_error_message(6)
                return None
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
    elif ui.RadioButtonMatrix.isChecked():
        string_input_first_string = str(ui.TextEditInputPolynomOrMatrixLine.toPlainText())
        if not re.fullmatch('[10]*', string_input_first_string):
            show_error_message(6)
            return None
        int_code_subwords_length = len(string_input_first_string)
        int_information_subwords_length = int_code_subwords_length - string_input_first_string.rfind('1')
        list_generator_matrix = creating_generator_matrix(list(string_input_first_string))
        polynom_generating = creating_polynom(string_input_first_string)
    print('Порождающая матрица: ')
    for list_current_row in list_generator_matrix:
        print(list_current_row)
    print()
    print('Порождающий полином: {}'.format(polynom_generating.as_expr()))
    string_input_text_real = str(ui.TextEditInputText.toPlainText())
    string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
    ui.TextEditOutputBinaryTextIn.setText(string_input_text_binary)
    list_informaion_subwords, list_code_subwords, list_submessages = [], [], []
    int_count_of_zeros = 0
    if len(string_input_text_binary) > int_information_subwords_length:
        for int_iteration in range(1, math.ceil(len(string_input_text_binary) / int_information_subwords_length)):
            list_informaion_subwords.append(string_input_text_binary[int_iteration * int_information_subwords_length -
                                                                     int_information_subwords_length:int_iteration * int_information_subwords_length])
        if len(string_input_text_binary) % int_information_subwords_length != 0:
            int_count_of_zeros = int_information_subwords_length - (len(string_input_text_binary) -
                                                                    (int_information_subwords_length * (
                                                                                len(string_input_text_binary) // int_information_subwords_length)))
            list_informaion_subwords.append(
                ('0' * int_count_of_zeros) + string_input_text_binary[
                                             -(int_information_subwords_length - int_count_of_zeros):])
        else:
            list_informaion_subwords.append(string_input_text_binary[-int_information_subwords_length:])
    else:
        try:
            int_count_of_zeros = int_information_subwords_length - len(string_input_text_binary)
            list_informaion_subwords.append(('0' * int_count_of_zeros) + string_input_text_binary)
        except:
            show_error_message(13)
            return None
    print('Список информационных подслов:')
    for string_current_information_subword in list_informaion_subwords:
        print(string_current_information_subword)
    print()
    for string_current_information_subword in list_informaion_subwords:
        list_indices_of_1 = find_all_1(string_current_information_subword)
        string_current_code_subword = ''
        for int_current_index_of_column in range(int_code_subwords_length):
            int_current_bit = 0
            for int_current_index_of_row in range(len(list_generator_matrix)):
                if int_current_index_of_row in list_indices_of_1:
                    int_current_bit = int(ord(str(int_current_bit)) ^ ord(str(
                        list_generator_matrix[int_current_index_of_row][int_current_index_of_column])))
            string_current_code_subword += str(int_current_bit)
        list_code_subwords.append(string_current_code_subword)
    ui.TableWidgetCodeSubwordsOrigins.setRowCount(1)
    ui.TableWidgetCodeSubwordsOrigins.setColumnCount(len(list_code_subwords))
    ui.TableWidgetCodeSubwordsOrigins.verticalHeader().setVisible(False)
    ui.TableWidgetCodeSubwordsOrigins.horizontalHeader().setVisible(False)
    for int_counter_iteration in range(len(list_code_subwords)):
        ui.TableWidgetCodeSubwordsOrigins.setItem(0, int_counter_iteration,
                                                  QtWidgets.QTableWidgetItem(
                                                      str(list_code_subwords[int_counter_iteration])))
    for string_current_code_subword in list_code_subwords:
        list_submessages.append(error_processing(string_current_code_subword))
    ui.TableWidgetSubmessages.setRowCount(1)
    ui.TableWidgetSubmessages.setColumnCount(len(list_submessages))
    ui.TableWidgetSubmessages.verticalHeader().setVisible(False)
    ui.TableWidgetSubmessages.horizontalHeader().setVisible(False)
    for int_counter_iteration in range(len(list_submessages)):
        ui.TableWidgetSubmessages.setItem(0, int_counter_iteration,
                                                  QtWidgets.QTableWidgetItem(
                                                      str(list_submessages[int_counter_iteration])))
    string_message_text_binary = ''.join(list_submessages)
    ui.TextEditOutputBinaryTextOut.setText(string_message_text_binary)
    polynom_table_error_vector = poly('x**{}'.format(sympy.degree(polynom_generating)))
    _, polynom_table_error_syndrome = division_of_polynomials(polynom_table_error_vector, polynom_generating)
    print('Табличный вектор ошибки: {}'.format(polynom_table_error_vector.as_expr()))
    print('Табличный cиндром ошибки: {}'.format(polynom_table_error_syndrome.as_expr()))
    int_interation = 0
    list_new_information_subwords = []
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
