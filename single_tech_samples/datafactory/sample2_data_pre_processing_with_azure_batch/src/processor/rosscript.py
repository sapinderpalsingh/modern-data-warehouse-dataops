'''
This script saves each topic in a bagfile as a csv.
Accepts inputfilename with full path and output folder path.
'''
import rosbag
import sys
import csv
import time
import string
import os  # for file management make directory
import shutil  # for file management, copy file
import argparse
import subprocess


def extractbagintocsv(cargs):
    listOfBagFiles = [args.rawPath]
    bagNamePath = '/' + \
        args.rawPath.split(
            '/')[len(args.rawPath.split('/'))-1].split('.bag')[0]
    numberOfFiles = "1"
    count = 0
    for bagFile in listOfBagFiles:
        count += 1
        print("Reading file " + str(count) +
              " of  " + numberOfFiles + ": " + bagFile)

        # access bag
        bag = rosbag.Bag(bagFile)
        bagContents = bag.read_messages()
        bagName = bag.filename

        try:
            if os.path.exists(args.extractedPath + bagNamePath):
                continue
            else:
                os.mkdir(args.extractedPath + bagNamePath)
        except Exception as e:
            raise RuntimeError(f"Error: {e.__class__()}")
            

        folder = args.extractedPath + bagNamePath

        # get list of topics from the bag
        listOfTopics = []
        for topic, msg, t in bagContents:
            if topic not in listOfTopics:
                listOfTopics.append(topic)

        for topicName in listOfTopics:
            # Create a new CSV file for each topic
            filename = folder + '/' + \
                topicName.replace('/', '_slash_') + '.csv'
            with open(filename, 'w+') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')
                firstIteration = True  # allows header row
                # for each instant in time that has data for topicName
                for subtopic, msg, t in bag.read_messages(topicName):
                    # parse data from this instant, which is of the form of multiple lines of "Name: value\n"
                    # - put it in the form of a list of 2-element lists
                    msgString = str(msg)
                    msgList = msgString.split('\n')
                    instantaneousListOfData = []
                    for nameValuePair in msgList:
                        splitPair = nameValuePair.split(':')
                        for i in range(len(splitPair)):  # should be 0 to 1
                            splitPair[i] = splitPair[i].strip()
                        instantaneousListOfData.append(splitPair)
                    # write the first row from the first element of each pair
                    if firstIteration:  # header
                        headers = ["rosbagTimestamp"]  # first column header
                        for pair in instantaneousListOfData:
                            headers.append(pair[0])
                        filewriter.writerow(headers)
                        firstIteration = False
                    # write the value from each pair to the file
                    # first column will have rosbag timestamp
                    values = [str(t)]
                    for pair in instantaneousListOfData:
                        if len(pair) > 1:
                            values.append(pair[1])
                    filewriter.writerow(values)
        bag.close()
    print("Extraction Successful! \nDone extracting all topics into respectice csv files")


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--rawPath", "-rPath",
                            help="Set the file path for the raw bag file")
        parser.add_argument("--extractedPath", "-ePath",
                            help="Set the file path for the extracted file")
        args = parser.parse_args()
        extractbagintocsv(args)

    except Exception as e:
        raise RuntimeError(f"Error: {e.__class__}\n Error Extracting the Bag File!")

