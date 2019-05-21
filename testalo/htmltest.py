

#SERVER SIDE TEST











from flask import Flask, render_template, request
from owlready2 import *
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', active='1')

@app.route('/', methods=['POST'])


def test_finder ():
    githubfolderurl = request.form['url']
    try:
        githubfolderurl = githubfolderurl.split("//")[1]
        if ("master" in githubfolderurl):
            githubfolderurl = githubfolderurl.split("master/")
            path1 = githubfolderurl[0].split("/")
            filepath = githubfolderurl[1]
            user = path1[1]
            repos = path1[2]
            url = "https://api.github.com/repos/" + user + "/" + repos + "/contents/" + filepath

        else:
            path1 = githubfolderurl.split("/")
            user = path1[1]
            repos = path1[2]
            url = "https://api.github.com/repos/" + user + "/" + repos + "/contents"
    except:
        return render_template('index.html', wronguri=True, active='1')
    test_list = list()

    #LA FORMULA MAGGGGICA!
    #url = 'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        for x in req:
            if "testcase" in x['name']:
                test_list.append(x['download_url'])

    else:
        return render_template('index.html', emptyfolder=True, active='1')

    return render_template('index.html', data=test_list, active='2')


@app.route('/test', methods=['POST'])

def test ():
    values = request.form.getlist('test')
    list_total = list()
    for test in values:
        onto = get_ontology(test).load()

        ontolist = list()
        ontolist.append(test)

        ontolist.append(list(onto.metadata.hasExpectedResult)[0])

        ontolist.append(list(onto.metadata.hasInputTestData)[0])

        ontolist.append(list(onto.metadata.hasSPARQLQueryUnitTest)[0])
        list_total.append(ontolist)

    return render_template('index.html', result=list_total, active='3')

if __name__ == '__main__':
  app.run (host='0.0.0.0')

#url = 'https://api.github.com/repos/ICCD-MiBACT/ArCo/contents/ArCo-release/test/CQ'


#test_finder("https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ", "testcase")