create table genre
(
    genre_id   int         not null
        primary key,
    genre_name varchar(45) null
)
    charset = latin1;

INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (12, 'Adventure');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (14, 'Fantasy');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (16, 'Animation');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (18, 'Drama');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (27, 'Horror');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (28, 'Action');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (35, 'Comedy');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (36, 'History');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (37, 'Western');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (53, 'Thriller');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (80, 'Crime');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (99, 'Documentary');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (878, 'Science Fiction');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (9648, 'Mystery');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (10402, 'Music');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (10749, 'Romance');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (10751, 'Family');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (10752, 'War');
INSERT INTO MovieKnowledge.genre (genre_id, genre_name) VALUES (10770, 'TV Movie');