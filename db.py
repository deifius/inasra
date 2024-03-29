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

def get_spine_for_inasra(inasraid: int):
	we_are_spines = db_query('''
		SELECT isp.dimension, isp.choice_pos, w.word, pw.word as prev_word
		FROM inasra_spine isp
		INNER JOIN word w ON w.id = isp.word_id
		LEFT JOIN word pw ON pw.id = isp.prev_word_id
		WHERE isp.inasra_id = ?
	''', inasraid)
	if len(we_are_spines) > 0:
		return we_are_spines[0]
	else:
		return None

def get_word_links(word: str, should_sort: bool = False):
	order_by = ''
	if should_sort: order_by = 'ORDER BY wl.link ASC'
	return list(map(lambda word_link : word_link['link'], db_query(f'''
		SELECT wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE w.word LIKE ?
		{order_by}
		''', word)))

def get_multiwords_links(words: list, should_sort: bool = False): # there was a list[str] typehint that didnt seem pythonesque
	order_by = ''
	if should_sort: order_by = 'ORDER BY wl.link ASC'
	placeholder = ['w.word LIKE ?']
	placeholders = ' OR '.join(placeholder * len(words))
	sql = f'''
		SELECT wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE {placeholders}
		{order_by}
	'''
	results = db_query(sql, *words)
	return list(map(lambda word_link : word_link['link'], results))

def get_word_images(word: str):
	return list(map(lambda word_image : word_image['image_url'], db_query('''
		SELECT wi.image_url
		FROM word_images wi
		INNER JOIN word w ON wi.word_id = w.id
		WHERE w.word = (?)
		''', word)))

def get_word(word: str):
	return db_query_one('''
		SELECT *
		FROM word
		WHERE word LIKE ?
	''', word)

def get_last_inasra_word(inasraid: int):
	last_inasra_word = db_query('''
		SELECT iw.id, iw.direction, iw.x, iw.y, w.word, w.url, w.summary, w.content
		FROM inasra_words iw
		LEFT JOIN word w ON w.id = iw.word_id
		WHERE iw.inasra_id = ?
		ORDER BY id DESC
	''', inasraid)
	if len(last_inasra_word) > 0:
		return last_inasra_word[0]
	else:
		return None

def get_word_value(word: str, key: str):
	word_obj = get_word(word)
	if word_obj:
		return word_obj[key]
	else:
		return None

def get_latest_spine_coords(inasraid):
	lastest_word_id = db_query_value("SELECT MAX(id) FROM inasra_spine WHERE inasra_id = ?", [inasraid])
	current_dimension = db_query_value("SELECT dimension FROM inasra_spine WHERE id = ?", [lastest_word_id])
	sumx = db_query_value("SELECT SUM(choice_pos) FROM inasra_spine WHERE inasra_id = ? AND dimension = 'x' AND id != ?", [inasraid, lastest_word_id])
	sumy = db_query_value("SELECT SUM(choice_pos) FROM inasra_spine WHERE inasra_id = ? AND dimension = 'y' AND id != ?", [inasraid, lastest_word_id])
	return current_dimension, y, x

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

	spineid = db_insert("inasra_spine",
		inasra_id = inasra_id,
		word_id = word_id,
		dimension = dimension,
		choice_pos = choice_pos,
		prev_word_id = prev_word_id
	)
	return spineid

def add_one_inasra_word_please(inasra_id: int, word: str, direction: str, y: int, x: int, *args):
	word_id = get_word_value(word, "id")
	if word_id:
		inasra_word_id = db_insert("inasra_words",
			inasra_id = inasra_id,
			word_id = word_id,
			direction = ('x' if direction == 'vert' else 'y'),
			x = x,
			y = y
		)
		return inasra_word_id
	else:
		return None

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
			# db_insert(inasra.dumps()) ###########TODO
		except TypeError as err:
			print(f'failed: {err}')
			result = -1
		return result
	return print_pre_state
