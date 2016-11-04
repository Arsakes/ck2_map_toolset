#!/bin/python
import grako
import json

grammar = """
file = { block }*;
    block = id '=' brackets { /\n/ }*;
    brackets = '{' pos rot hei '}' ;
    fnum = /-?[0-9]+[.][0-9]+/ ;
    numarray = { fnum }+ ;
    pos = 'position=' '{' numarray '}' ;
    rot = 'rotation=' '{' numarray '}' ;
    hei = 'height=' '{' numarray '}' ;
    id = /[0-9]+/ ;
"""
#comment = /#.*?$/ ;

model = grako.genmodel('Bracketed', grammar)
#model = grako.genmodel('Bracketed', com)

text="""# Endring
	1=
	{
		position=
		{
2092.000 2042.000 2082.000 2039.000 2092.000 2042.000 2091.000 2041.000 2096.000 2057.000 		}
		rotation=
		{
0.000 0.000 0.000 0.000 2.356 		}
		height=
		{
0.000 0.000 0.000 20.000 0.000 		}
	}
# Dupsko
	2=
	{
		position=
		{
2092.000 2042.000 2082.000 2039.000 2092.000 2042.000 2091.000 2041.000 2096.000 2057.000 		}
		rotation=
		{
0.000 0.000 0.000 -0.000 2.356 		}
		height=
		{
0.000 0.000 0.000 20.000 0.000 		}
	}"""


#ast = model.parse(text, "file")
#print('LEN:',json.dumps(ast, indent=2))
#print('LEN: ', len(ast))


#print(ast[1][1])

class PositionsData:
  
  def __init__(self, filename):
    with open(filename, 'r', encoding='latin-1', errors='ignore') as content:
      data = content.read()
      #print(data)
      parsed_data = model.parse(data, "file", eol_comments_re="#.*?$")
      content.close() 
      # Reorganize data
      self.data_organized = {}
      #print(parsed_data[0])
      for block in parsed_data:
        org_block = {
          'position' : [float(i) for i in block[2][1][2]],
          'rotation' : [float(i) for i in block[2][2][2]],
          'height' : [float(i) for i in block[2][3][2]]
        }
        self.data_organized[int(block[0])] = org_block
        #print(json.dumps(block, indent=2))

 
  def getProvince(self, i):
    return self.data_organized[i]

  def move(self, x, y):
    '''Changes the positions by constant vector for all provinces'''
    for i in self.data_organized:
      positions = self.data_organized[i]['position']
      print('OLD: ', positions)
      for i in range(len(positions)):
        if (i%2 == 0):
          positions[i] += x
        else:
          positions[i] += y
      print('NEW:' , positions)


  def update(self, provdef):
    '''Update the data in positions according to provdef file'''
    idMap = provdef.idMap
    
    newSet = {}
    nameSet = {}

    for province in provdef.data:
        name = province['Province Name']
        newId = int(province['Province ID'])
        nameSet[newId] = name

    for oldId in self.data_organized:
      if oldId in provdef.idMap:
        newId = provdef.idMap[oldId]
        newSet[newId] = self.data_organized[oldId]
        # set name
        name = nameSet[newId]
        newSet[newId]['comment'] = name
      else:
        print('Positions: province with id=' + str(oldId) + ' deleted from set.')
    self.data_organized = newSet


  def write(self, filename):
    '''Writes down the changed file'''
    outfile = open(filename, 'w')
    def fors(x):
      return "{0:.3f}".format(x)

    for i in self.data_organized:
      block = self.data_organized[i]
      # Starting brackets
      outfile.write('# ' + block['comment']+ '\n')
      outfile.write('	' + str(i) + '=\n	{\n')
      # Positions
      pos = ' '.join(fors(x) for x in block['position'])
      outfile.write('		position=\n		{\n')
      outfile.write(pos + '		}\n') 
      # Rotation
      rot = ' '.join(fors(x) for x in block['rotation'])
      outfile.write('		rotation=\n		{\n')
      outfile.write(rot + '		}\n') 
      # Height
      height = ' '.join(fors(x) for x in block['height'])
      outfile.write('		height=\n		{\n')
      outfile.write(height + '		}\n') 
      # Final
      outfile.write('	}\n') 

    outfile.close()
#posdata = PositionsData('positions.txt')

