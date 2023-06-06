from chalice import Chalice
import psycopg2
import boto3
import json


app = Chalice(app_name='RdsGetFront')

@app.lambda_function()
def get_rds(event, context): # a func lambda sempre recebe 2 parâmetros
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM pensionistas;")
    return {"pensionistas": cursor.fetchall()}


@app.route('/pensionistas', methods = ['GET'])
def get_rds_api():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))
    result = client.invoke(FunctionName='RdsGetFront-dev-get_rds')
    return json.load(result['Payload'])


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
