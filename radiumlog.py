import openpyxl

log_file = 'radium_log.xlsx'

#   Log to spreadsheet
def write(mdate, sername, window, mda, sens, act, days, disp_date):

    wb = openpyxl.load_workbook(log_file)
    ws = wb['radium']
    window_string = '{} - {}'.format(window[0], window[1])

    ws.append([mdate, sername, window_string, mda, sens, act, days, disp_date])

    wb.save(log_file)
