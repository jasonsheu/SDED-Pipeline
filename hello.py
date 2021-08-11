from flask import Flask
app =  Flask('SDED-Pipeline')

@app.route('/')
def hello():
	return 'Hello, World!'

