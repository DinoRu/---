from io import BytesIO

from openpyxl.workbook import Workbook

from app.models.tasks import Task
from app.utils.draw_excel_table import draw_report_header


def get_file_from_database(tasks: list[Task]) -> BytesIO:
    workbook = Workbook()
    worksheet = workbook.active
    draw_report_header(worksheet)
    for task in tasks:
        worksheet.append(
            (
                task.code,
                task.dispatcher_name,
                task.location,
                task.planner_date,
                task.voltage_class,
                task.work_type,
                task.completion_date,
                task.photo_url_1,
                task.photo_url_2,
                task.supervisor,
                task.comments
            )
        )
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer