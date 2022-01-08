import sqlite3

def make_word_question_marks(wird):
	questionmarks = ''
	for e in wird: questionmarks = questionmarks + '?,'
	return questionmarks[0:-1]
def db_insert(table, **values):
	connection = sqlite3.connect('inasra.sqlite3')
	cursor = connection.cursor()
	vals = []
	for each in values.keys(): vals.append(values[each])
	masterstring = "INSERT INTO " + table + "(" + ','.join(values.keys()) + ") VALUES("+ make_word_question_marks(vals) + ");"
	# print(masterstring)
	# print(vals)
	cursor.execute(masterstring, vals)
	connection.commit()
	cursor.close()
	connection.close()
	# print(cursor.lastrowid)
	return cursor.lastrowid
def db_query(query, *values):
	connection = sqlite3.connect('inasra.sqlite3')
	cursor = connection.cursor()
	cursor.execute(query, values)
	results = cursor.fetchall()
	if results is None:
		return []
	final = []
	for row in results:
		thing = {}
		for idx, col in enumerate(cursor.description):
			thing[col[0]] = row[idx]
		final.append(thing)
	return final

# def db_query_one(query, *values):
# 	return db_query(query, values)
