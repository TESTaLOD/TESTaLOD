from flask import Flask, render_template, request
from cq_test_machine import *
import time
from werkzeug.utils import secure_filename


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
        subfolder = request.form['subfo']
    except:
        subfolder = None

    try:
        githubfolderurl = request.form['url']
        try:
            url = API_url(githubfolderurl)
        except:
            return render_template('index.html',local=False, wronguri=True, active='1')
        try:
            if subfolder:
                test_list = subfinder(url, filekeyword, githubfolderurl)
            else:
                test_list = finder(url, filekeyword, githubfolderurl)

        except:
            return render_template('index.html',local=False, emptyfolder=True, active='1')
        ntot = len(test_list)
        return render_template('index.html', data=test_list, leng=ntot, active='2', local=False)
    except:
        req_list = request.files.getlist('localfile')
        start = time.time()
        list_local = list()
        for filesreq in req_list:
            try:
                filename = secure_filename(filesreq.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                filesreq.save(filepath)
                resulttest = testaction(filepath)
                if resulttest == "nodata":
                    os.remove(filepath)
                    resultdict = dict()
                    resultdict["input"] = filename
                    resultdict["status"] = "errorinput"
                    resultdict["matched"] = None
                    resultdict["missingnumber"] = None
                    list_local.append(resultdict)
                else:
                    list_local.append(resulttest)
                os.remove(filepath)
            except:
                os.remove(filepath)
                resultdict = dict()
                resultdict["input"] = filename
                resultdict["status"] = "errorinput"
                resultdict["matched"] = None
                resultdict["missingnumber"] = None
                list_local.append(resultdict)
        end = time.time()
        timetot = round(end - start, 2)
        stats = statmaker(list_local, timetot)
        return render_template('index.html', result=list_local, stats=stats, active='3', local=True)



@app.route('/test', methods=['POST'])

def test ():
    values = request.form.getlist('test')

    if values:
        start = time.time()
        list_total = list()
        for test in values:
            try:
                resulttest = testaction(test)
                if resulttest == "nodata":
                    resultdict = dict()
                    resultdict["input"] = test
                    resultdict["status"] = "errorinput"
                    resultdict["matched"] = None
                    resultdict["missingnumber"] = None
                    list_total.append(resultdict)
                elif resulttest:
                    list_total.append(resulttest)
            except:
                resultdict = dict()
                resultdict["input"] = test
                resultdict["status"] = "errorinput"
                resultdict["matched"] = None
                resultdict["missingnumber"] = None
                list_total.append(resultdict)
        end = time.time()
        timetot = round(end - start, 2)
        stats = statmaker(list_total, timetot)
        return render_template('index.html', result=list_total, stats= stats, active='3', local= False)


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == '__main__':
  app.run (host='0.0.0.0')




#url = 'https://api.github.com/repos/ICCD-MiBACT/ArCo/contents/ArCo-release/test/CQ'


#test_finder("https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ", "testcase")



