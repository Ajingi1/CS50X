SELECT people.name FROM people WHERE people.id IN
(SELECT stars.person_id FROM stars WHERE stars.movie_id IN
(SELECT stars.movie_id FROM stars WHERE stars.person_id =
    (SELECT people.id FROM people WHERE people.name = 'Kevin Bacon' and people.birth = 1958))) AND name != 'Kevin Bacon';
