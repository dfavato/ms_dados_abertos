import argparse
import pyexcel
import json
import html
from slugify import slugify
from bs4 import BeautifulSoup

tipos_arquivos = {
    'simples': {
        'index_field': 'Número de Protocolo',
        'cabecalho': [
            'Número de Protocolo',
            'Data do Pedido',
            'Texto do Pedido',
            'DataRegistro',
            'Texto da Resposta'
        ]
    },
    'completo': {
        'index_field': 'PROTOCOLO',
        'cabecalho': [
            'OUVIDORIA DE ORIGEM',
            'MUNICIPIO ORIGEM',
            'UF ORIGEM',
            'ESFERA ORIGEM',
            'PROTOCOLO',
            'MEIO DE ATENDIMENTO',
            'ORIGEM DO ATENDIMENTO',
            'DEMANDA ATIVA (S/N)',
            'DATA DA DEMANDA',
            'DATA PREVISTA PARA CONCLUSAO',
            'DATA DO FECHAMENTO',
            'CLASSIFICACAO',
            'ASSUNTO',
            'SUBASSUNTO 1',
            'SUBASSUNTO 2',
            'SUBASSUNTO 3',
            'FARMACO',
            'DAPS',
            'ESTABELECIMENTO COMERCIAL',
            'PRIMEIRO DESTINO',
            'MUNICIPIO PRIMEIRO DESTINO',
            'UF PRIMEIRO DESTINO',
            'DESTINO ATUAL',
            'MUNICIPIO DESTINO ATUAL',
            'UF DESTINO ATUAL',
            'STATUS ACOMPANHAMENTO',
            'DATA DO ACOMPANHAMENTO',
            'MUNICIPIO CIDADAO',
            'BAIRRO CIDADAO',
            'CEP CIDADAO',
            'UF CIDADAO',
            'SIGILOSO (S/N)',
            'ANONIMO (S/N)',
            'DETALHE DA DEMANDA',
            'OUVIDORIA RESPOSTA',
            'TIPO OUVIDORIA RESPOSTA',
            'MUNICIPIO OUVIDORIA RESPOSTA',
            'UF OUVIDORIA  RESPOSTA',
            'ESFERA OUVIDORIA RESPOSTA',
            'USUARIO RESPOSTA',
            'RESPOSTA'
        ]
    }
}

def excel_to_json(input_file, output_file, tipo_arquivo):
    records = pyexcel.get_records(file_name=input_file)
    d = dict()
    index_d = dict()
    separators = (',', ':')
    index_field = tipos_arquivos[tipo_arquivo]['index_field']
    with open(output_file, 'w') as outfile:
        for record in records:
            index_d['index'] = {'_id': record[index_field]}
            json.dump(index_d, outfile, separators=separators)
            outfile.write('\n')
            for cabecalho in tipos_arquivos[tipo_arquivo]['cabecalho']:
                d[slugify(cabecalho)] = str(record[cabecalho])
                # d['texto_resposta'] = BeautifulSoup(
                #    html.unescape(record['Texto da Resposta']), 'html.parser'
                # ).get_text()

            json.dump(d, outfile, separators=separators)
            outfile.write('\n')
    pyexcel.free_resources()


def check_header(header, tipo_arquivo):
    """Checa se a primeira linha da planilha corresponde ao CABECALHO_PLANILHA"""
    for cabecalho in tipos_arquivos[tipo_arquivo]['cabecalho']:
        if not (cabecalho in header):
            print('A coluna %s não foi encontrada no arquivo' % cabecalho)
            return False
    return True

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
    for tipo_arquivo in tipos_arquivos:
        if check_header(header, tipo_arquivo):
            print('File ok!')
            return tipo_arquivo
    pyexcel.free_resources()
    raise Exception('Não foi possível reconhecer o formato da planilha')

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
    tipo_arquivo = check_file(args.file_path)
    excel_to_json(args.file_path, 'output.json', tipo_arquivo)
    print('"output.json" gerado.')


