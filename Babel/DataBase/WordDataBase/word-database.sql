CREATE TABLE languages (
id INTEGER NOT NULL, 
name INTEGER, 
PRIMARY KEY (id)
);

CREATE TABLE words (
id INTEGER NOT NULL, 
word VARCHAR, 
part_of_speech_tag_id INTEGER, 
count INTEGER, 
file_count INTEGER, 
rank INTEGER, 
PRIMARY KEY (id)
);

CREATE TABLE part_of_speech_tags (
id INTEGER NOT NULL, 
tag VARCHAR, 
comment VARCHAR, 
PRIMARY KEY (id)
);
