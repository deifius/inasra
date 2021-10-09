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
	print(masterstring)
	cursor.execute(masterstring,vals)
	connection.commit()
	cursor.close()
	connection.close()
	return cursor.lastrowid
def db_query(query, *values):
	connection = sqlite3.connect('inasra.sqlite3')
	cursor = connection.cursor()
	cursor.execute(query, values)
	return cursor.fetchall()
