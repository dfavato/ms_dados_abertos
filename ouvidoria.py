import argparse
import pyexcel
import json
import html
from bs4 import BeautifulSoup

INDEX_FIELD = 'Número de Protocolo'
CABECALHO_PLANILHA = [
    INDEX_FIELD,
    'Data do Pedido',
    'Texto do Pedido',
    'DataRegistro',
    'Texto da Resposta'
]

def excel_to_json(input_file, output_file):
    records = pyexcel.get_records(file_name=input_file)
    d = dict()
    index_d = dict()
    separators = (',', ':')
    with open(output_file, 'w') as outfile:
        for record in records:
            index_d['index'] = {'_id': record[INDEX_FIELD]}
            d['data_pedido'] = record['Data do Pedido']
            d['texto_pedido'] = record['Texto do Pedido']
            d['data_registro'] = record['DataRegistro']
            d['texto_resposta'] = BeautifulSoup(html.unescape(record['Texto da Resposta']), 'html.parser').get_text()
            json.dump(index_d, outfile, separators=separators)
            outfile.write('\n')
            json.dump(d, outfile, separators=separators)
            outfile.write('\n')
    pyexcel.free_resources()
    

def check_header(header):
    """Checa se a primeira linha da planilha corresponde ao CABECALHO_PLANILHA"""
    for cabecalho in CABECALHO_PLANILHA:
        if not (cabecalho in header):
            Raise(Exception('A planilha não contém a coluna %s.' % cabecalho))

def check_file(file_path):
    """Checa se:
        1) o arquivo existe
        2) é um arquivo excel e
        3) possui as colunas necessárias
    """
    try:
        sheet_array = pyexcel.iget_array(file_name=file_path)
    except FileNotFoundError as e:
        raise(Exception(
            ('Não foi possível encontrar o arquivo %s, '
            'verifique se o local está correto') % file_path
        ))
        pyexcel.free_resources()
    except FileTypeNotSupported as e:
        raise(Exception(
            ('O arquivo %s não é suportado, '
             'os formatos suportados são: xls e xlsx') % file_path
        ))
        pyexcel.free_resources()
    header = sheet_array.__next__()
    check_header(header)
    print('File ok!')
    pyexcel.free_resources()


if __name__ == '__main__':
    """Para que o script funcione é necessário informar o caminho do arquivo
    que ficará guardado na variável args.file_path
    """
    parser = argparse.ArgumentParser(
        description='Pré processamento do arquivo da ouvidoria',
        usage=('Forneça o caminho de um arquivo Excel que contém os dados')
    )
    parser.add_argument('file_path', type=str, help='Local do arquivo da ouvidoria')
    args = parser.parse_args()
    check_file(args.file_path)
    excel_to_json(args.file_path, 'output.json')
    print('"output.json" gerado.')


