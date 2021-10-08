DROP TABLE IF EXISTS "inasra";
CREATE TABLE "inasra" ("id" integer NOT NULL,"name" TEXT, "width" INTEGER NOT NULL, "height" INTEGER NOT NULL, PRIMARY KEY (id));

DROP TABLE IF EXISTS "inasra_words";
CREATE TABLE "inasra_words" ("id" integer NOT NULL,"word_id" TEXT NOT NULL,"direction" text NOT NULL,"x" integer NOT NULL,"y" integer NOT NULL,"inasra_id" integer NOT NULL,"word_order" integer NOT NULL, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id), FOREIGN KEY(inasra_id) REFERENCES inasra(inasra_id));

DROP TABLE IF EXISTS "word";
CREATE TABLE "word" ("id" integer NOT NULL,"word" TEXT,"url" TEXT,"summary" TEXT,"content" TEXT, PRIMARY KEY (id));

DROP TABLE IF EXISTS "word_images";
CREATE TABLE "word_images" ("id" integer NOT NULL,"word_id" integer NOT NULL,"image_url" TEXT NOT NULL, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id));

DROP TABLE IF EXISTS "word_links";
CREATE TABLE "word_links" ("id" integer NOT NULL,"word_id" integer,"link" text, PRIMARY KEY (id), FOREIGN KEY(word_id) REFERENCES words(word_id));
