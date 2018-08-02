# Slip-Line-Calculator
A quick Python program to take S-C strikes/dips and find the slip lines

***If you have more than 20 measurements, it is recommended that you close any programs that use a lot of RAM such as Chrome and Firefox, or ArcGIS/QGIS. As pyplot creates figures it holds each in memory until the program it done and cane take up a large amount of memory. 

Thank you for using Slipline Calculator. This program was written by Ben Weinmann (Auburn University, brw0025@auburn.edu). It was built upon previous work by John Whitmore. And his work was built upon previous work by David Allison at the University of South Alabama.

**USAGE:

**Python 3.x is required; will not work with Python2.x yet as I haven't made the adequate exceptions for it.
On Linux open a new terminal window.
On Windows hit the Windows key, type cmd, and hit enter and a new command line terminal will open. 


**CALLING THE PROGRAM IN THE COMMAND LINE

**SYNTAX:

*Linux: 

python3 sliplineCalc.py -i [somefile.csv] -o [anewfiletobewrittento.csv] 
python3 sliplineCalc.py --dataIn [somefile.csv] --dataOut [anewfiletobewrittento.csv]

Alternatively the arguments can be left out and the program will prompt the user for input.In that case use: python3 sliplineCalc.py

*Windows:

python sliplineCalc.py -i [somefile.csv] -o [anewfiletobewrittento.csv]
Or alternatively, the command line arguments may be left out and the user will be prompted to give input.

*Help:

Type python(3) sliplineCalc_0.5.py -h for full help.

**DATA

The data can be located in an any folder, and that path to that folder can be passed as an argument with -i or --dataIn, but it will work best if the data and the program are in the same folder.
The program can probably read a .txt just fine, but has to date only been tested using .csv files. It will also write to .csv, but can write to text, but it is a little messy.

A simple .csv file should be used. It MUST be formatted as follows:
objectID, c_strike, c_dip, s_strike, s_dip
string    int       int    int       int

See example .csv 


*PASSING IN DATA

-i or --dataIn [name of file + extension]
Example: -i StrikeAndDip.csv
         --dataOut strikeanddip.csv


*DATA OUT

-o or --dataOut [file to be created + extension]
Example: -o output.csv
         --dataOut somethingQuad.csv
