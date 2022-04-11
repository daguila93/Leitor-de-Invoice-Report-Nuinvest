from pathlib import Path
import slate3k as slate
import re
import csv

currentPath = Path.cwd()  # get the script`s current path


def getAllPDFTables(currentPath):
    linhas = []

    for child in currentPath.iterdir():
        if(child.is_file() and child.suffix == '.pdf'):

            with open(child, 'rb') as temp:
                regexData = re.compile("(\d{2}\/\d{2}\/\d{4})")
                regexLinhasTabela = re.compile("BOVESPA\s(.*?)\sD")
                texto = slate.PDF(temp).text()
                data = regexData.findall(texto)
                dataFinal = data[2]

                for match in regexLinhasTabela.finditer(texto):
                    row = f"{dataFinal};{match.group(1).replace(' ', ';')}"
                    filtered_row = re.sub("(BOVESPA;)|(PN;)|(N[0-9];)|(CI;)|(#;)|(ON;)|(ER;)|(NM;)|(EX;)|(;D)\b", '', row)
                    linhas.append(filtered_row)

    return linhas


with open(currentPath.joinpath('ir.csv'), 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, delimiter=';', fieldnames=["Data", "Compra/Venda", "À Vista/Fracionado", "Nome Ativo", "Quantidade", "Preço/Ajuste", "Valor/Ajuste"])
    writer.writeheader()
    writer = csv.writer(f, delimiter="\n")
    writer.writerow(getAllPDFTables(currentPath))
