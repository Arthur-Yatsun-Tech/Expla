import argparse

from openpyxl import Workbook


def create_chemicals_sample_file():
    experiment_data = [
        [0.52, 0.56, 0.56, 0.58, 0.58, 0.56, 0.54, 0.60, 0.59, 0.55, 0.59, 0.55, 0.55, 0.60, 0.55, 0.58],
        [0.52, 0.56, 0.55, 0.57, 0.58, 0.58, 0.54, 0.58, 0.56, 0.55, 0.61, 0.54, 0.56, 0.63, 0.55, 0.58],
    ]

    workbook = Workbook()
    sheet = workbook.active
    # add by rows
    for values in zip(*experiment_data):
        sheet.append(values)

    workbook.save('./../test_xlsx_files/chemicals.xlsx')


def create_test_data_sample_file():
    experiment_data = [
        [0.03245, 0.05539, 0.3451, 0.05561, 0.03868, 0.06334, 0.04001, 0.6338, 0.18186, 0.26323, 0.17555, 0.26309, 0.22666, 0.30911, 0.20691, 0.2928],
        [0.03127, 0.05133, 0.3255, 0.05327, 0.03775, 0.05789, 0.0423, 0.06412, 0.17642, 0.26265, 0.17157, 0.26409, 0.22618, 0.30535, 0.20985, 0.28617],
        [0.03165, 0.05355, 0.033, 0.05456, 0.03827, 0.06167, 0.0391, 0.06825, 0.17814, 0.2629, 0.17358, 0.26356, 0.2263, 0.31006, 0.2084, 0.2844]
    ]

    workbook = Workbook()
    sheet = workbook.active
    # add by rows
    for values in zip(*experiment_data):
        sheet.append(values)

    workbook.save('./../test_xlsx_files/exp_data.xlsx')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="Created data type")

    args = parser.parse_args()

    data_type = args.type
    if data_type == "chemicals":
        create_chemicals_sample_file()
    elif data_type == "test":
        create_test_data_sample_file()

