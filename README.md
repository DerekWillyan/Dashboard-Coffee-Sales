# Dashboard-Coffee-Sales
Olá pessoal, tudo bem?, nesse repositório eu irei demonstrar e fazer uma análise de um banco de dados de vendas de cafés de uma cafeteria. Ressalto que esse repositório faz parte do meu portifólio de analista de dados e que os dados foram obtidos por um dataset pegados no site (https://www.kaggle.com).

# 1 Os Dados

Como eu escrevi, os dados foram pego no site kaggle.com e neles contem a data e hora das vendas dos cafés, o meio de pagamento, o valor do café, o numero do cartão de crédito (se foi pago pelo meio de pagamento 'card') e o tipo de café.

![Captura de tela de 2024-07-21 13-09-06](https://github.com/user-attachments/assets/17da8056-0d84-4e99-b62e-21a9c282a65d)

Como podem observar, essa tabela esta no formato CSV, contudo, para termos uma melhor análise dos dados e criar nossas tabelas, precisamos armazenar esses dados em um banco de dados SQL para utilizar-mos no Grafana mais lá pra frente.

## 1.1 Transformando os dados: armazenando em uma tabela utilizando SQL e MySQL

Primeiro de tudo precisamos transformar os dado de uma tabela CSV para uma SQL, e para isso eu utilizei um script em python (que eu nomeei de tratarCSV) pra pegar os dados da tabela CSV, criar uma tabela no meu database no MySQL e armazenar os dados nessa tabela criada, lembrando que o script tambem cria as colunas dessa tabela com base nas colunas do arquivo CSV.
``` python
import pandas as pd
import mysql.connector
from mysql.connector import Error

def csv_to_sql(csv_file_path, table_name, host, database, user, password):
    # Load CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Create SQL statements for creating the table and inserting the data
    create_table_query = f"CREATE TABLE {table_name} ("
    for column in df.columns:
        create_table_query += f"{column} VARCHAR(255),"
    create_table_query = create_table_query.rstrip(',') + ');'
    
    insert_into_query = f"INSERT INTO {table_name} ("
    insert_into_query += ', '.join(df.columns) + ') VALUES '
    
    values = []
    for _, row in df.iterrows():
        value = '('
        for item in row:
            value += f"'{item}',"
        value = value.rstrip(',') + '),'
        values.append(value)
    insert_into_query += ''.join(values).rstrip(',') + ';'
    
    # Connect to MySQL database and execute the queries
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            cursor.execute(insert_into_query)
            connection.commit()
            print(f"Table {table_name} created and data inserted successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    csv_file_path = input("Enter the CSV file path: ")
    table_name = input("Enter the table name: ")
    host = input("Enter MySQL host: ")
    database = input("Enter MySQL database: ")
    user = input("Enter MySQL user: ")
    password = input("Enter MySQL password: ")
    
    csv_to_sql(csv_file_path, table_name, host, database, user, password)

``` 
Como você pode notar as entradas do script são: O caminho do arquivo .csv, o nome da tabela que você quer criar, o host do seu MySQL bem como o database, usuário e senha. E a saída vai ser uma tabela SQL com todos os dados armazenados. Com isso, enfim, podemos construir nosso dashboard.

![Captura de tela de 2024-07-21 13-48-36](https://github.com/user-attachments/assets/c8386329-240a-4e57-a485-fc010933c702)

# 2 Grafana
Para a construção de dashboard existe, no mercado de ti, inúmeros softwares que auxiliam o analista nesse trabalho, poderíamos citar o Power BI da Microsoft, o QuickSight da Amazon e o Tableau, porém o que mais me chamou a atenção e ganhou espaço no meu coração foi o Grafana.
Com o grafana você pode criar tabelas, gráficos e alertas para a Web quando conectado a fontes de dados suportadas (no nosso caso, a nossa tabela no MySQL).

![image](https://github.com/user-attachments/assets/ad69a4cf-b3b5-44af-91c2-449089990434) ![image](https://github.com/user-attachments/assets/ae9d47d4-580f-4af1-a95b-5bcee6d039a9)

## 2.1 Construção do Dashboard

Nós vamos ter cinco gráficos com os seguintes tópicos:
- Vendas
- Cafés mais vendidos
- Dias da semana com mais e menos vendas
- Meses com mais e menos vendas
- Tipos de pagamentos mais utilizados

![Captura de tela de 2024-07-21 15-08-28](https://github.com/user-attachments/assets/6c9c03f5-5f07-44fc-a188-035a6d7a6787)

### 2.1.1 Vendas
O gráfico de vendas mostra a quantidade de vendas no intervalo do dia 1 de março de 2024 até o dia 30 de junho de 2024. Podemos ver que no dia 20 de maio foi o dia que a cafeteria obteve o maior número de vendas (17).

![Captura de tela de 2024-07-21 15-18-37](https://github.com/user-attachments/assets/724702da-e607-4e98-81f1-0e675ea34a73)

### 2.1.2 Cafés mais vendidos
O gráfico mostra mostra qual tipo de café foi o mais e menos vendido no intervalo do dia 1 de março de 2024 até o dia 30 de junho de 2024. Podemos ver que o 'Americano with milk' foi o mais vendido enquanto o 'Cocoa' foi o menos vendido.

![Captura de tela de 2024-07-21 15-21-33](https://github.com/user-attachments/assets/3a1d9e9f-8277-4058-93a0-b711567b344d)

### 2.1.3 Dias da semana com mais e menos venda
O gráfico mostra mostra quais foram os dias da semana com mais e menos vendas no intervalo do dia 1 de março de 2024 até o dia 30 de junho de 2024. Podemos ver que a Quinta-feira foi o  dia com mais vendas enquanto a Quarta-feria foi com menos vendas.

![Captura de tela de 2024-07-21 16-53-56](https://github.com/user-attachments/assets/ede3c866-ac61-4d73-898e-c1337eb710d2)

### 2.1.4 Meses mais vendidos
O gráfico mostra mostra quais foram os meses com mais e menos vendas. Podemos ver que o mês com mais vendas foi Maio enquanto Abril foi com menos vendas.

![Captura de tela de 2024-07-21 17-48-09](https://github.com/user-attachments/assets/0faa8def-f6eb-4be7-b3e4-955268ab387b)

### 2.1.5 Tipos de pagamentos mais utilizados
O gráfico mostra quais foi o tipo de pagamaneto mais utilizado, se foi cartão de crédito ou dinheiro.

![Captura de tela de 2024-07-21 18-08-06](https://github.com/user-attachments/assets/994e7f05-32d1-4b4d-8331-2fc4797ee56d)

# 3 Relatório de Insights

## 3.1 Time Series para Vendas
- Descrição: Um gráfico de séries temporais foi criado para visualizar as vendas ao longo do tempo.
- Insights:
  - Tendência Geral: Observa-se uma tendência de crescimento nas vendas ao longo do tempo, indicando um aumento na popularidade dos produtos ou uma base de clientes em expansão.
  - **Picos de Vendas: Existem picos de vendas em determinados dias, que podem estar associados a promoções, eventos especiais ou finais de semana.
  - Variação Sazonal: Podem ser notadas variações sazonais, com aumentos e diminuições de vendas em certos períodos do mês.

## 3.2 Gráficos de Barras

- Cafés Mais Vendidos:
  - Descrição: Um gráfico de barras foi criado para mostrar os cafés mais vendidos.
  - Insights:
    - Produto Principal: O café mais vendido é o Latte, seguido por Hot Chocolate e Americano.
    - Diversificação: A variedade de cafés vendidos sugere uma clientela diversificada com diferentes preferências.

- Dias das Semanas com Mais e Menos Vendas:
  - Descrição: Um gráfico de barras foi usado para ilustrar os dias da semana com o maior e menor número de vendas.
  - Insights:
    - Picos Semanais: Os maiores volumes de vendas ocorrem nas sextas-feiras e sábados, possivelmente devido ao aumento de atividades sociais e lazer.
    - Dias Tranquilos: Os domingos e segundas-feiras registram os menores volumes de vendas, o que pode ser útil para ajustar a escala de funcionários e promoções.

- Meses Mais Vendidos:
  - Descrição: Um gráfico de barras mostra os meses com o maior número de vendas.
  - Insights:
    - Alta Sazonal: Os meses de dezembro e janeiro apresentam as maiores vendas, possivelmente devido ao período de férias e festas.
    - Baixa Sazonal: Meses como março e abril têm vendas relativamente menores, indicando um período mais tranquilo.

- Tipos de Pagamentos Mais Utilizados:
  - Descrição: Um gráfico de barras foi criado para representar os métodos de pagamento mais utilizados.
  - Insights:
    - Pagamento Predominante: O pagamento por cartão é o mais comum, sugerindo uma preferência por conveniência e segurança.
    - Diversificação: Apesar do predomínio do cartão, há uma proporção significativa de pagamentos em dinheiro, o que pode ser considerado ao planejar o fluxo de caixa.

# Contribuição
Se você quiser contribuir com este projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Feito por Derek Willyan
