import time
import datetime
import json
import openpyxl


def read_data(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def wright_data(file: str, data: dict) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_project(file: str) -> None:
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    project_name = sheet['A2'].value
    knots_name = []
    knots_num = []

    for i in sheet['A:A'][5:]:
        i = i.value
        if i is not None:
            knots_num.append(i)

    for i in sheet['C:C'][5:]:
        i = i.value
        if i is not None:
            knots_name.append(i)

    data = read_data('projects_list.json')
    data[project_name] = knots_name
    wright_data('projects_list.json', data)


load_project('tabel.xlsx')
