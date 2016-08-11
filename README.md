Map modding toolset
====================
Made by pietrko <p.l.stepnicki@gmail.com>
This set of scripts is supposed to be used CK-TOOLSv18+

It allows of filtering ready to use provinceDef file for CK-TOOLS
in various ways.


Workflow
===================

1. Create classes and load data

  provbmp = ProvincesBMP(...)
  provdef = ProvincesData(...)

2. Filter out provinces you don't want using colors from Provinces Data
  new\_colors = provbmp.getColors()
  provdev.filterByColor(new\_colors)
  
3. Do stuff

Input: 
provinceDef.csv
provinceMask.bmp

Output:
provinceDef.csv

