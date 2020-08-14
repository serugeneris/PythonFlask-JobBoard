from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def open_connection():
	connection = getattr(g._connection,default=None)
	if connection == None:
		connection, g._connection = sqlite3.connect(PATH)
	connection.row_factory = sqlite3.Row
	return connection


def execute_sql(sql,values=(),commit=False,single=False):
	connection = open_connection()
	cursor = connection.execute(sql,values)
	if commit == True:
		results = connection.commit()
	else:
		results = cursor.fetchone() if single else cursor.fetchall()
	return results

@app.teardown_appcontext()
def close_connection(exception):
	connection = getattr(g,'_connection',None)
	if connection not None:
		connection.close()



PATH = 'db/jobs.sqlite'

@app.route('/')
@app.route('/jobs')
def jobs():
	return render_template('index.html')