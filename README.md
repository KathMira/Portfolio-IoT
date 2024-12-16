<h1 align="center">Portfólio - Pipeline de Dados com IOT e Docker</h1>

O projeto foi realizado usando as seguintes ferramentas:

- ### Python
    - Dependências:
        - Streamlit
        - Pandas
        - Plotly
        - Sqlalchemy
        - psycopg2-binary

- ### Docker
- ### Postgres
- ### Dbeaver

<br>

## Configuração
### No arquivo main.py
Conexão com o banco de dados:
```ruby
engine = create_engine('postgresql://postgres:minhaSenha@localhost:5432/postgres')
```
Carregando os dados do banco para o projeto:
```ruby
def carrega_dados(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)
```
Adicionando um título para o Dashboard das views no Streamlit:
```ruby
st.title('Dashboard de Temperaturas IoT')
```
Carregando views para o Dashboard:
<br>
Gráfico 1:
```ruby
st.header('Média de Temperatura por Dia')
data_avg_temp = carrega_dados('media_temperatura_salas_por_dia')
grafico1 = px.line(
    data_avg_temp,
    x='date',
    y='avg_temp',
    color='out_in',  # Diferenciar pelas categorias 'in' e 'out'
    labels={'out_in': 'Tipo'}
)

grafico1.update_layout(
    yaxis=dict(range=[0, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico1)
```
Gráfico 2:
```ruby
st.header('Média de temperatura externa no dia por mês')
data_avg_temp = carrega_dados('media_temperatura_externa_no_dia_por_mes')
grafico2 = px.bar(
    data_avg_temp,
    x='hour', 
    y='avg_temp', 
    color='month',
    barmode='group'
    )

grafico2.update_layout(
    yaxis=dict(range=[data_avg_temp['avg_temp'].min() - 1, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico2)
```
Gráfico 3:
```ruby
st.header('Média de temperatura interna no dia por mês')
data_avg_temp = carrega_dados('media_temperatura_interna_no_dia_por_mes')
grafico3 = px.bar(
    data_avg_temp,
    x='hour',
    y='avg_temp', 
    color='month',
    barmode='group'
    )

grafico3.update_layout(
    yaxis=dict(range=[data_avg_temp['avg_temp'].min() - 1, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico3)
```
### No arquivo csv_reader.py:
Importando bibliotecas:
```ruby
import pandas as pd
from sqlalchemy import create_engine
```
Utilização da função para ler o arquivo csv:
```ruby
data = pd.read_csv('data.csv')
```
Conexão com o banco:
```ruby
engine = create_engine('postgresql://postgres:minhaSenha@localhost:5432/postgres')
```
Importação dos dados do csv para o banco:
```ruby
data.to_sql('temperaturas', engine, if_exists='append', index=False)
```

## Execução

<!-- COMO TU EXECUTOU OS BAGUI -->
Após criar o container seguindo as instruções do pdf da matéria de IoT, ele já está funcionando.
![alt text](image.png)
Utilizando o seguinte comando:
![alt text](image-1.png)
Ele abre automaticamente o navegador com o dashboard configurado.

### Dashboard

![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)

<br>

## SQL

Criação da tabela no banco:
```ruby
create table if not exists Temperaturas(
id varchar (100) primary key,
room_id varchar (100) not null,
noted_date timestamp not null,
temperature int not null,
out_in char (3) not null
);
```

### View 1
Cria a view, seleciona o id da sala, a função AVG faz a média de temperatura dessa mesma sala em várias datas diferentes.
<br>
Agrupa por id de sala, data e se é externa/interna.
<br>
E ordena por data.
```ruby
CREATE VIEW media_temperatura_salas_por_dia AS
SELECT room_id, AVG(temperature) as avg_temp, date(noted_date), out_in
FROM Temperaturas
GROUP BY room_id, date(noted_date), out_in
order by date(noted_date);
```
### View 2
Cria a view, seleciona o id da sala, a função AVG faz a média de temperatura da parte externa da sala durante o período de um dia de várias datas diferentes durante o mês.
<br>
Agrupa por id de sala e mês e ano, a função EXTRACT ajuda a separar as horas do dia.
<br>
E ordena por mês e ano.
```ruby
create VIEW media_temperatura_externa_no_dia_por_mes as
SELECT room_id, avg(temperature) as avg_temp, extract (hour from noted_date) as hour, to_char(noted_date, 'MM-YYYY') as month
FROM Temperaturas
where out_in = 'Out'
GROUP BY room_id, EXTRACT(hour from noted_date),to_char(noted_date, 'MM-YYYY')
order by to_char(noted_date, 'MM-YYYY'), extract (hour from noted_date);
```
### View 3
Cria a view, seleciona o id da sala, a função AVG faz a média de temperatura da parte interna da sala durante o período de um dia de várias datas diferentes durante o mês.
<br>
Agrupa por id de sala e mês e ano, a função EXTRACT ajuda a separar as horas do dia.
<br>
E ordena por mês e ano.
```ruby
create VIEW media_temperatura_interna_no_dia_por_mes as
SELECT room_id, avg(temperature) as avg_temp, extract (hour from noted_date) as hour, to_char(noted_date, 'MM-YYYY') as month
FROM Temperaturas
where out_in = 'In'
GROUP BY room_id, EXTRACT(hour from noted_date),to_char(noted_date, 'MM-YYYY')
order by to_char(noted_date, 'MM-YYYY'), extract (hour from noted_date);
```
<br>

## Insights obtidos
Podemos analisar que na View 1, a partir da metade do mês de Setembro, houve uma alta de temperatura considerável no lado externo da sala enquanto dentro, mantinha a mesma média de temperatura.

<br>
Já na View 2, podemos ver a média de temperatura da parte externa da sala por dia, comparando com os demais dias do mês, onde tiramos a conclusão de que o mês de Outubro fi um dos mais quentes.

<br>
E na View 3, podemos ver a média de temperatura da parte externa da sala por dia, comparando com os demais dias do mês.