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
	#print(f"cursor lastrowid is {cursor.lastrowid} m'lord")
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
		WHERE word LIKE ?
	''', word)

def get_last_inasra_word(inasraid: int):
	last_inasra_word = db_query('''
		SELECT iw.id, iw.direction, iw.x, iw.y, iw.char_pos, w.word, w.url, w.summary, w.content
		FROM inasra_words iw
		LEFT JOIN word w ON w.id = iw.word_id
		WHERE iw.inasra_id = ?
		ORDER BY prev_word_id
	''', inasraid)
	if len(last_inasra_word) > 0:
		return last_inasra_word[0]
	else:
		return None

def get_word_value(word: str, key: str):
	word_rows = get_word(word)
	if len(word_rows) > 0:
		return word_rows[0][key]
	else:
		return None

def add_one_inasra_spine_please(inasra_id: int, word: str, choice_pos: int, *args):
	# word_id = db_query_value("id", "SELECT w.id FROM word w WHERE w.word = ?", word)
	word_id = get_word_value(word, "id")
	prev_word = db_query_one("SELECT s.* FROM inasra_spine s WHERE s.inasra_id = ? ORDER BY s.id DESC LIMIT 1", inasra_id)
	if word_id == None:
		print(f"yea, thy word {word} be inaccurate for thy inasra {inasra_id}")
		return None

	if len(args) == 1:
		dimension = args[0]
	else:
		try:
			if prev_word == None:
				dimension = "x"
			else:
				do_the_opposite = {
					"horiz": "vert",
					"vert": "horiz",
					"x": "y",
					"y": "x",
					"across": "down",
					"down": "across"
				}
				dimension = do_the_opposite[prev_word.dimension]
		except:
			print(f"we tried homie, but ya can't opposite {prev_word.dimension}")
			return None

	if prev_word == None:
		prev_word_id = None
	else:
		prev_word_id = prev_word.id

	spineid = db.db_insert("inasra_spine",
		inasra_id = inasra_id,
		word_id = word_id,
		dimension = dimension,
		choice_pos = choice_pos,
		prev_word_id = prev_word.id
	)
	return spineid

def get_word_summary(word: str):
	return get_word_value(word, "summary")

def get_word_content(word: str):
	return get_word_value(word, "content")

def db_query_value(key, query, *values):
	row = db_query_one(query, *values)
	if row == None:
		return None
	else:
		return row[key]

def db_query_one(query, *values):
	rows = db_query(query, *values)
	if len(rows) < 1:
		return None
	else:
		return rows[0]

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
