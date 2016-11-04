#!/bin/python
from mapLib import *
from grammar import *
import pickle


# Firstly we construct province information using provinceDef.xls/csv
# this is our base file we want to change!
a=ProvincesData('./examples/provinceDef.csv')

# In order to know in which way we want to change provinceDef.xls/csv
# We need bmp image 
b=ProvincesBMP('./examples/provinces_v2.bmp')

# Get all colors (so provinces) exsiting in provinces_v2.bmp
colors = b.getColors()

# Use this info to delete all provs not existing in base provinceDef file
a.filterByColor(colors)


# Counting
a.countProvinces()

# Checking 
b.checkMissing(a)

# Write the new csv file
a.write('provinceDef_v2.csv')
# after this you should transform provinceDef_v2.csv  into XLS excel file and then use CK2Tools


###########################################
# 
# Positions update
#
# Remember we have also positions.txt to update -> most likely we have changed the map geometry so adjustment is needed
# This instruction takes 
posdata = PositionsData('./examples/positions.txt')

# Translate the positions
posdata.move(-1579,-1162)

# Use the province definitions to updated positions data 
#(remember some provs are deleted from existence and we have OLD version of positions data)
posdata.update(a)

# Save updated positions data file
posdata.write('posnew.txt')
