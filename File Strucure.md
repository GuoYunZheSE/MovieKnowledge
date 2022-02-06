# File Strucure

## Protege

This file contains the `OWL` file for our project, it contains the entity, property and relationship defined.

![image-20220206172403601](/Users/lucas/Library/Application Support/typora-user-images/image-20220206172403601.png)

## BackEnd

### script

This directory contains the scripts and config for uwsgi.

#### Crawler.py

This file will craw the actor/movie information from **[the movie db(TMDB)](https://www.themoviedb.org/)** and insert into local database.

![image-20220206173917150](/Users/lucas/Library/Application Support/typora-user-images/image-20220206173917150.png)

### Data

#### MovieSQLData

This directory contains the SQL Insert data which is crawled by our `crawler.py`.

#### MovieKnowledge_*.json

This two json files contain the person name and movie name, they are used to train a **Entity Classifier** by  `spacy`. 

### BackEnd

This directory contains the `django` framework we used, and the view and controller file.