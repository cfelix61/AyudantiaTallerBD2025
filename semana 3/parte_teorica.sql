Select * from sakila.film; 
Select * from sakila.actor;   
/*3c*/
SELECT f.title, f.release_year, l.name, f.length
FROM sakila.film f, sakila.language l
WHERE f.language_id = l.language_id
ORDER BY f.title;

/*3d*/
SELECT 
f.title, 
f.release_year, 
l.name AS language, 
f.length, 
COUNT(fa.actor_id) AS actor_count
FROM sakila.film f
JOIN sakila.language l ON f.language_id = l.language_id
JOIN sakila.film_actor fa ON f.film_id = fa.film_id
GROUP BY f.film_id, f.title, f.release_year, l.name, f.length
ORDER BY f.title;


