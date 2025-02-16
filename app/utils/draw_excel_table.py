from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment, Font


def draw_report_header(worksheet: Worksheet) -> None:
	headers = [
		"№", "Тип работ", "Диспетчерское наименование ОЭСХ", "Адрес объекта",
		"Дата работ по плану", "Класс напряжения, кВ", "Вид работ",
		"Дата выполнения", "Широта", "Долгота", "фотофиксация 1", "фотофиксация 2",
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
		"A": 20, "B": 30, "C": 30, "D": 30, "E": 10,
		"F": 50, "G": 30, "H": 20, "I": 50, "J": 50,
		"K": 50, "L": 50, "M": 50, "N": 50, "O": 50,
		"P": 30, "Q": 30
	}

	for col, width in column_widths.items():
		worksheet.column_dimensions[col].width = width

	worksheet.row_dimensions[2].height = 30