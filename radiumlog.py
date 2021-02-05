import openpyxl

#   Log to spreadsheet
def write(mdate, sername, mda, sens, act, days, disp_date):

    wb = openpyxl.load_workbook('radium_log.xlsx')
    ws = wb['radium']

    ws.append([mdate, sername, mda, sens, act, days, disp_date])

    wb.save('radium_log.xlsx')
