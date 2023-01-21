DROP TABLE IF EXISTS "inasra";
CREATE TABLE "inasra" ("id" integer NOT NULL,"name" TEXT, PRIMARY KEY (id));

DROP TABLE IF EXISTS "inasra_words";
CREATE TABLE "inasra_words" ("id" integer NOT NULL,"inasra_id" integer NOT NULL,"word_id" integer NOT NULL,"direction" text NOT NULL,"x" integer NOT NULL,"y" integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id), FOREIGN KEY(inasra_id) REFERENCES inasra(inasra_id));

DROP TABLE IF EXISTS "inasra_spine";
CREATE TABLE "inasra_spine" ("id" integer NOT NULL, "inasra_id" integer NOT NULL, "word_id" integer NOT NULL,"dimension" text NOT NULL, "choice_pos" integer NOT NULL, "prev_word_id" integer, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id), FOREIGN KEY(inasra_id) REFERENCES inasra(inasra_id), FOREIGN KEY(prev_word_id) REFERENCES inasra_spine(id));

DROP TABLE IF EXISTS "word";
CREATE TABLE "word" ("id" integer NOT NULL,"word" TEXT,"url" TEXT,"summary" TEXT,"content" TEXT, PRIMARY KEY (id));

DROP TABLE IF EXISTS "word_images";
CREATE TABLE "word_images" ("id" integer NOT NULL,"word_id" integer NOT NULL,"image_url" TEXT NOT NULL, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id));

DROP TABLE IF EXISTS "word_links";
CREATE TABLE "word_links" ("id" integer NOT NULL,"word_id" integer,"link" text, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id));
