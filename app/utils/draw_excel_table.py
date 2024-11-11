from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment, Font


def draw_report_header(worksheet: Worksheet) -> None:
	headers = [
		"Код", "Диспетчерское наименование ОЭСХ", "Населенный пункт",
		"Дата по плану", "Класс напряжения", "Вид работ",
		"Дата выполнения", "Координаты х (долгота)", "Координаты у (широта)",
		"Фото 1", "Фото 2", "Исполнитель", "Комментарий"
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
		"A": 30, "B": 50, "C": 50, "D": 40, "E": 50,
		"F": 40, "G": 50, "H": 50, "I": 50, "J": 50,
		"K": 50, "L": 40
	}

	for col, width in column_widths.items():
		worksheet.column_dimensions[col].width = width

	worksheet.row_dimensions[2].height = 30