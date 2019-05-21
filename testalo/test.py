from owlready2 import *
from rdflib import *

x = 
while x != 0:
    #print (x)
    if  x < 10 :
        xst = str("0"+ str(x))
    elif x == 26:
        xst = str(str(x)+"a")
    else:
        xst = x
    url = "https://raw.githubusercontent.com/ICCD-MiBACT/ArCo/master/ArCo-release/test/CQ/testcase-" + str(xst) + ".owl"
    onto = get_ontology(url).load()


    a = (list(onto.metadata.hasExpectedResult))

    b = (list(onto.metadata.hasInputTestData))

    c = (list(onto.metadata.hasSPARQLQueryUnitTest))

    if not c:
        print(x)
    x = x-1