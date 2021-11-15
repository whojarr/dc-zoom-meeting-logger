import os
import json
import boto3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import GSpreadException


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

GOOGLE_AUTH_JSON = os.environ['GOOGLE_AUTH_JSON']
                        
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(GOOGLE_AUTH_JSON), scope)
gc = gspread.authorize(credentials)

s3 = boto3.resource('s3')


def googlesheet_allvalues2dict(rows):
    result = []
    heading_count = len(rows[0])
    for row in rows[1:]:
        row_dict = googlesheet_headings2dict(rows[0])
        i = 0
        while i < heading_count:
            row_dict[rows[0][i]] = row[i]
            i += 1
        result.append(row_dict)

    return result


def googlesheet_create():
    pass


def googlesheet_exists():
    pass


def googlesheet_headings2dict(headings):
    result = {}
    for heading in headings:
        result["{}".format(heading)] = None;
    return result


def googlesheet_row_add():
    pass


def googlesheet_update(sheet_name, worksheet_name, row):
    
    """ get the tabs and create one for the meeting title if not present """
    try:
        sh = gc.open(sheet_name)
        worksheet_list = sh.worksheets()
        current_sheet = None
        for worksheet in worksheet_list:
            if worksheet.title == worksheet_name:
                current_sheet = worksheet
        if not current_sheet:
            current_sheet = sh.add_worksheet(title=worksheet_name, rows="100", cols="20")
            headings = ["Meeting","Status","Timezone","Start Date","End Date","Duration","Account ID","Host ID","Subject","Type","ID","UUID","User Name","Email","Joined Date","Left Date","User ID","Participant ID"]
            current_sheet.append_row(headings, value_input_option='USER_ENTERED', insert_data_option=None, table_range='A1')

    except gspread.exceptions.SpreadsheetNotFound:
        return "sheet not found. ensure exists and is shared correctly"

    """ create a new row and insert it """
    current_sheet.append_row(row, value_input_option='USER_ENTERED', insert_data_option=None, table_range='A1')

    return current_sheet, row



def googlesheet2s3(sheet, bucket, key_prefix,):
    sheet = gc.open(sheet)
    worksheet_list = sheet.worksheets()
    stored_worksheets = []
    for ws in worksheet_list:
        print("worksheet: {}".format(ws.title))
        key = "{}{}.json".format(key_prefix, ws.title)
        worksheet = sheet.worksheet(ws.title)
        rows = worksheet.get_all_values()
        rows_dict = googlesheet_allvalues2dict(rows)
        rows_json = json.dumps(rows_dict)
        s3.Object(bucket, key).put(Body=rows_json)
        stored_worksheets.append(ws.title)
    return "Stored worksheet as {}".format(stored_worksheets)