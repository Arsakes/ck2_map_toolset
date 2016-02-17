#!/bin/python2
from mapLib import *
import pickle


#colors = pickle.load(open('uniqueList', 'rb'))
#createSubDefCSV(colors, 'definition.csv', 'definitionNEW.csv')

#fixTheCSV(colors)

a=ProvincesData('provinceDef.csv')
b=ProvincesBMP('provinces2.bmp')
colors = b.getColors()
a.filterByColor(colors)
print(a.getUniqueValues('Culture'))
#b.generatePropertyMap(a, 'Culture')
a.write('provinceDef2.csv')


#b.save('newprov.bmp')
#b.getColors('newColors')
#print(pickle.load(open('newColors','rb')))
