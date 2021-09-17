# CREATE_SPARQL.PY
# This program creats a new JSAP file (using path like parameter) for customing query.
# The first part of JSAP is the same of CHAT.JSAP and it uses SEPA.


# packages
import query_sparql # used for opening a new connection to the graphs
import os # used for read - write files


# first part of JSAP: connection parameters
# the line &&&&& is replaced with the correct custom query
string = """{
	"host": "localhost",
	"oauth": {
		"enable": false
	},
	"sparql11protocol": {
		"protocol": "http",
		"port": 8000,
		"query": {
			"path": "/query",
			"method": "POST",
			"format": "JSON"
		},
		"update": {
			"path": "/update",
			"method": "POST",
			"format": "JSON"
		}
	},
	"sparql11seprotocol": {
		"protocol": "ws",
		"reconnect" : true,
		"availableProtocols": {
			"ws": {
				"port": 9000,
				"path": "/subscribe"
			},
			"wss": {
				"port": 9443,
				"path": "/secure/subscribe"
			}
		}
	},
    "graphs": {

"default-graph-uri": [],

"using-graph-uri": []

},

"namespaces": {

"schema": "http://schema.org/",

"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",

"sha": "http://unibo.it/ontology/SmartHospitalAssistant#"

},

"queries": {

&&&&&

}
} """


# return the intestation of JSAP
def pass_sparql():
	return string


# it creats a new file with the correct query
# path_new --> the path of the new JSAP file
# stringa --> the intestation of JSAP
# it creats two temp files: program writes the intestation on the first temp
# Then the first temp is copied on the second temp changing "&&&&&" into a query
# It returns a string with the results
def creating(path_new, stringa):
	text_file = open(path_new + "\\temp1.jsap", "w")
	text_file.write(pass_sparql())
	text_file.close()
	with open(path_new + "\\temp1.jsap","r") as fin:
		with open(path_new + "\\temp2.jsap","w") as fout:
			for line in fin:
				if line.startswith('&&&&&'):
					fout.write(stringa)
				else:
					fout.write(line)
	os.remove(path_new + "\\temp1.jsap")
	stringa = query_sparql.connessione("QUERY", path_new + "\\temp2.jsap")
	os.remove(path_new + "\\temp2.jsap")
	return stringa
