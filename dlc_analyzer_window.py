###########################################################
# AUTHOR  : Chase Dudas
# CREATED : 11/15/2019
# Title   : dlc_analyzer_window.py
# COMMENT : 
# Need    : 
###########################################################
import csv
import math
import os
import pandas as pd
###########################################################
# HELPER FUNCTIONS
###########################################################

# Takes in a threshold value and a string reference to a desired csv file to open. 
# Opens the csv file, checking the extension just in case.
# Transfers the data fromn a csv file to a Data Frame
# Computes the covaration of movement if the two values are above the threshold.
# Stored and returned in a list of values
def analyze_csv_file(threshold, csvFile):
    # Check made for correct file extemsion 
    root, ext = os.path.splitext(csvFile)
    if ext != '.csv':
        # Not passed a .csv file
        print('Not a suitable .csv file. The file recieved was: %s' % csvFile)
        return None
    # Prints if was given a .csv file 
    print('Pulling data from %s' % csvFile)
    
    # import csv file using pandas
    df = pd.read_csv(csvFile, skiprows= 1)
    r, c = df.shape
    magnitude_list = []
    time_list = []

    # Traverse the data frame and preform calculations on the data. 
    for ind in range(1, r-1):
        # Checks if likelihood is higher than the set threshold
        if float(df.at[ind + 1, 'Vole1_RightEye.2']) < threshold or float(df.at[ind, 'Vole1_RightEye.2']) < threshold:
            # Point was not above likeliness threshold, leave blank 
            magnitude_list.append(None)
        else:
            # Both points are above the likeliness threshold 
            # Vector distance Vole 1
            magnitude_vector_vole1 = math.sqrt(math.pow(float(df.at[ind + 1, 'Vole1_RightEye']) - float(df.at[ind, 'Vole1_RightEye']),2) 
                                    + math.pow(float(df.at[ind + 1, 'Vole1_RightEye.1']) - float(df.at[ind, 'Vole1_RightEye.1']),2))
            # Vector distance Vole 2
            magnitude_vector_vole2 = math.sqrt(math.pow(float(df.at[ind + 1, 'Vole2_RightEye']) - float(df.at[ind, 'Vole2_RightEye']),2) 
                                    + math.pow(float(df.at[ind + 1, 'Vole2_RightEye.1']) - float(df.at[ind, 'Vole2_RightEye.1']),2))

            # Change in vector magnitude
            magnitude_vector = magnitude_vector_vole1 - magnitude_vector_vole2

            # Append to calculations list
            magnitude_list.append(magnitude_vector)

        # Append timestamps
        time_list.append(ind)

    return magnitude_list

# Takes in a list of covariation of movement values
# NOTE: Run a map to filter out values bigger than threshold 

def windowed_preview(threshold, movementList):
    for i, item in enumerate(movementList):
        if item == None:
            pass
        elif item <= threshold and item >= -threshold:
            print("%s\n" % item)

###########################################################
# MAIN FUNCTION
###########################################################
def main():
    movement_threshold = 0.5
    covariation_threshold = 20

    # Holds the user inputed file paths
    fileArgs = [r'C:\Users\Behavior Scoring\Desktop\DLC Project Utils\csv files\similar_motionDeepCut_resnet50_Normal_MotionAug14shuffle1_110000.csv']

    # Pass files as arguments to the function; Return data structure with analysis metrics
    analyzed_csv_data = analyze_csv_file(movement_threshold, fileArgs[0])

    # Show glimpses for windows under threshold
    windowed_preview(covariation_threshold, analyzed_csv_data)

if __name__ == "__main__":
    main()