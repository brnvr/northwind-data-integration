
# Code challenge - engenharia de dados
Instruções para executar a pipeline do projeto desenvolvido pelo candidado Bruno Gustavo Vieira:

## Setup

No diretório ``/meltano``, montar a imagem do docker que contém o projeto do Meltano:

```sh
docker build -t northwind .
```

É necessário também iniciar os bancos Postgres de origem e de destino. Eles estão localizados nos diretórios ``/postgres-source`` e ``/postgres-dest``. Dentro desses diretórios, basta executar o comando:

```sh
docker-compose up
```

## Jobs

Há 3 jobs disponíveis para controlar a pipeline:


### input-to-local-disk
Extrai os dados do CSV com os detalhes do pedido e os dados do banco Northwind e os carrega em ``/meltano/data``, no formato CSV. 

```sh
docker run -v "$(pwd)":/project northwind run input-to-local-disk
```

Os dados são inicialmente carregados no diretório ``/data/.temp``, e então um script é executado para movê-los para os diretórios com o padrão requisitado ``/{table}/{date}/{file}.csv``. É também gerado um dicionário ``csv_map.json`` que mapeia o nome e data de cada entidade para a pasta contendo os dados extraídos. 

### local-disk-to-destination
Extrai os dados contidos nos subdiretórios de ``/data`` e os carrega no banco Postgres destino. Ela utiliza o ``csv_map.json`` gerado no processo anterior para mapear as entidades a serem extraídas

```sh
docker run -v "$(pwd)":/project northwind run local-disk-to-destination
```
Um CSV será gerado no diretório ``/data/result`` contendo os dados da consulta de pedidos+detalhes (extraídos de uma view gerada no banco de destino).

### full-pipeline
Realiza os dois processos anteriores em sequência, ou seja, carrega os dados dos inputs para o disco local e do disco para o banco de destino.

```sh
docker run -v "$(pwd)":/project northwind run full-pipeline
```

Para qualquer um dos processos, você pode definir uma variável de ambiente **DATE** (uma data no formato *yyyy-mm-dd*) para utilizar uma data diferente da atual:

```sh
docker run -v -e DATE="2002-09-21" "$(pwd)":/project northwind run full-pipeline
```
## Airflow

Para executar essa pipeline diáriamente de forma automática, basta iniciar scheduler do airflow:
```sh
docker run -it -v "$(pwd)":/project northwind invoke airflow scheduler
```

## Observações

* O loader **target-csv** estava dando erro para extrair as colunas do tipo *real* (``products.unit_price`` e ``orders.freight``). Acabei focando em outras questões no desafio então não consegui descobrir a causa disso a tempo, por isso por enquanto essas colunas não estão sendo extraídas.
* Um bug pode ocorrer ao se rodar os jobs ``input-to-local-disk`` ou ``full-pipeline`` sem o diretório ``/data/.temp/postgres`` ter sido criado. Também não tive tempo de identificar a causa desse bug, mas basta rodar o mesmo job novamente e irá funcionar normalmente.
* O tipo de replicação dos extratores que extraem os dados iniciais está como **INCREMENTAL**. Para fins de depuração, caso você queira extrair todos os dados (e não apenas os que foram modificados/inseridos), deve-se deletar a pasta ``/.meltano/run`` (não encontrei um comando para realiar a limpeza de estado) ou então alterar o tipo de replicação dos extratores **tap-postgres-source** e **tap-csv-source** para **FULL_TABLE**.
