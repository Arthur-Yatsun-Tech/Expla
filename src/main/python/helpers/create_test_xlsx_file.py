from openpyxl import Workbook

experiment_data = [
    [0.52, 0.56, 0.56, 0.58, 0.58, 0.56, 0.54, 0.60, 0.59, 0.55, 0.59, 0.55, 0.55, 0.60, 0.55, 0.58],
    [0.52, 0.56, 0.55, 0.57, 0.58, 0.58, 0.54, 0.58, 0.56, 0.55, 0.61, 0.54, 0.56, 0.63, 0.55, 0.58],
]

workbook = Workbook()
sheet = workbook.active


for values in zip(*experiment_data):
    sheet.append(values)

workbook.save('./../test_xlsx_files/chemicals.xlsx')
