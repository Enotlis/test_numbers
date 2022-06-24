import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import db
from datetime import datetime

def get_google_sheet(spreadsheet_id: str)->tuple:
    '''Получение строк из таблицы Google Sheets'''
    creds_json = "creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes)
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:Z9999',
        majorDimension='ROWS'
    ).execute()
    
    return tuple(tuple(row[1:]) for row in values['values'])

def get_dollar_rate()->float:
    '''Получение круса доллара(текущего дня) с сайта ЦБ'''
    data = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    data_soup = BeautifulSoup(data.text, 'html.parser')
    exchange_rate_dollar = data_soup.find('valute', id='R01235').find('value').text
    return float(exchange_rate_dollar.replace(',', '.'))

def update_rows_to_db(spreadsheet_id: str,
                      last_version_sheets: tuple)->tuple:
    '''Извлечение обновлений из Google Sheets
        и добление их в таблице'''
    rows = get_google_sheet(spreadsheet_id)
    exchange_rate_dollar = get_dollar_rate()

    #Получаем изменения которые произошли в таблице с последнего просмотра 
    changes_rows = tuple(set(rows).difference(set(last_version_sheets)))

    conn = db.connect_db()
    cursor = conn.cursor()

    for row in changes_rows:
        cursor.execute(f"SELECT EXISTS (SELECT * FROM orders WHERE number_order = {row[0]})")
        result = cursor.fetchone()
        if result[0]:
            db.update('orders',{
                'price_usd':int(row[1]),
                'price_rub':round(float(row[1])*exchange_rate_dollar,2),
                'delivery_time':datetime.strptime(row[2], '%d.%m.%Y'),
                'number_order':int(row[0])
            })
        else:
            db.insert('orders',
                  {'number_order':int(row[0]),
                   'price_usd':int(row[1]),
                   'price_rub':round(float(row[1])*exchange_rate_dollar,2),
                   'delivery_time':datetime.strptime(row[2], '%d.%m.%Y')
            })                     
                                   
    conn.close()
    return rows

def main():
    spreadsheet_id = '1vhzenzhDNAkQCeOmqjDDfFazrTNIwdZljgQzG_xZvQw'
    last_version_sheets = tuple()

    while True:
        last_version_sheets = update_rows_to_db(spreadsheet_id,
                                                last_version_sheets)

if __name__ == '__main__':
    main()
