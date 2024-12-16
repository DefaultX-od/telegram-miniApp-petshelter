from spire.xls import Workbook

wb = Workbook()
ws = wb.worksheets.add("Test")
ws.range("A1").value = "Hello, Server!"
wb.save_to_file("test.xlsx")