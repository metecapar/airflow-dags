import urllib3
import requests,psycopg2
from airflow.models import Variable

db = Variable.get("db")
dbPassword = Variable.get("pass")
user = Variable.get("user")

def getDefinition(host, user, password):
    headers = urllib3.make_headers(basic_auth=user + ":" + password)
    url = "http://"+host+":15672/api/definitions"
    response = requests.request("GET", url, headers=headers)
    definition = response.text
    writeData(definition)

def writeData(definition):
    conn = psycopg2.connect(host=db, database="devops_template", user=user, password=dbPassword, port="5432")
    imlec = conn.cursor()
    insertQuery = 'INSERT INTO defs (defsRabbitMQ) VALUES (%s);'
    value = (definition,)
    imlec.execute(insertQuery,value)
    conn.commit()


    