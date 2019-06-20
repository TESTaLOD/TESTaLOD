import html
import json
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from owlready2 import *


def unescaper(string):
    unescaped_string = html.unescape(string)
    return (unescaped_string)

# ************************************************************************

def json_cleaner(json_data):   
    json_dict = json.loads(json_data)
    elements = json_dict.get("results")
    elements = elements.get("bindings")
    return elements

def query_on_toyset(query_string, toyset_string):
    g = rdflib.Graph()
    try:
        g.parse(toyset_string, format="ttl")
    except:
        g.parse(toyset_string, format="xml")
    qres = g.query(query_string)
    query_result = json_cleaner(qres.serialize(format="json"))
    return query_result

def query_on_data(string, endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(string)
    sparql.setReturnFormat(JSON)
    query_result = sparql.query().convert()
    query_result = query_result.get("results")
    query_result = query_result.get("bindings")
    return query_result

def json_comparer(query_result, expected_result):
    result_list = [x for x in expected_result if x in query_result]
    lista = []
    for x in expected_result:
        diz = {}
        if x in result_list:
            diz['color'] = 'Green'
        else:
            diz['color'] = 'Red'
        diz['content'] = x
        lista.append(diz)

    if len(result_list) == len(expected_result): # 10 su 10 (li trova tutti)
        # TABELLA VERDE: per ogni elemento di expected_result
        return True, None, lista
    else:
        var = len(expected_result) - len(result_list) # 0 su 10 (non ne trova nessuno)
        if var == len(expected_result):
            return False, None, lista
            # TABELLA ROSSA: per ogni elemento di expected_result
        else:
            check_list = [m for m in expected_result if m not in result_list] # da 1 a 9 (ne trova qualcuno)
            #tabella colorata VERDE/ROSSA
            return True, str(len(check_list)), lista


def final_function (query_string, expected_string, toyset, endpoint): 
    if toyset:
        return json_comparer(query_on_toyset(unescaper(query_string), unescaper(toyset)), json_cleaner(unescaper(expected_string)))
    elif endpoint:
        return json_comparer(query_on_data(unescaper(query_string), unescaper(endpoint)), json_cleaner(unescaper(expected_string)))
    else:
        return "nodata", None, None

def statmaker (listot, time):
    good = 0
    miss = 0
    bad = 0
    for x in listot:
        if x["status"] == True and not x["missingnumber"]:
            good += 1
        elif x["status"] == False:
            bad += 1
        elif x["status"] == True and x["missingnumber"]:
            miss += 1
    result = list()
    result.append(good)
    result.append(miss)
    result.append(bad)
    result.append(time)
    return result


def API_url(githubfolderurl):
    githubfolderurl = githubfolderurl.split("//")[1]
    if ("/tree/master/" in githubfolderurl):
        githubfolderurl = githubfolderurl.split("master/", 1)
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

    return(url)

def subfinder(url, filekeyword, parent):
    req = requests.get(url)
    req = req.json()
    test_list = list()
    for x in req:
        if x['download_url']:
            if x['download_url'].endswith('.owl'):
                if filekeyword and filekeyword in x['name']:
                    test_list.append(x['download_url'])
                elif filekeyword is None:
                    test_list.append(x['download_url'])
        else:
            test_list.append(subfinder(API_url(x['html_url']), filekeyword, x['html_url']))
    dict_test = dict()
    if test_list:
        dict_test[parent]= test_list
    else:
        dict_test[parent] = None
    return dict_test

def finder(url, filekeyword, parent):
    req = requests.get(url)
    req = req.json()
    test_list = list()
    for x in req:
        if x['download_url']:
            if x['download_url'].endswith('.owl'):
                if filekeyword and filekeyword in x['name']:
                    test_list.append(x['download_url'])
                elif filekeyword is None:
                    test_list.append(x['download_url'])

    dict_test = dict()
    if test_list:
        dict_test[parent] = test_list
    else:
        dict_test[parent] = None
    return dict_test



def testaction (test):

        onto = get_ontology(test).load()
        ontolist = list()
        ontolist.append(test)

        expecteddata = list(onto.metadata.hasExpectedResult)[0]
        ontolist.append(expecteddata)

        datatype = list(onto.metadata.hasInputTestDataCategory)[0]
        ontolist.append(str(datatype).split('.')[1])

        datauri = list(onto.metadata.hasInputTestDataUri)[0]
        ontolist.append(datauri)

        querydata = list(onto.metadata.hasSPARQLQueryUnitTest)[0]
        ontolist.append(querydata)
        #testalod = Namespace("https://raw.githubusercontent.com/TESTaLOD/TESTaLOD/master/ontology/testalod.owl#")
        if str(datatype).split('.')[1] == "ToyDataset":
            status, missing, matchedlist = final_function(querydata, expecteddata, datauri, None)
        elif str(datatype).split('.')[1] == "SPARQLendpoint":
            status, missing, matchedlist = final_function(querydata, expecteddata, None, datauri)
        if status == "nodata":
            return "nodata"
        else:
            resultdict = dict()

            resultdict["input"] = ontolist
            resultdict["status"] = status
            resultdict["matched"] = matchedlist
            resultdict["missingnumber"] = missing

            return resultdict
