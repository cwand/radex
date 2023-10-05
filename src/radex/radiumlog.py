import openpyxl
from datetime import date

log_file = 'radium_log.xlsx'


#   Log to spreadsheet
def write_log(mdate: date, sername: str, mda: float, sens: float, act: float, days: float,
              disp_date: date):

    wb = openpyxl.load_workbook(log_file)
    ws = wb['radium']

    ws.append([mdate, sername, mda, sens, act, days, disp_date, date.today()])

    wb.save(log_file)
