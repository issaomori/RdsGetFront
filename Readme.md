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

Devemos criar o banco de dados\
`awslocal rds create-db-instance --master-username user --master-user-password pass --db-instance-identifier mydb --engine postgres --db-name database --db-instance-class db.t3.small`

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

Criar a tabela de pensionistas
```sql
CREATE TABLE pensionistas (
id SERIAL PRIMARY KEY,
nome VARCHAR(20) NOT NULL
);
```

Para inserir itens na tabela pensionistas
```sql
INSERT INTO pensionistas (nome) VALUES ('João'), ('Maria'), ('José');
```

<br>

Para exibir todos os registros de uma tabela
```sql
SELECT * FROM pensionistas;
```

# COMO TESTAR

### GET
`https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/pensionistas`