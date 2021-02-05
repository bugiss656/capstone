import os
import re
import xlsxwriter
from .models import *

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_filenames():
    """
    Function returns a list of file names in 'saved_data' directory.
    """
    _, filenames = default_storage.listdir('saved_data')
    return [filename for filename in filenames]


def list_files_info():
    """
    Function returns a list of dictionaries for each file
    in 'saved_data' directory. Each file contains file name,
    created time and modified time.
    """
    _, filenames = default_storage.listdir('saved_data')
    files = [{'name': filename,
            'created': default_storage.get_created_time(f'saved_data/{filename}'),
            'modified': default_storage.get_modified_time(f'saved_data/{filename}')
            } for filename in filenames if re.search('^[a-z0-9]', filename)]

    return files


def save_as_excel_file(filename, data):
    """
    Function for saving data in Excel file, takes two arguments:
    filename which is a name of the saved file and data which is
    a list of dictionaries contains data to be saved in Excel file.
    """
    workbook = xlsxwriter.Workbook(f'{default_storage.location}/saved_data/{filename}.xlsx', {'default_date_format': 'dd/mm/yy', 'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0, len(data[0]), 20)

    bold = workbook.add_format({'bold': 1})

    header_row = 0
    header_col = 0

    for key, value in data[0].items():
        if key == 'temperature' or key == 'feels_like':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (\u00b0C)', bold)
            header_col += 1
        elif key == 'wind_speed':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (m/s)', bold)
            header_col += 1
        elif key == 'wind_direction':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (\u00b0)', bold)
            header_col += 1
        elif key == 'pressure':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (hPa)', bold)
            header_col += 1
        elif key == 'humidity':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (%)', bold)
            header_col += 1
        elif key == 'visibility':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (km)', bold)
            header_col += 1
        elif key == 'pm1' or key == 'pm25' or key == 'pm10':
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper() + ' (\u00B5g/cm\u00B3)', bold)
            header_col += 1
        else:
            worksheet.write(header_row, header_col, key.replace('_', ' ').upper(), bold)
            header_col += 1

    body_row = 1
    body_col = 0

    for item in data:
        for key, value in item.items():
            worksheet.write(body_row, body_col, value)
            body_col += 1
        body_row += 1
        body_col = 0

    workbook.close()


def open_file(filename):
    """
    Opens the file from 'saved_data' directory by name.
    """
    return os.startfile(os.path.abspath(f'saved_data/{filename}'))


def delete_file(filename):
    """
    Deletes the file from 'saved_data' directory by name.
    """
    return os.remove(os.path.abspath(f'saved_data/{filename}'))
