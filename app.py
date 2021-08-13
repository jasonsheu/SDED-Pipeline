from flask import Flask, render_template, request, url_for, flash, redirect
from ragic_tools import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO: What should this be?'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-job/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        tab_folder = request.form['tab_folder']
        sheet_index = request.form['sheet_index']
        api_key = request.form['api_key']

        if not tab_folder: # TODO add verification?
            flash('Tab folder is required!')
        if not sheet_index: # TODO add verification?
            flash('Sheet index is required!')
        if not api_key:
            flash('API Key is required!')
        else:
            # Parse table from Ragic
            ragic_reader = RagicTools(tab_folder, sheet_index, api_key)
            table = ragic_reader.get_table()
            print(table)

            # TODO


            return redirect(url_for('index'))
    
    return render_template('create.html')

    #return redirect(url_for('history'))

@app.route('/job-history/')
def history():
    return render_template('history.html')


@app.route('/favicon.ico')
def icon():
    return redirect(url_for('static', 'sded-logo.png'))
