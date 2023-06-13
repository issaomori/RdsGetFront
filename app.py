from chalice import Chalice
import psycopg2
import boto3
import json


app = Chalice(app_name='RdsGetFront')


# AWS Lambda


@app.lambda_function()
def get_all(event, context):
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    cursor.execute("SELECT orders.id, orders.status, users.nome, array_agg(items.nome) as item_nomes \
                    FROM orders JOIN users ON orders.user_id = users.id JOIN unnest(orders.items) AS item_id ON TRUE \
                    JOIN items ON items.id = item_id GROUP BY orders.id, orders.status, users.nome;")  # comando que faz a consulta no banco
    return {"list_orders": cursor.fetchall()}


@app.lambda_function()
def get_order(event, context):
    id_user = event['ID']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    cursor.execute(f"SELECT orders.id, orders.status, users.nome, \
       ARRAY(SELECT items.nome FROM items WHERE items.id = ANY(orders.items)) as item_nomes\
        FROM orders JOIN users ON orders.user_id = users.id WHERE orders.id = {id_user};")  # comando que faz a consulta no banco
    return {"list_orders": cursor.fetchone()}


@app.lambda_function()
def get_order_name(event, context):
    name_user = event['nome']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT orders.id, orders.status, users.nome,
                   ARRAY(SELECT items.nome FROM items WHERE items.id=ANY(orders.items)) as item_nomes
                   FROM orders JOIN users ON orders.user_id=users.id
                   WHERE users.nome='{name_user}';""")  # comando que faz a consulta no banco
    return {"list_orders": cursor.fetchall()}


@app.lambda_function()
def new_order(event, context):  # itens, user
    id_do_usuario = event['nome']
    status = "PROCESSANDO"
    items_pedidos = event['items']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    cursor.execute(f"WITH user_info AS (SELECT id FROM users WHERE nome = '{id_do_usuario}'),\
    insert_user AS (INSERT INTO users (nome) SELECT '{id_do_usuario}'\
    WHERE NOT EXISTS (SELECT 1 FROM user_info) RETURNING id)\
    INSERT INTO orders (status, user_id, items) SELECT '{status}',\
    COALESCE((SELECT id FROM user_info), (SELECT id FROM insert_user)), ARRAY{items_pedidos};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"new order": "pedido cadastrado com sucesso"}


@app.lambda_function()
def update_status(event, context):
    id_do_usuario = event['ID']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    # comando que atualiza o status de um pedido para aprovado
    cursor.execute(
        f"UPDATE orders SET status='APROVADO' WHERE id={id_do_usuario};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"Update Status": "pagamento aprovado"}


@app.lambda_function()
def delete_order(event, context):
    id_do_pedido = event['ID']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    # comando que atualiza o status de um pedido para aprovado
    cursor.execute(f"DELETE from orders WHERE id={id_do_pedido};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"Deleted order": "pedido cancelado"}


# ------------------------------------------------------------------

# AWS Gateway


@app.route("/order", methods=['PATCH'], cors=True)
def update_an_order():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))
    payload = app.current_request.json_body
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings
    result = client.invoke(FunctionName='RdsGetFront-dev-update_status',
                           Payload=json_payload)
    return json.load(result['Payload'])
# echo '{"ID":"5"}' | chalice-local invoke -n update_status
# https://mmwdi1i8c3.execute-api.localhost.localstack.cloud:4566/api/order


@app.route("/order/user/{nome}", methods=['GET'], cors=True)
def get_order_name_api(nome):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    # convertemos e recebemos o id passado por parâmetro
    payload = {"nome": nome}
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"nome":"Igor"}' | chalice-local invoke -n get_order
    # o client.invoke é: chalice-local invoke -n get_order_name
    # o payload é: echo '{"nome":"Igor"}'.
    result = client.invoke(FunctionName='RdsGetFront-dev-get_order_name',
                           Payload=json_payload)
    return json.load(result['Payload'])


@app.route("/order", methods=['GET'], cors=True)
def get_all_api():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    result = client.invoke(FunctionName='RdsGetFront-dev-get_all')
    return json.load(result['Payload'])


@app.route("/order/{var}", methods=['GET'], cors=True)
def get_order_api(var):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    if (var.isdigit()):
        # convertemos e recebemos o id passado por parâmetro
        payload = {"ID": var}
        # transformamos um Json válido em uma string, já que Payload só
        json_payload = json.dumps(payload)
        # trabalha com strings

        # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
        # o client.invoke é: chalice-local invoke -n get_order
        # o payload é: echo '{"ID":"2"}'.
        result = client.invoke(FunctionName='RdsGetFront-dev-get_order',
                               Payload=json_payload)
        return json.load(result['Payload'])
    else:
        payload = {"nome": var}
        # transformamos um Json válido em uma string, já que Payload só
        json_payload = json.dumps(payload)
        # trabalha com strings

        # faz a mesma função que a linha do terminal: echo '{"nome":"Igor"}' | chalice-local invoke -n get_order
        # o client.invoke é: chalice-local invoke -n get_order_name
        # o payload é: echo '{"nome":"Igor"}'.
        result = client.invoke(FunctionName='RdsGetFront-dev-get_order_name',
                               Payload=json_payload)
        return json.load(result['Payload'])


@app.route("/order", methods=['POST'], cors=True)  # {"ID":"4","items":[1, 1]}
def receive_an_order():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    # payload = {"ID": app.current_request.json_body[ID], "items": "[2,2]"}
    payload = app.current_request.json_body
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings
    # app.current_request.json_body => STRING ou JSON(dicionário)
    result = client.invoke(FunctionName='RdsGetFront-dev-new_order',
                           Payload=json_payload)
    return json.load(result['Payload'])
# https://e0f0uaiay3.execute-api.localhost.localstack.cloud:4566/api/order


@app.route("/order/{var}", methods=['DELETE'], cors=True)
def delete_order_api(var):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    payload = {"ID": var}  # convertemos e recebemos o id passado por parâmetro
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
    # o client.invoke é: chalice-local invoke -n get_order
    # o payload é: echo '{"ID":"2"}'.
    result = client.invoke(FunctionName='RdsGetFront-dev-delete_order',
                           Payload=json_payload)
    return json.load(result['Payload'])
