import mysql.connector
from mysql.connector import errorcode

# i would have liked to connect to the database through a config file but due to lack of time
# i hardcoded the connection to the database in my code itself. i have starred out the connection information
# for security purposes
cnn = mysql.connector.connect(
	user = '*****', password = '*****', host = '*****', database = '*****'
)
cursor = cnn.cursor()

#reads the given PovertyAllocation csv file
with open('LAPHiPovAllocation2019-20.csv', 'r', encoding='utf-8-sig') as proj:
	file = proj.readlines()

infos = []
indexList = []
id = 0

#iterative loop for every row in file. Its purpose is to handle each line/row in the file seperately as a list.
for row in file:
	row = row.replace('\n', '')
	row = row.replace('%', '')
	quotedSubstring = ""
	index = 0
	newRow = ""
	lastIndex = ""

	#tries to go through each token in the row and modifies the current row in the file such that the format is acceptable for the insert statement
	try:
		for x in row:
			index = row.index(x)
			lastIndex = x
			if x == '"': #records index of double quotations, creates substring of row without double quotation mark
				print(index)
				indexList.append(index)
				row = row[0:index] + row[index + 1:len(row)]

				if len(indexList) == 2: #when the list of indexes of double quotations is > 2, a new substring is formed with the indexes and modified to
										#exclude extra commas
					quotedSubstring = row[indexList[0]:indexList[1]]
					quotedSubstring = quotedSubstring.replace(',', '')

					newRow = row[:indexList[0]] + quotedSubstring + "," + row[indexList[1] + 1:len(row)]
					row = newRow
					print(newRow)
					indexList = []
				else:
					pass
	except ValueError: #exception happens on errors when attributed value is incorrect
		pass

	#splits row and records values as a list separated by commas
	infos = row.split(',')

	# ALL DATATYPES EXCEPT INTEGERS AND FLOATS HAVE TO BE INSERTED AS STRINGS IN EXECUTE STATEMENT

	# the variables of the values from the row that are being accessed from a list
	id = id + 1
	districtCode = "'" + infos[0] + "'"
	districtName = "'" + str(infos[1]).strip() + "'"
	schoolCode = "'" + infos[2] + "'"
	schoolName = "'" + str(infos[3]).strip() + "'"
	povertyPercent = "'" + infos[12] + "'"


	#execute statements
	query2 = 'INSERT INTO PovertyAllocation (AllocationID, DistrictCode, DistrictName, SchoolCode, SchoolName, PovertyPercentage)' +\
			'VALUES (%s, %s, %s, %s, %s, %s)' % (id, districtCode, districtName, schoolCode, schoolName, povertyPercent)

	try:
		cursor.execute(query2)
		print('Inserted', cursor.rowcount, 'row(s) of data.')
		cnn.commit()
	except mysql.connector.Error as e: # bad data is outputted to a separate file
		file = open("povertyAllocation.txt", "a")
		error = str(query2)
		file.write(error + "\n")

cursor.close()
cnn.close()