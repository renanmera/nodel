import pandas as pd
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# Creating a new Sheet for working on it

"""
sheet_body = {
    'properties': {
        'title': 'Google Sheets For Nodel',
        'locale': 'en_US',
        'autoRecalc': 'ON_CHANGE',
        'timeZone': 'GMT-05:00'
        }
    ,
    'sheets': [
        {
            'properties': {
                'title': 'Data'
            }
        },
        {
            'properties': {
                'title': 'Pivot Table'
            }
        }
    ]
}

sheets_file = service.spreadsheets().create(
    body = sheet_body
).execute()
print(sheets_file['spreadsheetUrl'])
"""

# tried pivot table with pandas

"""
spreadsheet_id = '1HUo286Q-sWeRCk8gbzq2i_Whse5m-KTnYw3tf-woXwQ'

response = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    majorDimension = 'ROWS',
    range = 'Data'
).execute()

columns = response['values'][0]
data = response['values'][1:]
df = pd.DataFrame(data,columns=columns)

# Dataframe grouped for 2 indexes
df_grouped1 = df.groupby(['Author','Sentiment','Country']).count()
df_grouped2 = df.groupby(['Author','Sentiment','Theme']).count()

df_grouped1.pivot_table(index=['Author','Sentiment'],columns=['Country'],fill_value=0)
df_grouped2.pivot_table(index=['Author','Sentiment'],columns=['Theme'],fill_value=0)

"""

# PivotTable JSON Template

spreadsheet_id = '1HUo286Q-sWeRCk8gbzq2i_Whse5m-KTnYw3tf-woXwQ'

request_body = {
    'requests': [
        {
            'updateCells': {
                'rows': {
                    'values': [
                        {
                            'pivotTable': {
                                # Data Source
                                'source': {
                                    'sheetId': '333276127',
                                    'startRowIndex': 0,
                                    'startColumnIndex': 0,
                                    'endRowIndex': 16,
                                    'endColumnIndex': 4
                                },
                                
                                # Rows Field(s)
                                'rows': [
                                    # row field #1
                                    {
                                        'sourceColumnOffset': 0,
                                        #'showTotals': False, 
                                        'sortOrder': 'ASCENDING',
                                        #'repeatHeadings': False,
                                        #'label': 'Country',
                                    },
                                    # row field #2
                                    {
                                        'sourceColumnOffset': 1,
                                        #'showTotals': False, 
                                        'sortOrder': 'ASCENDING',
                                        #'repeatHeadings': False,
                                        #'label': 'Country',
                                    }
                                ],

                                # Columns Field(s)
                                'columns': [
                                    # column field #1
                                    {
                                        'sourceColumnOffset': 2,
                                        'sortOrder': 'ASCENDING', 
                                        #'showTotals': False
                                    },
                                    # column field #2
                                    {
                                        'sourceColumnOffset': 3,
                                        'sortOrder': 'ASCENDING',
                                        #'repeatHeadings': False, 
                                        #'showTotals': False
                                    }
                                ],

                                # Values Field(s)
                                'values': [
                                    # value field #1
                                    {
                                        #'sourceColumnOffset': 2,
                                        'summarizeFunction': 'CUSTOM',
                                        #'default': '=False',
                                        'formula' : '=True'
                                        #'name': 'Profit Total:'
                                    }
                                ],

                                'valueLayout': 'HORIZONTAL'
                            }
                        }
                    ]
                },
                
                'start': {
                    'sheetId': '216286515',
                    'rowIndex': 0, 
                    'columnIndex': 0 
                },
                'fields': 'pivotTable'
            }
        }
    ]
}

response = service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body=request_body
).execute()
