import mysql.connector
from mysql.connector import errorcode


cnn = mysql.connector.connect(
	user = '*****', password = '*****', host = '*****', database = '*****'
)

cursor = cnn.cursor()

#reads the given ImprovementFunds csv file
with open('WSIF School Improvement Funds 2019-20 (002).csv', 'r', encoding='utf-8-sig') as proj:
	file = proj.readlines()


infos = []
indexList = []
id = 0
#iterative loop for every row in file. Its purpose is to handle each line/row in the file seperately as a list.
for row in file:
	row = row.replace('\n', '')
	row = row.replace('$', '')
	quotedSubstring = ""
	index = 0
	newRow = ""
	lastIndex = ""

	# tries to go through each token in the row and modifies the current row in the file such that the format is acceptable for the insert statement
	try:
		for x in row:
			index = row.index(x)
			lastIndex = x
			if x == '"': # records index of double quotations, creates substring of row without double quotation mark
				print(index)
				indexList.append(index)
				row = row[0:index] + row[index + 1:len(row)]

				if len(indexList) == 2: # when the list of indexes of double quotations is > 2, a new substring is formed with the indexes and modified to
										# exclude extra commas
					quotedSubstring = row[indexList[0]:indexList[1]]
					quotedSubstring = quotedSubstring.replace(',', '')

					newRow = row[:indexList[0]] + quotedSubstring + "," + row[indexList[1] + 1:len(row)]
					row = newRow
					print(newRow)
					indexList = []
				else:
					pass
	except ValueError: # exception happens on errors when attributed value is incorrect
		pass

	infos = row.split(',') # splits row and records values as a list separated by commas

	# ALL DATATYPES EXCEPT INTEGERS AND FLOATS HAVE TO BE INSERTED AS STRINGS IN EXECUTE STATEMENT

	# the variables of the values from the row that are being accessed from a list
	id = id + 1
	schoolYear = "'" + str(infos[0]).strip() + "'"
	organizationLevel = "'" + str(infos[1]).strip() + "'"
	county = "'" + str(infos[2]).strip() + "'"
	esdName = "'" + str(infos[3]).strip() + "'"
	esdOrganizationID = "'" + infos[4] + "'"
	districtCode = "'" + infos[5] + "'"
	districtName = "'" + str(infos[6]).strip() + "'"
	districtOrganizationID = "'" + infos[7] + "'"
	schoolCode = "'" + infos[8] + "'"
	schoolName = "'" + str(infos[9]).strip() + "'"
	schoolOrganizationID = "'" + infos[10] + "'"
	organizationID = "'" + infos[11] + "'"
	status = "'" + str(infos[12]).strip() + "'"
	awardAmount = "'" + infos[13] + "'"


	#execute statements
	query2 = 'INSERT INTO ImprovementFunds (FundID, SchoolYear, OrganizationLevel, County, ESDName, ESDOrganizationID, DistrictCode, DistrictName, DistrictOrganizationID, SchoolCode, SchoolName, SchoolOrganizationID, OrganizationID, AccountabilityStatus, ImprovementAward)' +\
			'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % (id, schoolYear, organizationLevel, county, esdName, esdOrganizationID, districtCode, districtName, districtOrganizationID, schoolCode, schoolName, schoolOrganizationID, organizationID, status, awardAmount)

	print(query2)
	cursor.execute(query2)
	print('Inserted', cursor.rowcount, 'row(s) of data.')
	cnn.commit()

cursor.close()
cnn.close()