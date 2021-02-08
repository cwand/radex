import openpyxl

log_file = 'radium_log.xlsx'

#   Log to spreadsheet
def write(mdate, sername, mda, sens, act, days, disp_date):

    wb = openpyxl.load_workbook(log_file)
    ws = wb['radium']

    ws.append([mdate, sername, mda, sens, act, days, disp_date])

    wb.save(log_file)
