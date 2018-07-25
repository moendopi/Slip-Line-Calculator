"""Slip line calculator to calculate the slip between S and C fabrics"""
import math, os, sys, csv, argparse, time
import numpy as np
import matplotlib.pyplot as plt
if sys.platform == 'win32':
    import winsound
    
try:
    import mplstereonet
except ImportError:
    print("Installing missing modules, please wait...\n")
    if sys.platform == 'win32':
        os.system('python get-pip.py')
    
    if sys.platform == 'linux':
        os.system('pip3 install mplstereonet')
    else:
        os.system('pip install mplstereonet')
    
# grab argument input from the user
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dataIn', help="Enter the name of the file, or the path to the file plus the file name")
parser.add_argument('-o','--dataOut', help="Enter the name of the file you want to be written to or the path plus the file name")
args = parser.parse_args()


def slipLine(objectID, c_strike, c_dip, s_strike, s_dip, quad):
    
    if s_strike <= 90 and quad.upper() == "E":
        s_pol_az = 270 + s_strike
    elif s_strike <= 90 and quad.upper() == "W":
        s_pol_az = 90 + s_strike
    elif s_strike >= 270 and quad.upper() == "E":
        s_pol_az = s_strike - 90
    else:
        s_pol_az = s_strike - 270
    
        
    if c_strike <= 90 and quad.upper() == "E":
        c_pol_az = 270 + c_strike
    elif c_strike <= 90 and quad.upper() == "W":
        c_pol_az = 90 + s_strike
    elif c_strike >= 270 and quad.upper() == "E":
        c_pol_az = c_strike - 90
    else:
        c_pol_az = c_strike - 270
        
    s_pol_plunge = 90 - s_dip
    c_pol_plunge = 90 - c_dip
    
    s_x = math.sin(math.radians(s_pol_az)) * math.sin(math.radians(90 - s_pol_plunge))
    c_x = math.sin(math.radians(c_pol_az)) * math.sin(math.radians(90 - c_pol_plunge))
    
    s_y = math.cos(math.radians(s_pol_az)) * math.sin(math.radians(90 - s_pol_plunge))
    c_y = math.cos(math.radians(c_pol_az)) * math.sin(math.radians(90 - c_pol_plunge))
    
    s_z = math.cos(math.radians(90 - s_pol_plunge))
    c_z = math.cos(math.radians(90 - c_pol_plunge))
    
    thetaRads = math.acos(s_x*c_x+s_y*c_y+s_z*c_z)
    if thetaRads < 0:
        thetaRads *= -1
    thetaDegs = thetaRads * 180 / math.pi
    
    
    # Vector A
    # 3D cross product
    a_x =  (s_y * c_z - s_z * c_y) / math.sin(thetaRads)
    a_y = -(s_x * c_z - s_z * c_x) / math.sin(thetaRads)
    a_z =  (s_x * c_y - s_y * c_x) / math.sin(thetaRads)
    
    
    #thetaAC = math.acos(a_x * c_x + a_y * c_y + a_z + c_z) # angle in radians
    #if thetaAC < 0:
    #    thetaAC *= -1
    
    # those calculations above don't work. The excel sheet always shows 1.571
    # for thetaAC / Theta A/C rad.s. So I have just set it that 1.571
    thetaAC = 1.571
    thetaACdegs = thetaAC * 180 / math.pi
    
    # Lower hemisphere
    if a_z < 0:
        a_xLH = -a_x
    else:
        a_xLH = a_x
    
    if a_z < 0:
        a_yLH = -a_y
    else:
        a_yLH = a_y
    
    if a_z < 0:
        a_zLH = -a_z
    else:
        a_zLH = a_z
    
    
    # Vector B - Slip direction
    # 3D cross-prouct
    b_x =  (c_y * a_z - c_z * a_y) / math.sin(thetaAC)
    b_y = -(c_x * a_z - c_z * a_x) / math.sin(thetaAC)
    b_z =  (c_x * a_y - c_y * a_x) / math.sin(thetaAC)
    
    # Lower hemisphere
    if b_z < 0:
        b_xLH = -b_x
    else:
        b_xLH = b_x
    
    if b_z < 0:
        b_yLH = -b_y
    else:
        b_yLH = b_y
    
    if b_z < 0:
        b_zLH = -b_z
    else:
        b_zLH = b_z
    
    # Slip direction
    if b_xLH < 0 and b_yLH >= 0:
        azimuth = 450 - math.degrees(math.atan2(b_yLH, b_xLH))
    else:
        azimuth = 90 - math.degrees(math.atan2(b_yLH, b_xLH))
    azimuth = round(azimuth)
    
    # Plunge
    plunge = 90 - math.degrees(math.acos(b_zLH))
    plunge = round(plunge)

    final_product = [str(objectID), int(c_strike), int(c_dip), int(s_strike), int(s_dip), str(quad), int(azimuth), int(plunge)]
    return final_product

    
def getData():

    try:
        if args.dataIn != None:
            data = args.dataIn
        else:
            print("\nIf this python file is in the the same folder as the .csv you wish to \n\
to convert, enter just the file name as extension.")
            print("\nIf the file is in a different folder than this python file, enter \n\
the enter path including the file name and extension.")
            print("\nThe output file will be placed where ever this python file is located.\n")
            data = input("Enter file name or path: ")
        if sys.platform == 'win32':
            data = os.getcwd() + '\\' + data
        elif sys.platform == 'linux':
            data = os.getcwd() + '/' + data
        print("Location of the input file: ")
        print(data)
        
    except FileNotFoundError:
        if sys.platform == 'win32':
            winsound.MessageBeep()
        elif sys.platform == 'linux':
            duration = 1 # seconds
            freq = 440 # hertz
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
        print("File not found. {} is not a valid file or path. \nCheck spelling or file path\n".format(data))
    	
        
        # reprompt the user to put in useable data
        data = input("\nEnter file name or path: ")
        if sys.platform == 'win32':
            data = os.getcwd() + '\\' + data
        elif sys.platform == 'linux':
            data = os.getcwd() + '/' + data
        print(data)
    
    dataFile =  open(data, 'r')
    strikesAndDips = []

    dataFile.readline()
    for line in dataFile:
        strikesAndDips.append(line) # add [] around the variable to be added to the list to make each line a list itself
        
    dataFile.close()
    return strikesAndDips


def calculateSlips(data):
    
    slipsList = []
    for line in data:
        line = line.split(',')
        objectID, C_Strike, C_Dip, S_Strike, S_Dip, quad = line
        
        # Convert all of the items to integers
        objectID = str(objectID)
        C_Strike = float(C_Strike)
        C_Dip = float(C_Dip)
        S_Strike = float(S_Strike)
        S_Dip = float(S_Dip)
        quad = str(quad).strip()
        
        # populated the slipList by calling slipLine for each line!
        slipsList.append(slipLine(objectID, C_Strike, C_Dip, S_Strike, S_Dip, quad))

    return slipsList
    
   
def toCSV(dataOut):
    
    if args.dataOut != None:
        outputPath = args.dataOut
    else:
        outputPath = input("Enter output file name or path: ")

    # Determine which OS they are using, and adjust file path accordingly
    if sys.platform == 'win32':
        outputPath = os.getcwd() + '\\' + outputPath
        print("Your data was written to: ")
        print(outputPath)
        
    elif sys.platform == 'linux':
        outputPath = os.getcwd() + '/' + outputPath
        print("\nYour data was written to: ")
        print(outputPath)
    
    try:
        outputFile = open(outputPath, 'w', newline = '')
    except PermissionError:
        print("{} is open. Please close it and try again.".format(outputPath))
        time.sleep(10)
        sys.exit()
    
    # Set up a csv writer object, comma delimited, and terminate the lines with a newline
    writer = csv.writer(outputFile, delimiter = ',', lineterminator='\n')
    
    # Add a header
    writer.writerow(['ID', 'C_strike', 'C_Dip', 'S_Strike', 'S_Dip', 'QUAD', 'Slip_azimuth', 'Slip_plunge'])
    
    # Write all the rows in the dataFile/list into a new csv file
    writer.writerows(dataOut)
        
    # Close the file
    outputFile.close()
    
    return outputPath


def createFigures(outputPath):
    '''Creates stereograms of the original S and C fabric with the slip line plotted as well.'''

    if args.dataOut != None:
        slipLines = open(args.dataOut, 'r')
    else:
        slipLines = open(outputPath, 'r')
    
    # remove the header first!
    slipLines.readline()
    
    current = os.getcwd()
    
    if sys.platform == 'win32':
        newFolder = '\\stereograms'
        newDir = current + newFolder
    elif sys.platform == 'linux':
        newFolder = '/stereograms'
        newDir = current + newFolder
    
    try:
        os.mkdir(newDir, mode=0o777)
    except FileExistsError:
        pass
    
    os.chdir(newDir)
    
    # Warning this could be rough...
    print("\nPlease wait. This may take a minute...")
    start = time.clock()
    # read through the file, split the lines, and assign variables
    for line in slipLines:
        line = line.split(',')
        objectID, C_Strike, C_Dip, S_Strike, S_Dip, quad, SL_azimuth, SL_plunge = line
        
        # Convert all of the items to integers
        objectID = str(objectID)
        C_Strike = int(C_Strike)
        C_Dip = int(C_Dip)
        S_Strike = int(S_Strike)
        S_Dip = int(S_Dip)
        quad = str(quad)
        SL_azimuth = int(SL_azimuth)
        SL_plunge = int(SL_plunge)
        
        # Make the stereograms
        plt.title('{}'.format(objectID))
        fig = plt.figure(figsize = (8, 8))
        ax = fig.add_subplot(111, projection = 'stereonet', title = "{}".format(objectID))
        ax.plane(C_Strike, C_Dip, c = 'b', label = 'C-Plane %03d/%02d' % (C_Strike, C_Dip))
        ax.plane(S_Strike, S_Dip, c = 'r', label = 'S-Plane %03d/%02d' % (S_Strike, S_Dip))
        ax.line(SL_azimuth, SL_plunge, c = 'k', label = 'Slip line %03d/%02d' % (SL_azimuth, SL_plunge))
        ax.legend()
        plt.savefig("{}.png".format(objectID), format = 'png', dpi = 300)
        
    slipLines.close()
    if sys.platform == 'win32':
        winsound.MessageBeep()
    print("Completed in {:.3f} seconds".format(time.clock() - start))
    
    
def main():
    print("Slip Line Calculator version 0.5")
    print("Written by Ben Weinmann")
    print("Original Excel by John Whitmore")
    print("Maths derived from SCslip by David Allison")
    print("It can be found at: http://www.usouthal.edu/geography/allison/GY403/StructureSpreadsheets.html\n")
    
    # save original data for a list variable
    inputData = getData()
        
    # assign calculated data from original to list variable
    slipLines = calculateSlips(inputData)
    print(slipLines)
    
    # pass calculated data to be written to csv
    outputPath = toCSV(slipLines)
    
    createFigures(outputPath)
		
main()    
