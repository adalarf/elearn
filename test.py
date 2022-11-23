import csv
import re
import os
from prettytable import PrettyTable


dic_naming = {'name': 'Название',
            'description': 'Описание',
            'key_skills': 'Навыки',
            'experience_id': 'Опыт работы',
            'premium': 'Премиум-вакансия',
            'employer_name': 'Компания',
            'Оклад': 'Оклад',
            'area_name': 'Название региона',
            'published_at': 'Дата публикации вакансии'}

def csv_reader(file_name):
    with open(file_name, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        if os.stat(file_name).st_size == 0:
            return 'Пустой файл'
        headlines = next(reader)
        vacancies = []
        for row in csv.reader(file):
            if len(headlines) != len(row) or '' in row:
                continue
            vacancies.append(row)
        return [headlines, vacancies]

def formatter(row):
    work_experience = {"noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"}

    currency = {"AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"}

    dic = {}
    for key in row.keys():
        if key == 'salary_to':
            salary_from = format_int(row["salary_from"])
            salary_to = format_int(row[key])
            if row['salary_gross'] == 'Да':
                dic.update({'Оклад':f'{salary_from[0]} {salary_from[1]} - {salary_to[0]} {salary_to[1]} ({currency[row["salary_currency"]]}) (Без вычета налогов)'})
                continue
            else:
                dic.update({'Оклад':f'{salary_from[0]} {salary_from[1]} - {salary_to[0]} {salary_to[1]} ({currency[row["salary_currency"]]}) (С вычетом налогов)'})
                continue
        elif key == 'salary_gross' or key == 'salary_currency' or key == 'salary_from':
            continue
        if key == 'experience_id':
            dic.update({key: work_experience[row[key]]})
            continue
        if key == 'published_at':
            data = f'{row[key][8:10]}.{row[key][5:7]}.{row[key][0:4]}'
            dic.update({key: data})
            continue
        else:
            dic.update({key: row[key]})
    return dic

def format_int(num):
    formatted = num.split('.')[0]
    return [formatted.replace(formatted[-3:], ''), formatted[-3:]]

def print_vacancies(data_vacancies, dic_naming, string_number, row_number):
    table = PrettyTable()
    vacancies_values = []
    for vacancy in data_vacancies:
        updated = formatter(vacancy)
        for key in updated.keys():
            updated[key] = ' '.join(updated[key].split())
            if key == 'key_skills':
                updated[key] = updated[key].replace(', ', '\n')
            if len(updated[key]) >= 100:
                updated[key] = f'{updated[key][:100]}...'
            vacancies_values.append(updated[key])
    for i in range(1, len(vacancies_values)):
        try:
            table.add_row(vacancies_values[9 * i - 9:9 * i])
        except:
            break
    table.field_names = dic_naming.values()
    table.add_autoindex('№')
    table.align = 'l'
    table.max_width = 20
    table.hrules = 1
    table.get_string()
    row_number = row_number.split(', ')
    if row_number[0] == '':
        row_number = table.field_names
    else:
        row_number.insert(0,'№')
    string_number = string_number.split(' ')
    if len(string_number) == 1 and string_number[0] != '':
        print(table.get_string(fields=row_number, start=int(string_number[0]) - 1))
    elif len(string_number) == 2:
        print(table.get_string(fields=row_number, start=int(string_number[0]) - 1,
                               end=int(string_number[1]) - 1))
    else:
        print(table.get_string(fields=row_number))

def csv_filer(reader, list_naming):
    vacancies_list = []
    for i in range(len(reader)):
        j = 0
        vacancy_dict= {}
        for elements in reader[i]:
            value = re.sub(r'<.*?>', '', ', '.join(elements.split('\n')))
            if value == 'True':
                value = 'Да'
            elif value == 'False':
                value = 'Нет'
            fillable_data = {list_naming[j]: value}
            vacancy_dict.update(fillable_data)
            j += 1
        vacancies_list.append(vacancy_dict)
    return vacancies_list

input_data=[]
for i in range(3):
    input_data.append(''.join(input().split('\n')))
file_name = input_data[0]
string_number = input_data[1]
row_number = input_data[2]
headlines_and_vacancies = csv_reader(file_name)
if headlines_and_vacancies == 'Пустой файл':
    print(headlines_and_vacancies)
else:
    reader = headlines_and_vacancies[1]
    list_naming = headlines_and_vacancies[0]
    if len(reader) == 0:
        print('Нет данных')
    else:
        data_vacancies = csv_filer(reader, list_naming)
        print_vacancies(data_vacancies, dic_naming, string_number, row_number)