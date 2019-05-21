from owlready2 import *
from rdflib import *
import requests



def test_finder (githubfolderurl, keyword = None):

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

    test_list = list()

    #LA FORMULA MAGGGGICA!
    #url = 'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'

    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        for x in req:
            if keyword:
                if keyword in x['name']:
                    test_list.append(x['download_url'])
            else:
                test_list.append(x['download_url'])
    else:
        print('Content was not found.')

    for test in test_list:

        onto = get_ontology(test).load()

        print(test)

        print (list(onto.metadata.hasExpectedResult))

        print (list(onto.metadata.hasInputTestData))

        print (list(onto.metadata.hasSPARQLQueryUnitTest))

#url = 'https://api.github.com/repos/ICCD-MiBACT/ArCo/contents/ArCo-release/test/CQ'


test_finder("https://github.com/ICCD-MiBACT/ArCo/tree/master/ArCo-release/test/CQ", "testcase")