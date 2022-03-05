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

def get_word_links(word: str):
	return db_query('''
		SELECT wl.id, wl.word_id, wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE w.word = ?
		''', word)

def get_word(word: str):
	return db_query('''
		SELECT *
		FROM word
		WHERE word = ?
	''', word)

def get_word_value(word: str, key: str):
	word_rows = get_word(word)
	if len(word_rows) > 0:
		return word_rows[0][key]
	else:
		return None

def get_word_summary(word: str):
	return get_word_value(word, "summary")

def get_word_content(word: str):
	return get_word_value(word, "content")

# def db_query_one(query, *values):
# 	return db_query(query, values)
