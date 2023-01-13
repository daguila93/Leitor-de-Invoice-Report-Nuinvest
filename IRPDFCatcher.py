import os
import re
from pathlib import Path
import pandas as pd
import slate3k as slate

regex = "nota (.{0,}) Data"

pathname = os.curdir
separador = os.path.sep
allFiles = os.listdir(pathname)

for file in allFiles:
    fpath = pathname + separador + file
    if (os.path.isfile(fpath) and file.endswith('.pdf')):
        print(file)
        with open(fpath, 'rb') as realFile:
            df = slate.PDF(realFile)
            invoiceNumber = re.findall(regex, str(df.text()))

            if(len(invoiceNumber) != 0):
                print(invoiceNumber)

                realFile.close()

                os.rename(fpath, pathname + separador + invoiceNumber[0] + ".pdf");

currentPath = Path(os.curdir)


def extract_data(file):
    rows = list()

    if file.is_file() and file.suffix == '.pdf':
        with open(file, 'rb') as f:
            document_text = slate.PDF(f).text()
            date = date_regex.findall(document_text)[2]
            invoice = invoice_number.findall(document_text)[0]

            for row in rows_regex.finditer(document_text):
                matched_group = f'{invoice} {date} {row.group(1)}'
                replaced = re.sub('\s(PN|N[0-9]|CI|#|ON|ER|EJ|NM|EX|EDJ|ED)', '', matched_group)
                splitted = replaced.split(' ')
                rows.append(splitted)

    return rows


date_regex = re.compile('\d{2}\/\d{2}\/\d{4}')
invoice_number = re.compile('nota (.{0,}) Data')
rows_regex = re.compile('BOVESPA\s(.*?)\s[C,D]\s')
data = list()

for child in currentPath.iterdir():
    data += extract_data(child)

dt = pd.DataFrame(data, columns=['Nota de Negociação', 'Data Pregão', 'C/V', 'Tipo de Mercado','Especificação do Título',  'Quantidade', 'Preço/Ajuste', 'Valor/Ajuste'])

dt.to_csv('ir.csv', sep=';', encoding='utf-8', index=False)
dt.to_excel('ir.xlsx', index=False)
