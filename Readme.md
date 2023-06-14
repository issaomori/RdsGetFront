# RDS_STACKSPOT

Projeto da fase inicial do Labs42_jan23 em parceria com o Itaú.

DESAFIO 5:
Criar um plugin para StackSpot usando AWS RDS, API Gateway, AWS Lambda

Equipe:
Projeto feito pela equipe: Welton (wleite), Gabriel (gissao-m) e Maria Clara (maclara-).

### Pré-requisito:

Abra o docker desktop...

Já no VsCode inicialize o container:\
`localstack start -d`

# 1 - Iniciando um projeto com o Chalice:

`chalice-local new-project`

Escolha o nome do projeto\
`[?] Enter the project name: RdsGetFront`

Escolha a opção "REST API"\
`[?] Select your project type: REST API : > REST API`

### Entre na pasta do projeto Chalice:

`cd RdsGetFront`

Para "compilar" o arquivo, na verdade registra as nossas funções nos serviços AWS\
`chalice-local deploy`

### Rode o comando invoke para executar uma função:
Para ver o retorno da função no terminal:\
`chalice-local invoke -n first_function`

Você verá o retorno da função no terminal:\
`{"hello": "world"}`


Com essa função criada, faremos modificações nela para atender as nossas necessidades....

# 2 - Iniciando um banco de dados RDS para usar com o Chalice:

Ecolhemos o banco de dados Postgres por ser compatível com o Localstack e ter uma boa base de documentação de como utilizá-lo.

### Pré-requisitos:
<br>
Biblioteca psycopg2 local

`pip3 install psycopg2-binary`

<br>

Cliente postgress para o terminal\
`sudo apt install postgresql-client`

<br>

Para conectar-se com  banco usaremos a versão já complilada e adaptada da biblioteca psycopg2.
Para isso, no arquivo "requeriments.txt" escreva:\
`aws-psycopg2`

<br>

Para listar as instâncias de banco de dados RDS\
`awslocal rds describe-db-instances`

<br>

Devemos criar o banco de dados com LocalStack\
`awslocal rds create-db-instance --master-username user --master-user-password pass --db-instance-identifier mydb --engine postgres --db-name database --db-instance-class db.t3.small`

<br>

Criando o banco de dados com o docker\
`docker run -p 4510:5432 -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=user -e POSTGRES_DB=database postgres`
<br>

Agora você pode se conectar ao banco de dados PostgreSQL usando um cliente de banco de dados ou uma biblioteca de programação. Use o host localhost, a porta 4510, o nome de usuário postgres e a senha para se conectar ao banco de dados.
`psql -d database -U user -p 4510 -h localhost -W`\
A senha é `pass` e o usuário caso necessário é `user`

<br>

Se quiser sair do banco de dados use:
```sql
exit
```

<br>

... Agora, dentro do banco de dados...
Para exibir as tabelas que temos
```sql
\dt
```

<br>

Criar a tabela de pedidos
```sql
CREATE TABLE orders (
id SERIAL PRIMARY KEY,
status VARCHAR(20) NOT NULL,
user_id INTEGER NOT NULL,
items INTEGER[] NOT NULL
);
```

<br>

Criar a tabela de items
```sql
CREATE TABLE items (
id SERIAL PRIMARY KEY,
nome VARCHAR(20) NOT NULL
);
```

Criar a tabela de users
```sql
CREATE TABLE users (
id SERIAL PRIMARY KEY,
nome VARCHAR(40) NOT NULL
);
```

<br>

Para deletar uma tabela
```sql
DROP TABLE orders;
```

<br>

Para inserir itens na tabela items
```sql
INSERT INTO items (nome) VALUES ('x-salada'), ('misto'), ('hot-dog');
```
<br>


Para inserir itens na tabela usuários
```sql
INSERT INTO users (nome) VALUES ('João'), ('Lúcia'), ('Igor');
```

<br>

Para inserir itens na tabela pedidos
```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '1', ARRAY[1, 2]);
```

<br>

```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '2', ARRAY[2, 3]);
```

<br>

```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '3', ARRAY[1, 3]);
```

<br>

Para exibir todos os registros de uma tabela
```sql
SELECT * FROM orders;
```

<br>

Para exibir os registros de uma tabela, filtrando por um parâmetro específico
```sql
SELECT * FROM orders WHERE id=1;
```

<br>

Deletando linhas de uma tabela
```sql
DELETE from livros WHERE id=1;
```

<br>

Para fazer um update em uma linha da tabela
```sql
UPDATE livros SET disponivel=1 WHERE id=19;
```

<br>

Para fazer a consulta trocando todos os ids pelos nomes dos users (praticamente refaz a tabela de pedidos, mas com nomes em vez de ids_users)
```sql
SELECT orders.id, orders.status, users.nome, orders.items
FROM orders
JOIN users ON orders.user_id = users.id;
```

<br>

Para fazer uma consulta mesclando os dados de duas tabelas diferentes, nesse caso queremos que a tabela de pedidos retorne com o nome de quem fez o pedido, e não com o ID desse user
```sql
SELECT orders.id, orders.status, users.nome, orders.items
FROM orders
JOIN users ON orders.user_id = users.id
WHERE orders.id = 3;
```

<br>

Consulta no banco de dados que troca o array de IDs de itens pelo nome correspondente da tabela de items
```sql
SELECT orders.id, orders.status, orders.user_id, array_agg(items.nome) AS nomes_itens
FROM orders
JOIN items ON items.id = ANY(orders.items)
WHERE orders.id = 3
GROUP BY orders.id, orders.status, orders.user_id;
```

<br>


Consulta no banco de dados que troca o array de IDs de itens pelo nome correspondente da tabela de items
Mesmo comando, mas usando 2 joins em vez da função ANY
```sql
SELECT orders.id, orders.status, orders.user_id, array_agg(items.nome) AS nomes_itens
FROM orders
JOIN unnest(orders.items) AS item_id ON true
JOIN items ON items.id = item_id
WHERE orders.id = 3
GROUP BY orders.id, orders.status, orders.user_id;
```


<br>

Consultar o pedido substituindo o ID do usuário e do item pelo nome correspondente em sua tabela
```sql
SELECT orders.id, orders.status, users.nome,
       ARRAY(SELECT items.nome FROM items WHERE items.id = ANY(orders.items)) as item_nomes
FROM orders
JOIN users ON orders.user_id = users.id
WHERE orders.id = 3;
```

<br>

Comando que troca o ID_user pelo nome, e os id_itens pelos itens MOSTRANDO os itens duplicados de um mesmo pedido
```sql
SELECT orders.id, orders.status, users.nome,
       array_agg(items.nome) as item_nomes
FROM orders
JOIN users ON orders.user_id = users.id
JOIN unnest(orders.items) AS item_id ON TRUE
JOIN items ON items.id = item_id
GROUP BY orders.id, orders.status, users.nome;
```

<br>

Para adicionar um novo pedido, no nome do user, e ao mesmo tempo salvar o user novo na tabela de users
```sql
WITH new_user AS (
    INSERT INTO users (nome) VALUES ('Jonata')
    RETURNING id
)
INSERT INTO orders (status, user_id, items)
VALUES ('APROVADO', (SELECT id FROM new_user), ARRAY[1, 2]);
```

<br>


Para adicionar um novo pedido, no nome de um user já existente
```sql
WITH user_info AS (
    SELECT id FROM users WHERE nome = 'Ronaldo'
)
INSERT INTO orders (status, user_id, items)
VALUES ('APROVADO', (SELECT id FROM user_info), ARRAY[3, 4]);
```

<br>

Conferimos se o USER já está cadastrado, se for um user novo, cadastramos o user e registramos o pedido, se o user já existir, apenas registramos o novo pedido dele
```sql
WITH user_info AS (
    SELECT id FROM users WHERE nome = 'Matheus'
),
insert_user AS (
    INSERT INTO users (nome)
    SELECT 'Matheus'
    WHERE NOT EXISTS (SELECT 1 FROM user_info)
    RETURNING id
)
INSERT INTO orders (status, user_id, items)
SELECT 'PROCESSANDO', COALESCE((SELECT id FROM user_info), (SELECT id FROM insert_user)), ARRAY[2, 1, 3];
```

<br>


Como filtrar os pedidos pelo nome de quem pediu
```sql
SELECT orders.id, orders.status, orders.user_id, orders.items
FROM orders
JOIN users ON users.id = orders.user_id
WHERE users.nome = 'Igor';
```

Como filtrar os pedidos pelo nome de quem pediu, APARECENDO o nome dos itens pedidos
```sql
SELECT orders.id, orders.status, users.nome,
       ARRAY(SELECT items.nome FROM items WHERE items.id = ANY(orders.items)) as item_nomes
FROM orders
JOIN users ON orders.user_id = users.id
WHERE users.nome = 'Igor';
```


<br>


Como filtrar os pedidos pelo nome de quem pediu, fazendo que o nome do User venha no lugar do ID
```sql
SELECT orders.id, orders.status, users.nome AS user_nome, orders.items
FROM orders
JOIN users ON users.id = orders.user_id
WHERE users.nome = 'Igor';
```

# 3 - Como testar a API:

### POST

`https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/`

#### BODY:
```json
{
  "nome": "Valéria",
  "items": [
    1,
    2
  ]
}
```

```json
{
  "nome": "Messias",
  "items": [
    1,
    3
  ]
}
```

```json
{
  "ID": "3",
  "items": [
    1,
    3,
    2
  ]
}
```

<br>

### GET
`https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/2`

<br>

### UPDATE
`https://2v3qgzz3sn.execute-api.localhost.localstack.cloud:4566/api/order`

#### BODY:
```json
{
  "ID": "2"
}
```
<br>

### DELETE
`https://n0q4zv02w2.execute-api.localhost.localstack.cloud:4566/api/order/2`

<br>

### Iniciando um servidor local com python

<br>

Dentro da pasta do projeto digite no terminal
`python3 -m http.server 8000`

<br>


## Extra:

### Comandos amigos:

Para listar todas as funções lambdas\
`awslocal lambda list-functions | grep FunctionName`

Para passar algum parâmetro para uma funçao lambda específica\
`echo '{"ID":"1053"}' | chalice-local invoke -n get_order`

Para logar nos serviços pagos da Localsatck\
`export LOCALSTACK_API_KEY=sua_key`  Essa key você pega na sua página de usuário da localstak

_______________________________________________________________________________________________

(aparece todos)

SELECT orders.id, orders.status, users.nome, orders.items
FROM orders
JOIN users ON orders.user_id = users.id
;

(aparece todos com os itens)

SELECT orders.id, orders.status, users.nome,
       ARRAY(SELECT items.nome FROM items WHERE items.id = ANY(orders.items)) as item_nomes
FROM orders
JOIN users ON orders.user_id = users.id;

(NAO aparece todos com os itens)
SELECT orders.id, orders.status, users.nome,
       array_agg(items.nome) as item_nomes
FROM orders
JOIN users ON orders.user_id = users.id
JOIN unnest(orders.items) AS item_id ON TRUE
JOIN items ON items.id = item_id
GROUP BY orders.id, orders.status, users.nome;
