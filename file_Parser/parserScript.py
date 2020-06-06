#!/usr/bin/python

#  Large File Parser
#  Written by Nse Ekpoudom
#  October 25, 2019

import pandas as pd
import csv
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def amount_sign(typeCol,amt):
# 
# 	Returns a numeric value for the amount: negative value for debits
# 
	if 'debit' in typeCol:
		return float(amt) * -1
	else:
		return float(amt)     

def getDateandType(line):

	
	index = 0
	found = False
	while not found and index < len(line):
		if line[index]=='credit' or line[index]=='debit':
			found =True
		else:
			index += 1
	dateItem = line[index-1]
	typeItem = line[index]

	return dateItem, typeItem

def readFile(filename):
#
# returns a list of data containing user_id, amount, date, type
# read from a csv file, filename,  that is pipe delimited. Pipes can be embedded in the string
# commented out code debug statements

	f = open(filename, "r")


	outList = list()
	count = 0
	for line in f:
		lst = line.split("|")
		#if the length is 7, no embedded bars otherwise parse for embedded bars
		if len(lst) > 7:  #process to extract the right data
			count = count + 1
			#print(lst)
			#print(getDateandType(lst[3:]))

			#print([lst[0], lst[2],getDateandType(lst[3:])[0],getDateandType(lst[3:])[1]])
			#print(getDateandType(lst[3:]))

			outList.append([lst[0], lst[2],getDateandType(lst[3:])[0],getDateandType(lst[3:])[1]])
			
			
		else:
			outList.append([lst[0], lst[2], lst[4], lst[5]])
			count = count + 1
	
	#output record count of good and complicated records
	#print("number of follow up lines: " + str(count))
	#print("Lines of good data: " + str(len(outList)))
	return outList

def outputData(dataRecs, outFile):
#
# Takes data from dataRecs aggregates and outputs the data to a csv file: outFile
#
	labels = ['user_id', 'amount', 'date', 'type']
	df = pd.DataFrame.from_records(dataRecs, columns=labels)
	df = df.drop(df.index[0])

	#convert amount to numeric with proper sign depending on type (debit or credit)
	df['new_amount'] = df.apply(lambda x: amount_sign(x['type'],x['amount']),axis=1)


	df_sum = df.groupby(['user_id']).sum().new_amount


	df_count= df.groupby(['user_id']).count().date
	df_min = df.groupby(['user_id']).min().new_amount
	df_max = df.groupby(['user_id']).max().new_amount

	df_output = pd.concat([df_count,df_sum, df_min, df_max], axis=1)


	#append to file with header
	f =open(outFile, 'a')
	df_output.to_csv(f, header=False)
	

if __name__ == "__main__":
    #TODO remove hardcoded file references
	dataLst = readFile('transactions2.csv')
	#print(dataLst)

	#write header to output file to be passed to get data
	labels = [['user_id', 'n', 'sum', 'min', 'max']]
	with open('transactions3_Output.csv', 'w') as outputF:
		fileWriter = csv.writer(outputF)
		fileWriter.writerows(labels)
	outputF.close()
	
	outputData(dataLst,'transactions3_Output.csv')
	
