"""Slip line calculator to calculate the slip between S and C fabrics"""
import math, os, sys, csv, argparse, time
import numpy as np
import matplotlib.pyplot as plt
if sys.platform == 'win32':
    import winsound
    
if sys.platform == 'darwin' or sys.platform == 'os2' or sys.platform == 'os2emx':
    print("Incompatible operating system. Consider true Unix or Windows variants.")
    time.sleep(10)
    sys.exit()

try:
    import seaborn as sb
    import mplstereonet
except ImportError:
    print("Installing missing modules, please wait...\n")
    if sys.platform == 'linux':
        os.system('pip3 install seaborn')
    else:
        os.system('pip3 install seaborn')
    
    if sys.platform == 'linux':
        os.system('pip3 install mplstereonet')
    else:
        os.system('pip3 install mplstereonet')
    
    if sys.platform == 'linux':
        os.system('sudo apt install speech-dispatcher')
    
# grab argument input from the user
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dataIn', help="Enter the name of the file, or the path to the file plus the file name")
parser.add_argument('-o','--dataOut', help="Enter the name of the file you want to be written to or the path plus the file name")
args = parser.parse_args()


def slipLine(objectID, S_strike, S_dip, C_strike, C_dip):

    # Step 1
    Cpol_az = 270 + S_strike
    Cpol_pl = -1 * (S_dip - 90)
    Spol_az = 270 + C_strike
    Spol_pl = -1 * (C_dip - 90)


    # Step 2
    C_cosAplha = math.sin(math.radians(Cpol_az)) * math.sin(math.radians(90-Cpol_pl))
    C_cosBeta = math.cos(math.radians(Cpol_az)) * math.sin(math.radians(90-Cpol_pl))
    C_cosGamma = math.cos(math.radians(90-Cpol_pl))


    # Step 3
    S_cosAplha = math.sin(math.radians(Spol_az)) * math.sin(math.radians(90-Spol_pl))
    S_cosBeta = math.cos(math.radians(Spol_az)) * math.sin(math.radians(90-Spol_pl))
    S_cosGamma = math.cos(math.radians(90-Spol_pl))


    # Step 4
    thetaRads = math.acos(C_cosAplha*S_cosAplha+C_cosBeta*S_cosBeta+C_cosGamma*S_cosGamma)
    thetaDegs = math.degrees(thetaRads)
    

    # Step 5
    if thetaRads != 0:
        intCosAlpha3d = (C_cosBeta * S_cosGamma - C_cosGamma * S_cosBeta) / math.sin(thetaRads)
    else:
        intCosAlpha3d = 0

    if thetaRads != 0:
        intCosBeta3d = -(C_cosAplha * S_cosGamma - C_cosGamma * S_cosAplha) / math.sin(thetaRads)
    else:
        intCosBeta3d = 0

    if thetaRads != 0:
        intCosGamma3d = (C_cosAplha * S_cosBeta - C_cosBeta * S_cosAplha) / math.sin(thetaRads)
    else:
        intCosGamma3d = 0
        

    # Step 6 ###LH = is opposite sign of intCosGamma3d
    if intCosGamma3d < 0:
        intCosAlphaLH = -intCosAlpha3d
    else:
        intCosAlphaLH = intCosAlpha3d

    if intCosGamma3d < 0:
        intCosBetaLH = -intCosBeta3d
    else:
        intCosBetaLH = intCosBeta3d

    if intCosGamma3d < 0:
        intCosGammaLH = -intCosGamma3d
    else:
        intCosGammaLH = intCosGamma3d
    

    # Step 7A - C Plane(?)
    # azimuth
    if intCosAlphaLH == 0 and intCosBetaLH == 0:
        azimuth1 = 0
    elif intCosAlphaLH < 0 and intCosBetaLH >= 0:
        azimuth1 = 450 - math.degrees(math.atan2(intCosBetaLH, intCosAlphaLH))
    else:
        azimuth1 = 90 - math.degrees(math.atan2(intCosBetaLH, intCosAlphaLH))

    # plunge
    #plunge1 = 90 - math.degrees(math.acos(intCosGammaLH)) # this never works, and never gets used, so...
		

    # Step 7B - s plane(?)
    # azimuth 
    azimuth2 = math.acos(intCosAlpha3d * S_cosAplha + intCosBeta3d * S_cosBeta + intCosGamma3d * S_cosGamma)
    plunge2 = azimuth2 * 180 / math.pi


    # Step 8
    cosAlpha3d = (S_cosBeta * intCosGamma3d - S_cosGamma * intCosBeta3d) / math.sin(azimuth2)
    cosBeta3d = -(S_cosAplha * intCosGamma3d - S_cosGamma * intCosAlpha3d) / math.sin(azimuth2)
    cosGamma3d = (S_cosAplha * intCosBeta3d - S_cosBeta * intCosAlpha3d)/ math.sin(azimuth2)
    

    # Step 9 - reverse signs
    if cosGamma3d < 0:
        cosAlphaLH = -cosAlpha3d
    else:
        cosAlphaLH = cosAlpha3d

    if cosGamma3d <0:
        cosBetaLH = -cosBeta3d
    else:
        cosBetaLH = cosBeta3d

    if cosGamma3d <0:
        cosGammaLH = -cosGamma3d
    else:
        cosGammaLH = cosGamma3d


    # Step 10 - finally
    # final azimuth
    if cosAlphaLH < 0 and cosBetaLH >= 0:
        azimuth_final = 450-math.degrees(math.atan2(cosBetaLH, cosAlphaLH))
    else:
        azimuth_final = 90 - math.degrees(math.atan2(cosBetaLH, cosAlphaLH))

    #if azimuth_final > 360:
     #   azimuth_final -= 360

    plunge_final = 90 - math.degrees(math.acos(cosGammaLH))
    
    azimuth_final = round(azimuth_final)
    if azimuth_final > 180:
        azimuth_final = azimuth_final - 180
    plunge_final = round(plunge_final)

    final_product = [str(objectID), int(S_strike), int(S_dip), int(C_strike), int(C_dip), int(azimuth_final), int(plunge_final)]
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
        objectID, C_Strike, C_Dip, S_Strike, S_Dip = line
        
        # Convert all of the items to integers
        objectID = str(objectID)
        C_Strike = int(C_Strike)
        C_Dip = int(C_Dip)
        S_Strike = int(S_Strike)
        S_Dip = int(S_Dip)
        
        # populated the slipList by calling slipLine for each line!
        slipsList.append(slipLine(objectID, S_Strike, S_Dip, C_Strike, C_Dip))

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
    outputFile = open(outputPath, 'w', newline = '')
    
    # Set up a csv writer object, comma delimited, and terminate the lines with a newline
    writer = csv.writer(outputFile, delimiter = ',', lineterminator='\n')
    
    # Add a header
    writer.writerow(['ID', 'C_strike', 'C_Dip', 'S_Strike', 'S_Dip', 'SL_azimuth', 'SL_plunge'])
    
    # Write all the rows in the dataFile/list into a new csv file
    writer.writerows(dataOut)
        
    # Close the file
    outputFile.close()


def createFigures():
    '''Creates stereograms of the original S and C fabric with the slip line plotted as well.'''

    slipLines = open(args.dataOut, 'r')
    
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
        objectID, C_Strike, C_Dip, S_Strike, S_Dip, SL_azimuth, SL_plunge = line
        
        # Convert all of the items to integers
        objectID = str(objectID)
        C_Strike = int(C_Strike)
        C_Dip = int(C_Dip)
        S_Strike = int(S_Strike)
        S_Dip = int(S_Dip)
        SL_azimuth = int(SL_azimuth)
        if SL_azimuth > 180:
            SL_azimuth = SL_azimuth - 180
        SL_plunge = int(SL_plunge)
        
        # Make the stereograms
        sb.set()
        plt.xkcd()
        plt.title('{}'.format(objectID))
        fig = plt.figure(figsize = (8, 8))
        ax = fig.add_subplot(111, projection = 'stereonet', title = "{}".format(objectID))
        ax.plane(C_Strike, C_Dip, c = 'b', label = 'C-Plane %03d/%02d' % (C_Strike, C_Dip))
        ax.plane(S_Strike, S_Dip, c = 'r', label = 'S-Plane %03d/%02d' % (S_Strike, S_Dip))
        ax.plane(SL_azimuth, SL_plunge, c = 'k', label = 'Slip line %03d/%02d' % (SL_azimuth, SL_plunge))
        ax.legend()
        plt.savefig("{}.png".format(objectID), format = 'png', dpi = 300)
        
    slipLines.close()
    if sys.platform == 'linux':
        os.system('spd-say "Thank you for using Slip Line Calculator version 0.3"')
    print("Completed in {:.3f} seconds".format(time.clock() - start))
    
    
def main():
    # the weirdest intro screen...
    #if sys.platform == 'linux':
        #os.system('spd-say "Welcome to Slip Line Calculator"')
    print("Slip Line Calculator version 0.3")
    print("Written by Ben Weinmann")
    print("Original Excel by John Whitmore")
    print("Maths derived from http://www.usouthal.edu/geography/allison/GY403/StructureSpreadsheets.html\n")
    
    # save original data for a list variable
    inputData = getData()
    
    # assign calculated data from original to list variable
    slipLines = calculateSlips(inputData)
    
    # pass calculated data to be written to csv
    toCSV(slipLines)
    
    createFigures()
		
main()    
