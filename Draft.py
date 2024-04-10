import sympy
import re
import math
import random
from sympy import poly

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
    return poly(string_polynom[:-3], symbol_x)
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    if int(string_bit): return '0'
    else: return '1'
def error_processing(string_current_code_subword: str) -> str:
    '''Внесение/исправление ошибок в текущем кодовом подслове'''
    list_indices_of_1 = find_all_1(string_current_code_subword)
    if len(list_indices_of_1) == 0: return string_current_code_subword
    elif len(list_indices_of_1) > 1: int_position_of_error = random.randint(0, len(string_current_code_subword) - 1)
    else:
        while True:
            int_position_of_error = random.randint(0, len(string_current_code_subword) - 1)
            if int_position_of_error != list_indices_of_1[0]: break
    return (string_current_code_subword[:int_position_of_error] + changing_the_bit(string_current_code_subword[int_position_of_error]) +
        string_current_code_subword[int_position_of_error + 1:])
def find_all_1(string_search_base: str) -> list:
    '''Нахождение индексов 1 в строке'''
    list_indices_of_1 = []
    for int_index, string_current_number in enumerate(string_search_base):
        if string_current_number == '1': list_indices_of_1.append(int_index)
    return list_indices_of_1
def division_of_polynomials(polynom_dividend: sympy.Poly, polynom_divider: sympy.Poly) -> (sympy.Poly, sympy.Poly):
    '''Деление полиномов'''
    polynom_dividend = sympy.poly(polynom_dividend, symbol_x, domain='GF(2)')
    polynom_divider = sympy.poly(polynom_divider, symbol_x, domain='GF(2)')
    polynom_quotient, polynom_remainder = sympy.div(polynom_dividend, polynom_divider, symbol_x)
    return polynom_quotient, polynom_remainder
def checking_the_polynomial_generation_line(string_polynom_generating: str) -> bool:
    '''Проверка корректности вводимой строки генерации полинома'''
    list_checking = string_polynom_generating.split(' ')
    print(list_checking)
    if (len(list_checking) - 1) % 2 != 0:
        print(1)
        return False
    else:
        for int_index, string_element in enumerate(list_checking):
            if int_index % 2 == 0 or int_index == 0:
                if string_element in ['x', '1']: pass
                elif re.fullmatch('x\*\*\d', string_element): pass
                else:
                    print(2)
                    return False
            elif string_element != '+':
                print(3)
                return False
        return True

bool_polynom_choise = bool(int(input('Введите 1, в случае ввода полинома: ')))
symbol_x = sympy.symbols('x')
if bool_polynom_choise:
    int_code_subwords_length = int(input('Введите длину кодовых подслов: '))
    string_polynom_generating = input('Введите порождающий полином: ')
    if checking_the_polynomial_generation_line(string_polynom_generating) and len(string_polynom_generating) != 0:
        if string_polynom_generating in ['x', '1']:
            print('Некорректный ввод.')
            exit(666)
        try: polynom_generating = poly(string_polynom_generating, symbol_x)
        except:
            print('Некорректный ввод.')
            exit(666)
        int_information_subwords_length = int_code_subwords_length - sympy.degree(polynom_generating)
        if sympy.degree(polynom_generating) >= int_code_subwords_length - 1: exit(666)
        list_polynom_dergees = [tuple_current_degree[0] for tuple_current_degree in polynom_generating.as_dict().keys()]
        string_matrix_first_string = '0' * int_code_subwords_length
        for int_current_polynom_degree in list_polynom_dergees:
            string_matrix_first_string = (string_matrix_first_string[:int_current_polynom_degree] + '1' +
                                          string_matrix_first_string[int_current_polynom_degree + 1:])
        list_generator_matrix = creating_generator_matrix(list(string_matrix_first_string))
    else:
        print('Некорректный ввод.')
        exit(666)
else:
    string_input_first_string = input('Введите 1-ю строку матрицы: ')
    if not re.fullmatch('[10]*', string_input_first_string):
        print('Некорректный ввод.')
        exit(666)
    int_code_subwords_length = len(string_input_first_string)
    int_information_subwords_length = int_code_subwords_length - string_input_first_string.rfind('1')
    list_generator_matrix = creating_generator_matrix(list(string_input_first_string))
    polynom_generating = creating_polynom(string_input_first_string)
print('Порождающая матрица: ')
for l in list_generator_matrix:
    print(l)
print()
print('Порождающий полином: {}'.format(polynom_generating.as_expr()))
string_input_text_real = input('Введите входное сообщение: ')
string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
print('Бинарный формат входного текста: {}'.format(string_input_text_binary))
list_informaion_subwords, list_code_subwords, list_submessages = [], [], []
int_count_of_zeros = 0
if len(string_input_text_binary) > int_information_subwords_length:
    for int_iteration in range(1, math.ceil(len(string_input_text_binary) / int_information_subwords_length)):
        list_informaion_subwords.append(string_input_text_binary[int_iteration * int_information_subwords_length -
                                                                 int_information_subwords_length:int_iteration * int_information_subwords_length])
    if len(string_input_text_binary) % int_information_subwords_length != 0:
        int_count_of_zeros = int_information_subwords_length - (len(string_input_text_binary) -
                                            (int_information_subwords_length * (len(string_input_text_binary) // int_information_subwords_length)))
        list_informaion_subwords.append(
            ('0' * int_count_of_zeros) + string_input_text_binary[-(int_information_subwords_length - int_count_of_zeros):])
    else:
        list_informaion_subwords.append(string_input_text_binary[-int_information_subwords_length:])
else:
    try:
        int_count_of_zeros = int_information_subwords_length - len(string_input_text_binary)
        list_informaion_subwords.append(('0' * int_count_of_zeros) + string_input_text_binary)
    except:
        exit(666)
print('Список информационных подслов:')
for l in list_informaion_subwords:
    print(l)
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
print('Список кодовых подслов:')
for l in list_code_subwords:
    print(l)
print()
for string_current_code_subword in list_code_subwords:
    list_submessages.append(error_processing(string_current_code_subword))
print('Список подслов сообщения:')
for l in list_submessages:
    print(l)
print()
string_message_text_binary = ''.join(list_submessages)
print('Сообщение в бинарном формате: {}'.format(string_message_text_binary))
polynom_table_error_vector = poly('x**{}'.format(sympy.degree(polynom_generating)))
_, polynom_table_error_syndrome = division_of_polynomials(polynom_table_error_vector, polynom_generating)
print('Табличный вектор ошибки: {}'.format(polynom_table_error_vector.as_expr()))
print('Табличный cиндром ошибки: {}'.format(polynom_table_error_syndrome.as_expr()))
int_interation = 0
list_new_information_subwords = []
for string_current_submessage in list_submessages:
    print('\nТекущее подсообщение: {}'.format(string_current_submessage))
    if len(find_all_1(string_current_submessage)) == 0:
        print('Текущее подслово сообщения: {}'.format(string_current_submessage))
        string_current_information_subword = string_current_submessage[:int_information_subwords_length]
    else:
        polynom_current_submessage = creating_polynom(string_current_submessage)
        _, polynom_0_error_syndrome = division_of_polynomials(polynom_current_submessage, polynom_generating)
        if polynom_0_error_syndrome == 0: pass
        else:
            if polynom_0_error_syndrome == polynom_table_error_syndrome:
                polynome_current_error_vector = polynom_table_error_vector
            else:
                int_index_of_alignment = 0
                polynom_current_error_syndrome = polynom_0_error_syndrome
                while True:
                    _, polynom_current_error_syndrome = division_of_polynomials(polynom_current_error_syndrome.mul(poly('x')), polynom_generating)
                    int_index_of_alignment += 1
                    if int_index_of_alignment > int_code_subwords_length - 1:
                        print('Не найден текущий синдром. Конец работы алгоритма.')
                        exit(13)
                    if polynom_current_error_syndrome == polynom_table_error_syndrome: break
                _, polynome_current_error_vector = division_of_polynomials(
                    poly('x**{}'.format(int_code_subwords_length - int_index_of_alignment), symbol_x).mul(polynom_table_error_vector),
                    poly('x**{} - 1'.format(int_code_subwords_length), symbol_x))
                print('Итерация совпадения синдромов: {}'.format(int_index_of_alignment))
            print('Текущий вектор ошибки: {}'.format(polynome_current_error_vector.as_expr()))
            if polynome_current_error_vector.as_expr() == 1:
                if string_current_submessage[0] == '1': polynom_current_submessage = creating_polynom('0' + string_current_submessage[1:])
            else:
                dictionary_current_error_vector, dictionary_current_submessage = polynome_current_error_vector.as_dict(), polynom_current_submessage.as_dict()
                for tuple_current_degree in dictionary_current_error_vector.keys():
                    if tuple_current_degree in dictionary_current_submessage.keys() and (dictionary_current_error_vector[tuple_current_degree] +
                                                                    dictionary_current_submessage[tuple_current_degree]) % 2 == 0:
                        polynom_current_submessage = polynom_current_submessage - poly('x**{}'.format(str(tuple_current_degree[0])))
                    elif tuple_current_degree not in dictionary_current_submessage.keys():
                        polynom_current_submessage = polynom_current_submessage + poly( 'x**{}'.format(str(tuple_current_degree[0])))
            print('Текущее подсообщение с исправленной ошибкой: {}'.format(polynom_current_submessage.as_expr()))
        polynom_current_information_subword, polynom_remainder = division_of_polynomials(polynom_current_submessage, polynom_generating)
        if polynom_remainder != 0: print('В текущем блоке допущена ошибка!')
        print('Текущий полином информационного подслова: {}'.format(polynom_current_information_subword.as_expr()))
        string_current_information_subword = ''.join(str(current_number) for current_number in polynom_current_information_subword.as_list())
        string_current_information_subword = string_current_information_subword[::-1]
        if len(string_current_information_subword) < int_information_subwords_length:
            string_current_information_subword += '0' * (int_information_subwords_length - len(string_current_information_subword))
    list_new_information_subwords.append(string_current_information_subword)
    print('Текущее декодированное информационное подслово: {} <-> {}'.format(string_current_information_subword,
                                                                             list_informaion_subwords[int_interation]))
    int_interation += 1
if int_count_of_zeros > 0: list_new_information_subwords[-1] = list_new_information_subwords[-1][int_count_of_zeros:]
string_output_text_binary = ''.join(list_new_information_subwords)
print('\nБинарный формат декодированного сообщения: {}'.format(string_output_text_binary))
print('Бинарный формат входного сообщения: {}'.format(string_input_text_binary))
try:
    string_output_text_real = int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8, 'big').decode()
    print('Декодированное сообщение: {}'.format(string_output_text_real))
except:
    print('Алгоритм отработал некорректно.')
    exit(13)


# import sympy
# x = sympy.symbols('x')
# q, r = sympy.div('x**4', 'x**4 + x**3 + x**2 + x + 1', x)
# print(q, r)
# 1 -x**3 - x**2 - x - 1
# print(sympy.poly(r).abs())
# Poly(x**3 + x**2 + x + 1, x, domain='ZZ')
# ost = sympy.poly(r).abs()
# print(str(ost.as_expr()))
# x**3 + x**2 + x + 1