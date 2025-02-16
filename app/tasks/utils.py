from io import BytesIO
from typing import List

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment, Font

from app.db.models import Task


def draw_report_header(worksheet: Worksheet) -> None:
    headers = [
        "№", "Тип работ", "Диспетчерское наименование ОЭСХ", "Адрес объекта",
        "Дата работ по плану", "Класс напряжения, кВ", "Вид работ",
        "Дата выполнения",  "Широта", "Долгота", "фотофиксация 1", "фотофиксация 2",
        "фотофиксация 3", "фотофиксация 4", "фотофиксация 4",
        "Исполнитель", "Комментарий"
    ]
    set_header_row(worksheet, headers)
    set_column_sizes(worksheet)


def set_header_row(worksheet: Worksheet, headers: list[str]) -> None:
    alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    bold_font = Font(bold=True)

    for col, header in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=col, value=header)
        cell.alignment = alignment
        cell.font = bold_font

    worksheet.row_dimensions[1].height = 30


def set_column_sizes(worksheet: Worksheet) -> None:
    column_widths = {
        "A": 10, "B": 30, "C": 30, "D": 30, "E": 30,
        "F": 20, "G": 30, "H": 30, "I": 20, "J": 20,
        "K": 50, "L": 50, "M": 50, "N": 50, "O": 50,
        "P": 40, "Q": 60
    }

    for col, width in column_widths.items():
        worksheet.column_dimensions[col].width = width

    worksheet.row_dimensions[2].height = 30


def get_file_from_database(tasks: List[Task]) -> BytesIO:
    workbook = Workbook()
    worksheet = workbook.active
    draw_report_header(worksheet)
    for task in tasks:
        worksheet.append(
            (
                task.id,
				task.work_type,
                task.dispatcher_name,
                task.address,
                task.planner_date,
                task.voltage,
                task.job,
                task.completion_date,
                task.latitude,
                task.longitude,
                task.photo_url_1,
                task.photo_url_2,
				task.photo_url_3,
				task.photo_url_4,
				task.photo_url_5,
                task.supervisor,
                task.comments
            )
        )
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer