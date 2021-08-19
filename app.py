from flask import Flask, render_template, request, url_for, flash, redirect
from ragic_tools import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TODO: What should this be?'

LOG_FILE = "test.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs/new/request-spreadsheet', methods=('GET', 'POST'))
def request_spreadsheet():
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
            
            table = ragic_reader.get_table() #NED json as string

            # TODO
            f = open(LOG_FILE, 'w')
            json.dump(table, f)

            return redirect(url_for('confirmation'))
    
    return render_template('create.html')

    #return redirect(url_for('history'))

@app.route('/request/confirm')
def confirmation():
    json_file = open(LOG_FILE, 'r')

    data = json.load(json_file) # load json file into python dict object
    
    # Parse the table information
    print("Printing table info:")
    
    # for key1 in data:
    #     print("Entry:", key1)
    #     item = data[key1]
    #     for key2 in item:
    #         if (key2[0] != '_'):
    #             print('    ', key2, ":", item[key2])

    meta_fnames = ["_ragicId", "_star", "_index_title_", "_index_", "_seq"]
    field_names = [key for key in data['0'].keys() if key not in meta_fnames]
    
    print(field_names)

    
    

    return render_template('confirmation.html', table_info=repr(data))



@app.route('/jobs/history/')
def history():
    return render_template('history.html')


@app.route('/favicon.ico')
def icon():
    return redirect(url_for('static', 'sded-logo.png'))
