SELECT title FROM movies
WHERE EXISTS
 (SELECT * FROM stars JOIN people ON stars.person_id = people.id
 WHERE people.name = 'Bradley Cooper' AND movies.id = stars.movie_id)
 AND EXISTS
 (SELECT * FROM stars JOIN people ON stars.person_id = people.id
 WHERE people.name = 'Jennifer Lawrence' AND movies.id = stars.movie_id);
