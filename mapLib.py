#!/bin/python2
import os
from PIL import Image
import csv
import pickle
import numpy as np

# update adjacencies basing on 
def updateAdj():
  adjIn = 'adjacencies.csv'
  adjOut = 'adjacenciesNEW.csv'
  filename = 'definitionNEW.csv'
  # create id list
  with open(filename, 'rb') as csvSrc:
    base = csv.reader(csvSrc, delimiter=';')
    idList = set()
    n = 0
    for row in base:
      if (n != 0):
        idList.add(int(row[0]))
      n = 1

  with open(adjIn, 'rb') as csvAdj:
    out = open(adjOut, 'wb')
    base = csv.reader(csvAdj, delimiter=';')
    csvOut = csv.writer(out, delimiter=';')
    # check from and To
    first = True
    for row in base:
      if ( first == False):
        idFrom = int(row[0])
        idTo = int(row[1])
        if(idFrom in idList or idTo in idList):
          print ("yes")
          csvOut.writerow(row)
        else:
          print ("not")
      else:
        first = False 
        csvOut.writerow(row)


# Class for provinces.bmp handling
#
class ProvincesBMP:
  
  def __init__(self, filename = None):
    if (filename is None):
      self.data = None
      print('You must provide province definition csv file!')
      return

    else:
      self.data = Image.open(filename)

  def getColors(self, filename=None):
    """Creates a unique table of colors from bmp image"""
    # create a set
    newProvSet = set()
    counter = 0
    pixels = self.data.getdata()
    for pixel in pixels:
      color = tuple(pixel)
      newProvSet.add(color)
      #increase counter
      if (counter < len(newProvSet)):
        counter = counter + 1

    self.colorset = newProvSet

    if (filename is None):
      return newProvSet
    else:
      with open(filename, 'wb') as out:
        pickle.dump(newProvSet, out)
        out.close()
        return newProvSet


  def generatePropertyMap(self, provinceData, key):
    '''Generate image that have specific feature marked on province map'''
    # get the list of values for the field key
    values = provinceData.getUniqueValues(key)
    # iterate through provinces a assign color to each one basing
    # on the value 
    newColors = {}
    i=0

    palleteFile = open(key+'_pallete.txt','w')
    palleteW = csv.writer(palleteFile)
    # generate rbg pallete for unique values and saveit
    for val in values:
      
      r=i%8
      g=((i-r)/8) % 8
      b=((i-g*8-r)/64) % 8
      i=i+1
      newColors[val] = [16+r*32,16+g*32,16+b*32]
      palleteW.writerow([val] +[16+r*32,16+g*32,16+b*32]) 

    # close the pallete file      
    palleteFile.close()


    #Generate the color swap map
    colorMapTable = []
    for province in provinceData.data:
      cfrom = list(provinceData.getColor(province))
      cto = newColors[province[key]]
      colorMapTable.append([cfrom,cto])

    # Ready to swap colors
    self._swapColors(colorMapTable)

    # save
    self.data.save(key+'_map.png')
    

  def _swapColors(self, colorMapTable):
    '''Internal function'''
    data = np.array(self.data)
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
  
    for pair in colorMapTable:
      cfrom = pair[0]
      cto = pair[1]
      # DEBUG: print(pair)
      mask = (red == cfrom[0]) & (green == cfrom[1]) & (blue == cfrom[2])
      data[:,:,:3][mask] = [cto[0], cto[1], cto[2]]
    
    self.data = Image.fromarray(data)


  def save(self,filename):
    self.data.save(filename)


#
# Class for handling positions file
#

# Main function fixes the csv file that mapfiller tool uses
# for generation
#
class ProvincesData:

  def __init__(self, filename = None):
    if (filename is None):
      self.data = None
      print('You must provide province definition csv file!')
      return

    else:
      csvIn = open(filename, 'r')
      data = csv.reader(csvIn, delimiter=';')
      self.fieldnames = next(data)

      # Load whole file into memory and close the file
      data = csv.DictReader(csvIn, delimiter=';', fieldnames=self.fieldnames)
      self.data = []

      # Load each field except first and empty into memory 
      for row in data:
        if (row['Province ID'] != ''):
          self.data.append(row)
      
      #print(self.data[0])
      csvIn.close();
      print('Province definition file: ' + filename + ' loaded.')


  def write(self, filename, recomputeIds=True):
    '''Writes down the output csv file'''
    if (recomputeIds):
      self._recomputeId()

    csvOUT = open(filename, 'w')
    outdata = csv.DictWriter(csvOUT, delimiter=';', fieldnames=self.fieldnames)
    outdata.writeheader();
    outdata.writerows(self.data)
    csvOUT.close()
      
  def _recomputeId(self):
    '''Private function should be executed each time provinces are changed to recompute ids'''
    n=1
    for province in self.data:
      province['Province ID'] = n
      n=n+1
 

  def filterByColor(self, colors):
    '''Colors is a table of colors which we want to stay in def file'''

    if self.data is None:
      return

    temp = []
    for province in self.data:
      color = self.getColor(province)
      if (color in colors):
        temp.append(province)
      else: 
        print ('Province: ' + province['Province Name'] + ' dropped.')
    self.data = temp

  def countProvinces(self):
    '''Count the amounts of provinces currently in the file'''
    return len(self.data)


  def getColor(self, province):
    '''Return tuple with province color'''
    print(province['Red'])
    red = int(province['Red'])
    green = int(province['Green'])
    blue = int(province['Blue'])
    return tuple([red,green,blue])

  
  def getUniqueValues(self, key):
    '''Returns a Set of all cultures on map'''
    uniqueVals = set()
    try:
      self.fieldnames.index(key)
    except ValueError:
      return 

    for province in self.data:
      uniqueVals.add(province[key])
    return uniqueVals
     

  def filterByField(self, key, valuesSet):
    '''Filter the list of provinces with fields "key" in values set'''
    temp = []
    try:
      self.fieldnames.index(key)
    except ValueError:
      return 

    for province in self.data:
      if (province[key] in valuesSet):
        temp.append(province)
    self.data = temp
