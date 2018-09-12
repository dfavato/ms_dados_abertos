# Ciências dos dados aplicados aos dados do Ministério da Saúde
Ciências dos Dados aplicados aos dados do Ministério da Saúde

## Instalação do ambiente
### Requisitos iniciais:

* Ambiente Linux
* [Python3](https://www.python.org/downloads/)
* [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
* [Kibana](https://www.elastic.co/downloads/kibana)

### Criando o ambiente virtual
```bash
python3 -m venv caminho/para/um/diretorio
```

**Ativando o ambiente virtual**
```bash
source caminho/para/um/diretorio/bin/activate
```

**Confirmando que o ambiente virtual funcionou**
O comando `which python` deve imprimir: `caminho/para/um/diretorio/bin/python`

**Atualiando Python package index**
```bash
pip install --upgrade pip
```

### Clonando o repositório do git
```bash
git clone https://github.com/dfavato/ms_dados_abertos.git
cd ms_dados_abertos
```

### Instalando os pacotes Python
```bash
pip install -r requirements.txt
```

# Gerando o arquivo de carga para o ElasticSearch
```bash
python ouvidoria.py caminho/para/planilha/da/ouvidoria
```

Para que o script funcione, a planilha da ouvidoria deve ter as seguintes colunas:
**Planilha simples**

|Número de protocolo|Data do pedido|Texto do pedido|DataRegistro|Texto da Resposta|
|-------------------|--------------|---------------|------------|-----------------|

**Planilha completa**
|Cabeçalho|
|---------|
|OUVIDORIA DE ORIGEM|
|MUNICIPIO ORIGEM|
|UF ORIGEM|
|ESFERA ORIGEM|
|PROTOCOLO|
|MEIO DE ATENDIMENTO|
|ORIGEM DO ATENDIMENTO|
|DEMANDA ATIVA (S/N)|
|DATA DA DEMANDA|
|DATA PREVISTA PARA CONCLUSAO|
|DATA DO FECHAMENTO|
|CLASSIFICACAO|
|ASSUNTO|
|SUBASSUNTO 1|
|SUBASSUNTO 2|
|SUBASSUNTO 3|
|FARMACO|
|DAPS|
|ESTABELECIMENTO COMERCIAL|
|PRIMEIRO DESTINO|
|MUNICIPIO PRIMEIRO DESTINO|
|UF PRIMEIRO DESTINO|
|DESTINO ATUAL|
|MUNICIPIO DESTINO ATUAL|
|UF DESTINO ATUAL|
|STATUS ACOMPANHAMENTO|
|DATA DO ACOMPANHAMENTO|
|MUNICIPIO CIDADAO|
|BAIRRO CIDADAO|
|CEP CIDADAO|
|UF CIDADAO|
|SIGILOSO (S/N)|
|ANONIMO (S/N)|
|DETALHE DA DEMANDA|
|OUVIDORIA RESPOSTA|
|TIPO OUVIDORIA RESPOSTA|
|MUNICIPIO OUVIDORIA RESPOSTA|
|UF OUVIDORIA  RESPOSTA|
|ESFERA OUVIDORIA RESPOSTA|
|USUARIO RESPOSTA|
|RESPOSTA|

Ao rodar o script será gerado o arquivo `output.json`

# Inicializar o ambiente ElasticSearch + Kibana
Executar os seguintes comandos:
```bash
caminho/para/pasta/do/elasticsearch/bin/elasticsearch &
caminho/para/pasta/do/kibana/bin/kibana
```

Se tudo ocorrer corretamente você deverá ver a seguinte mensagem no terminal: `log   [12:02:04.112] [info][listening] Server running at http://localhost:5601`.
Visite `http://localhost:5601` a página do Kibana deve ser carregada.

# Criando o *Index* do ElasticSearch
Em `http://localhost:5601` vá na guia *DevTools*
No console digite:
```js
PUT /ouvidoria
{
	"mappings": {
		"chamado": {
			"properties": {
				"data_pedido": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss.SSS"},
				"data_registro": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss.SSS"},
				"texto_pedido": {"type": "text", fielddata: true},
				"texto_resposta": {"type": "text", fielddata: true}
			}
		}
	}
}
```

Clique no ícone em forma de play *send request*.
Você deverá receber como resposta:
```js
{
	"acknowledge": true,
	"shards_acknowledge": true,
	"index": "ouvidoria"
}
```

# Carregando os dados no ElasticSearch
No terminal digite:
```bash
curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/ouvidoria/chamado/_bulk?pretty' --data-binary @output.json
```

Se der certo o terminal irá imprimir várias linhas no formato json.

**Pronto agora tudo está preparado para criação de Dashboards**

