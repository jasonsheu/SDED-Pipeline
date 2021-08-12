from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO: What should this be?'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/new-job/', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			flash('Title is required!')
		else:
			return redirect(url_for('index'))

	return render_template('create.html')

