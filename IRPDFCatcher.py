import re
from pathlib import Path

import pandas as pd
import slate3k as slate

currentPath = Path(r'C:\desenv\Python\IR PDF Catcher\files') #Caminho para a pasta com os pdfs de I.R


def extract_data(file):
    rows = list()

    if file.is_file() and file.suffix == '.pdf':
        with open(file, 'rb') as f:
            document_text = slate.PDF(f).text()
            date = date_regex.findall(document_text)[2]

            for row in rows_regex.finditer(document_text):
                matched_group = f'{date} {row.group(1)}'
                replaced = re.sub('\s(PN|N[0-9]|CI|#|ON|ER|EJ|NM|EX|ED|EDJ)', '', matched_group)
                splitted = replaced.split(' ')
                rows.append(splitted)

    return rows



date_regex = re.compile('\d{2}\/\d{2}\/\d{4}')
rows_regex = re.compile('BOVESPA\s(.*?)\s[C,D]\s')
data = list()

for child in currentPath.iterdir():
    data += extract_data(child)

dt = pd.DataFrame(data, columns=['Data Pregão', 'C/V', 'Tipo de Mercado','Especificação do Título',  'Quantidade', 'Preço/Ajuste', 'Valor/Ajuste'])

dt.to_csv('ir.csv', sep=';', encoding='utf-8', index=False)
dt.to_excel('ir.xlsx', index=False)
