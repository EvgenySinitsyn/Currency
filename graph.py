import requests
from xml.etree import ElementTree as ET

CURRENCIES = {
    'USD': 'R01235',
    'EUR': 'R01239',
    'CNY': 'R01375',
}


def parse_history(curr, date_begin, date_end):
    """ Получение данных ЦБ об истории курсов """
    url = f'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_begin}&date_req2={date_end}&VAL_NM_RQ={CURRENCIES[curr]}'
    try:
        page = requests.get(url).text
        print(page)

        tree = ET.fromstring(page)
        dates = []
        values = []
        for i in tree.findall("Record"):
            values.append(round(float(i.find("Value").text.replace(',', '.')) / int(i.find("Nominal").text), 4))
            dates.append(i.attrib["Date"])

        return values, dates
    except:
        return "Нет интернета или сработала защита от Ddos"


