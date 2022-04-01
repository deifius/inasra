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
	return list(map(lambda word_link : word_link['link'], db_query('''
		SELECT wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE w.word = ?
		''', word)))

def get_word_images(word: str):
	return list(map(lambda word_image : word_image['image_url'], db_query('''
		SELECT wi.image_url
		FROM word_images wi
		INNER JOIN word w ON wi.word_id = w.id
		WHERE w.word = ?
		''', word)))

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

def logginDB(inasra):
	def print_pre_state(*args, **kwargs):
		print(f"my inasra is:{inasra}:{args}")
		inasra.history.append(args, kwargs)#########TODO
		try:
			result = inasra(*args, **kwargs)
			db.db_insert(inasra.dumps()) ###########TODO
		except TypeError as err:
			print(f'failed: {err}')
			result = -1
		return result
	return print_pre_state
