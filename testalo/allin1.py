from flask import Flask, render_template, request
from owlready2 import *
import requests
from cq_test_machine import *
import time
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', active='1')

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
            return render_template('index.html', wronguri=True, active='1')

        #LA FORMULA MAGICA
        #url = 'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

        try:
            test_list = finder(url, filekeyword, githubfolderurl)
            print(test_list)


        except:
            return render_template('index.html', emptyfolder=True, active='1')
        ntot = len(test_list)
        return render_template('index.html', data=test_list, leng=ntot, active='2')
    except:
        test_list = list()
        req_list = request.files.getlist('folder')
        for filesreq in req_list:
            test_list.append(filesreq.filename)
        ntot = len(test_list)

        #TODO if len = 0 ---> html: 0 FILES

        return render_template('index.html', data=test_list, leng=ntot, active='2')

@app.route('/test', methods=['POST'])

def test ():
    values = request.form.getlist('test')
    try:
        toysetkeyword = request.form['toysetkeyword']
    except:
        toysetkeyword = None
    start = time.time()
    try:
        list_total = list()
        for test in values:
            onto = get_ontology(test).load()

            ontolist = list()
            ontolist.append(test)

            expecteddata = list(onto.metadata.hasExpectedResult)[0]
            ontolist.append(expecteddata)

            inputtestdata = list(onto.metadata.hasInputTestData)[0]
            ontolist.append(inputtestdata)

            querydata = list(onto.metadata.hasSPARQLQueryUnitTest)[0]
            ontolist.append(querydata)


            status, missing, missinglist = final_function(inputtestdata, querydata, expecteddata, toysetkeyword)
            resultdict = dict()

            resultdict["input"] = ontolist
            resultdict["status"] = status
            resultdict["missing"] = missinglist
            resultdict["missingnumber"] = missing

            list_total.append(resultdict)

        end = time.time()
        timetot = round(end - start, 2)
        stats = statmaker(list_total, timetot)
        return render_template('index.html', result=list_total, stats= stats, active='3')
    except:
        if list_total:
            end = time.time()
            timetot = round(end - start,2)
            stats = statmaker(list_total, timetot)
        else:
            stats = None
        return render_template('index.html', problem= test,  stats= stats, result=list_total, active='3')



if __name__ == '__main__':
  app.run (host='0.0.0.0')

#url = 'https://api.github.com/repos/ICCD-MiBACT/ArCo/contents/ArCo-release/test/CQ'


#test_finder("https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ", "testcase")



