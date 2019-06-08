from flask import Flask, render_template, request
#from owlready2 import *
from cq_test_machine import *
import time, shutil
from werkzeug.utils import secure_filename
import uuid
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'temp'


@app.route('/')
def index():
    return render_template('index.html', local=False, active='1')

@app.route('/', methods=['POST'])


def test_finder ():
    try:
        filekeyword = request.form['filekeyword']
    except:
        filekeyword = None

    try:
        githubfolderurl = request.form['url']
        try:
            url = API_url(githubfolderurl)
        except:
            return render_template('index.html',local=False, wronguri=True, active='1')
        try:
            test_list = finder(url, filekeyword, githubfolderurl)
        except:
            return render_template('index.html',local=False, emptyfolder=True, active='1')
        ntot = len(test_list)
        return render_template('index.html', data=test_list, leng=ntot, active='2', local=False)
    except:
        try:
            try:
                toysetkeyword = request.form['toysetkeyword']
            except:
                toysetkeyword = None

            try:
                endpoint = request.form['endpointurl']
            except:
                endpoint = None
            req_list = request.files.getlist('localfile')
            start = time.time()
            list_local = list()
            for filesreq in req_list:
                filename = secure_filename(filesreq.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                filesreq.save(filepath)
                resulttest = testaction(filepath, toysetkeyword, endpoint)
                if resulttest == "nodata":
                    os.remove(filepath)
                    if list_local:
                        end = time.time()
                        timetot = round(end - start, 2)
                        stats = statmaker(list_local, timetot)
                    else:
                        stats = None
                    return render_template('index.html', problemdata= True, problem= filepath, result=list_local, stats=stats, active='3', local=True)
                else:
                    list_local.append(resulttest)
                os.remove(filepath)
            end = time.time()
            timetot = round(end - start, 2)
            stats = statmaker(list_local, timetot)
            return render_template('index.html', result=list_local, stats=stats, active='3', local=True)
        except:
            os.remove(filepath)
            if list_local:
                end = time.time()
                timetot = round(end - start, 2)
                stats = statmaker(list_local, timetot)
            else:
                stats = None
            return render_template('index.html',probleminput= True, problem=filename, stats=stats, result=list_local, active='3', local=True)



@app.route('/test', methods=['POST'])

def test ():
    try:
        toysetkeyword = request.form['toysetkeyword']
    except:
        toysetkeyword = None

    try:
        endpoint = request.form['endpointurl']
    except:
        endpoint = None
    values = request.form.getlist('test')

    if values:
        start = time.time()
        try:
            list_total = list()
            for test in values:
                resulttest = testaction(test, toysetkeyword, endpoint)
                if resulttest == "nodata":
                    if list_total:
                        end = time.time()
                        timetot = round(end - start, 2)
                        stats = statmaker(list_total, timetot)
                    else:
                        stats = None
                    return render_template('index.html', problem=test, problemdata=True, result=list_total, stats=stats, active='3', local=False)
                elif resulttest:
                    list_total.append(resulttest)
            end = time.time()
            timetot = round(end - start, 2)
            stats = statmaker(list_total, timetot)
            return render_template('index.html', result=list_total, stats= stats, active='3', local= False)
        except:
            if list_total:
                end = time.time()
                timetot = round(end - start,2)
                stats = statmaker(list_total, timetot)
            else:
                stats = None
            return render_template('index.html',probleminput= True, problem= test, local= False, stats= stats, result=list_total, active='3')

if __name__ == '__main__':
  app.run (host='0.0.0.0')




#url = 'https://api.github.com/repos/ICCD-MiBACT/ArCo/contents/ArCo-release/test/CQ'


#test_finder("https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ", "testcase")



