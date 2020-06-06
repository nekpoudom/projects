"""
This program finds the smallest number in a constantly increasing circular list.
Requirement: Make your program as extendible and flexible as possible.
The only difference between this program and minCircList2.py is the lists are input
via a text file.

Author:  Nse Ekpoudom
Created:  July 11, 2018
"""


def getMinVal(circularList, listLength):
    """
    This function takes a sorted circular list (circularList) of length (listLength)
    It implements the binary search algorithm for a performance of O(log(N)).
    Precondition:  circularList is a list of integers of length 1 or greater
    Postcodition: The minimum value in the list is return.
    """

    #there is only 1 item in the list return the value (base case)
    if listLength == 1:
        return circularList[0]

    #get the mid location of the list
    midIdx = int(listLength/2)

    #check to see if the middle value is the minimum value
    if midIdx >= 1 and circularList[midIdx] < circularList[midIdx - 1]:
        return circularList[midIdx]

    #check to see if the next value is the minimum value
    if midIdx < listLength-1 and circularList[midIdx + 1] < circularList[midIdx]:
        return circularList[midIdx + 1]

    #Recursively select which half of the list to search further
    #search left half of the list
    if circularList[listLength - 1] > circularList[midIdx-1]:
        return getMinVal(circularList[0:midIdx], len(circularList[0:midIdx]))

    #search right half of the list
    else:
        return getMinVal(circularList[midIdx+1:], len(circularList[midIdx+1:]))
    

#Main program to test the function with different lists from an input file

#open input and output files

infile = open('listInput.txt','r')
outfile = open('minVals.txt','w')

# find the minimum value in the lists
for line in infile:
    lst = list(map(int,(line).split(',')))   #convert the string to a list of integers
    #get the minimum value and write it to an output file
    outfile.write(str(getMinVal(lst, len(lst))) +'\n') 

infile.close()
outfile.close()
    

