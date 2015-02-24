#!/usr/bin/python -i
## Change above to point to your python. The -i option leaves you in interactive mode after the script has completed. Use ctrl-d to exit python.

## Import the pycudd module
import pycudd

## Import the json module
import json

from collections import Counter

##
## The next two steps are essential. PyCUDD has been set up so that the multitudinous
## references to the DdManager are obviated. To achieve this, there is the notion of
## a default manager. Though you may have as many DdManager objects as you want, only
## one of them is active at any given point of time. All operations that require a
## manager use the manager that last called the SetDefault method. 
## 
## NOTE: The DdManager constructor takes the same arguments as Cudd_Init. Refer ddmanager.i
## to see the default values (which can be overriden when you call it)
##
mgr = pycudd.DdManager()
mgr.SetDefault()


## Read in the json formatted BLN
import json
from pprint import pprint
json_data=open('c6288.json')

data = json.load(json_data)
pprint(data)
newDS = []


#try:
#
#    dataform = str(response_json).strip("'<>() ").replace('\'', '\"')
#    struct = json.loads(dataform)

#json.loads('c17.json')
#print myGraph

## This simple example finds the truths set of f = (f0 | f1) & f2 where
## f0 = (x4 & ~x3) | x2
## f1 = (x3 & x1) | ~x0
## f2 = ~x0 + ~x3 + x4
## and x0 through x4 are individual Boolean variables

## Create bdd variables x0 through x4
x = []
order = []
## Create subfunction list
sf = []
i = 0
num_inputs = 0
num_outputs = 0

for node in data['nodes']:
    if node['gate'] == 'i':
	x.append( mgr.IthVar(i))
	order.append(node['id'])
        i += 1
    if node['gate'] == 'o':
	num_outputs += 1
    else:
	newDS.append( {'gate':node['gate'], 'input':[], 'output':node['id'] } )

num_inputs = i
io = num_inputs + num_outputs

while i > 0:
	i =  i - 1
	sf.append([])

print len(x)
print len(sf)

for id in order:
    print 'id is ', id
    for link in data['links']:
        if link['source'] == id-1:
            print link['source']
            for gate in newDS:
              if ( gate['output'] == link['target'] ):
                  gate['input'].append( link['source'] - 1 )

for id in order:
    for item in newDS:
	c = mgr.IthVar(0)
	d = mgr.IthVar(0)
	if len(item['input']) == 2:
            a = item['input'][0]
            if a > num_inputs:
                a = a - io
                c = sf[id-1][a]
            else:
                c = x[a]
            b = item['input'][1]
            if b > num_inputs:
                b = b - io
                d = sf[id-1][b]
            else:
                d = x[b]

	if item['gate'] == 'and':
	    sf[id-1].append ( c & d )
	if item['gate'] == 'or':
	    sf[id-1].append( c + d )
	if item['gate'] == 'not':
	    if len(item['input']) == 1:
		a = item['input'][0]
                if a > num_inputs:
		    a = a - io
                    c = sf[id-1][a]
                else:
                    c = x[a]
      		sf[id-1].append( ~c )
num_nodes = 0
for each in sf:
	num_nodes = num_nodes + len(each)
print 'Number of Nodes: ', num_nodes
f = sf[len(x)-1][0]
print sf[len(x)-1][0]
## Compute functions f0 through f2

#f0 =( x[0] & x[1] )
# f0 = (x4 & ~x3) | x2
# f1 = (x3 & x1) | ~x0
# f2 = ~x0 + ~x3 + x4

## Compute function f
#f = (f0 | f1) & f2
# f = f0

## Print the truth set of f
f.PrintMinterm()


