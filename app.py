from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory
from ragic_tools import *
from Click2Mail import Address
from werkzeug.utils import secure_filename
import os


# Flask App Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = b"_\xa8\xf0\x10\xcc3\xa6n\x9c'\xd1\xc5\x91\x06z1=\x8b|\xe7\xb8\x8d\xdb\xdd3\xd4j\x9e5\xdf\x04\xf5"
app.config['UPLOAD_FOLDER'] = "uploads"

# Global Constant Declaration
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
LOG_FILE = "address_list.json"

artwork_path = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs/new/request-spreadsheet', methods=('GET', 'POST'))
def request_spreadsheet():
    
    if request.method == 'POST':
        
        ragic_url = request.form['ragic_url']
        api_key = get_api_key()
        file_path = upload_file(request)

        if not ragic_url: # TODO add verification?
            flash('URL is required!')
        if not api_key:
            flash('Login is required!')
        else:
            # Parse table from Ragic
            ragic_reader = RagicTools(ragic_url, api_key)
            
            table = ragic_reader.get_table() #NED json as string

            # TODO
            f = open(LOG_FILE, 'w')
            json.dump(table, f)

            return redirect(url_for('confirmation'))
    
    return render_template('create.html')

    #return redirect(url_for('history'))

@app.route('/request/confirm', methods=('GET', 'POST'))
def confirmation():
    json_file = open(LOG_FILE, 'r')

    df = pd.read_json(json_file)
    df = df.transpose()
    df = df.drop(["_ragicId", "_star", "_index_title_", "_index_", "_seq"], axis=1).sort_index()
    data = df.to_dict('records')

    data = [Address(entry) for entry in data]
    
    # Parse the table information
    
    
    flat_data = [list(entry) for entry in data]
    
    if request.method == 'POST':
        
        if request.form['submit_button'] == 'Cancel':
            return redirect(url_for('request_spreadsheet'))
        elif request.form['submit_button'] == 'Confirm':
            #send mail
            #delete all files to prevent clutter
            
            return redirect(url_for('c2m_publish'))

            
    
    return render_template('confirmation.html', table_body=flat_data, filename=artwork_filename)
    


    

@app.route('/help/api-key', methods=('GET', 'POST'))
def get_api_key():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            api_key = RagicReader.get_api_key(username, password)

            return api_key
        except RagicReader.AuthenticationError:
            flash('Invalid username and/or password')
    

    

@app.route('/publish')
def c2m_publish():
    print("C2M REST IS RUNNING")
    
    # Stage account (0)
    #c2m = c2mAPI.c2mAPIRest("SDEnergyDistrict","LaneL0vesSanDiego!","0")
    
    # Production account (1)
    c2m = c2mAPI.c2mAPIRest("lanewsharman","1Lovesandiego","1")
    

    json_file = open(LOG_FILE, 'r')

    df = pd.read_json(json_file)
    df = df.transpose()
    df = df.drop(["_ragicId", "_star", "_index_title_", "_index_", "_seq"], axis=1).sort_index()
    data = df.to_dict('records')

    for address in data:
        c2m.addressList.append(address)

    

    # Setting  Print Options
    #letter 8.5x11
    po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on First Page','Black and White','White 24#','Printing both sides','First Class','#10 Double Window')
    
    #postcard 3.5 x 5
    #po = c2mAPI.printOptions('Postcard 3.5 x 5','Next Day','Single Sided Postcard','Black and White','White Uncoated','Printing both sides','First Class','#10 Double Window')
    
    print(artwork_path)
    print(c2m.runAll(artwork_path,"2",po).text)

    #delete files
    dir = 'uploads'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))
    

    print('DOCID: ' + c2m.documentId)
    print('AddressListId: ' + c2m.addressListId)
    print('JobId: ' + c2m.jobId)
    
    if int(c2m.jobId) != 0:
        return "success!"
    else:
        return "failure :("

    # TODO https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
    # TODO https://rest.click2mail.com/#/


@app.route('/jobs/history/')
def history():
    return render_template('history.html')


@app.route('/favicon.ico')
def icon():
    return redirect(url_for('static', filename='sded-logo.png'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], artwork_filename)

#file uploading
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


def upload_file(request):
    if request.method == 'POST':
        print('uploading')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'no file'
        file = request.files['file']
        
        
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return ''
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global artwork_path
            artwork_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            global artwork_filename

            artwork_filename = filename # TODO fix this
            print(artwork_filename)
            return filename
        else:       
            error = 'Wrong filetype!! Please use one of these: ' + str(ALLOWED_EXTENSIONS)
            print(error)