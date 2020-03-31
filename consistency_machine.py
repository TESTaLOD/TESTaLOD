import requests
from owlready2 import *
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import XSD
def consistency_action(test):
    ontolist = list()
    onto = get_ontology(test).load()
    ontolist.append(test)
    print(onto.metadata.hasInferenceRequirement)
    try:
        requirements = list(onto.metadata.hasInferenceRequirement)[0]
    except:
        requirements = list(onto.metadata.hasRequirement)[0]
    ontolist.append(requirements)
    datatype = list(onto.metadata.hasInputTestData)[0]
    ontolist.append(datatype)
    status = consistency_check(test)


    if status == "nodata":
        return "nodata"
    else:
        resultdict = dict()

        resultdict["input"] = ontolist
        resultdict["status"] = status

        return resultdict

def consistency_check(test):
    try:
        r = requests.get("https://testalodinf.herokuapp.com/consistencyCheck?IRI=" + test)
    except:
        print("REQUEST")
    if r.status_code == 200:
        j0 = Namespace("http://www.ontologydesignpatterns.org/schemas/testannotationschema.owl#")
        g = Graph()
        g = g.parse(data=str(r.text))
        for x, y, z in g:
            if y == j0.hasActualResult and z == Literal('true',datatype=XSD.boolean):
                return True
            elif y == j0.hasActualResult and z == Literal('false',datatype=XSD.boolean):
                return False
    else:
     return "nodata"

def consistent_statmaker(listot, time):
    good = 0
    bad = 0
    for x in listot:
        if x["status"] == True:
            good += 1
        elif x["status"] == False:
            bad += 1
    result = list()
    result.append(good)
    result.append(bad)
    result.append(time)
    return result