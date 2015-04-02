CREATE TABLE words (
id INTEGER NOT NULL, 
word VARCHAR, 
document_id INTEGER, 
count INTEGER, 
PRIMARY KEY (id)
);

CREATE TABLE files (
id INTEGER NOT NULL, 
added_time DATETIME, 
path VARCHAR, 
inode INTEGER, 
shasum VARCHAR(64), 
has_duplicate BOOLEAN, 
title VARCHAR, 
author VARCHAR, 
comment VARCHAR, 
PRIMARY KEY (id), 
UNIQUE (path), 
CHECK (has_duplicate IN (0, 1))
);
