# QUERY_SPARQL.PY
# This is a module used for connecting OWL to python with SEPA (https://github.com/arces-wot/SEPABins)
# There's a function (connessione(...)) which is used for querying OWL.
# This function has two parameters (the name of the query, for example "QUERY_ALL") --> references to JSAP file, and the path of the JSAP file.
# It also has a return for return the string.
# This module also split and replace all useless char.
# Remember to change the path.


# Packages for SEPA
from sepy.SAPObject import *
from sepy import *
import json
from sepy.SEPA import *

# for deleting files
import os


# create the connection with OWL and then it runs the query
def connessione(sparql_query, path):
    # Open the jsap and connection
    mySAP = open(path,"r")
    sap = SAPObject(json.load(mySAP))
    sc = SEPA(sapObject=sap)

    # querying
    result = sc.query(sparql_query)
    str1 = json.dumps(result) # convert dict into string

    # the follow lines are used for extrapolating only the correct values of the result
    str1 = str1.replace(" ","").replace('"value":"',"&&&").replace("{","").replace("}","").replace(",","\n")
    text_file = open("Output.txt", "w")
    text_file.write(str1)
    text_file.close()
    with open("output.txt","r") as fin:
        with open("input.txt","w") as fout:
            for line in fin:
                if line.startswith('&&&'):
                    fout.write(line)
                else:
                    fout.write("")
    with open("input.txt","r") as file:
        query_result = file.read().replace("&&&","").replace("[","").replace("]","").replace('"',"")
    os.remove("input.txt")
    os.remove("output.txt")

    # return the string (It's a string vector with only the values)
    return query_result


# insert only one value
def insert_one(sparql_query, path, force_binding):
    mySAP = open(path,"r")
    sap = SAPObject(json.load(mySAP))
    sc = SEPA(sapObject=sap)
    sc.update(sparql_query,
        forcedBindings=force_binding)


def other_query(path_jsap, sparql_query, path):
    mySAP = open(path,"r")
    sap = SAPObject(json.load(mySAP))
    sc = SEPA(sapObject=sap)
    sc.update(sparql_query,
        forcedBindings=force_binding)
