/*1-a
a.	Cree en el schema info209 (no en sakila!) una vista llamada v_detalle_films que entregue el título de cada película,
 el año (reléase_year), el idioma, la duración y la cantidad de actores que están registrados en la tabla film_actor, para cada película. 
*/
CREATE VIEW info209.v_detalle_films AS
SELECT 
    f.title, 
    f.release_year, 
    l.name AS language, 
    f.length, 
    COUNT(fa.actor_id) AS actor_count
FROM sakila.film f
JOIN sakila.language l ON f.language_id = l.language_id
JOIN sakila.film_actor fa ON f.film_id = fa.film_id
GROUP BY f.film_id, f.title, f.release_year, l.name, f.length;

CREATE VIEW info209.v_detalle_films2 AS
SELECT 
    f.title, 
    f.release_year, 
    l.name AS language, 
    f.length, 
    COUNT(fa.actor_id) AS actor_count
FROM sakila.film f, sakila.language l, sakila.film_actor fa
where f.language_id = l.language_id
and  f.film_id = fa.film_id
GROUP BY f.film_id, f.title, f.release_year, l.name, f.length;

SELECT * FROM info209.v_detalle_films;
SELECT * FROM info209.v_detalle_films2;

/*1-b
b.	Cree en el schema info209 (no en sakila!) una vista que entregue el nombre y apellido de cada cliente, 
indicando el monto total que ha pagado por arriendos cada cliente. 
Realice una consulta (SELECT) a la vista, ordenando la información anterior por monto pagado, de mayor a menor. 
*/
CREATE VIEW info209.detalles_arriendos_clientes AS
select 
	c.customer_id,
    c.first_name,
    c.last_name,
    sum(p.amount)
from sakila.customer c, sakila.payment p
where c.customer_id = p.customer_id
group by c.customer_id, c.first_name, c.last_name;

select * from info209.detalles_arriendos_clientes; 

/*1-c
c.	Utilizando las funciones year() y month(), cree en el schema info209 una vista que entregue los totales de pago recibidos 
cada mes por cada empleado (staff). La vista debe desplegar el nombre y apellido de cada empleado, el mes, el año y la cantidad
 y monto total de pagos recibidos. 
*/
create view info209.total_pagos_mensuales_empleados as
select
	s.staff_id,
    s.first_name,
    s.last_name,
	s.username,
    year(p.payment_date) as anio,
    monthname(p.payment_date) as mes,
    count(p.payment_id),
    sum(p.amount)
from sakila.staff s, sakila.payment p 
where s.staff_id = p.staff_id
/*join sakila.payment p on s.staff_id = p.staff_id*/
group by s.staff_id, s.first_name, s.last_name, s.username, anio, mes;

select * from info209.total_pagos_mensuales_empleados;

/*1-d
d.	Cree una vista que entregue los nombres y apellidos de los clientes, más la cantidad de películas de acción distintas
que ha arrendado cada uno. Utilice la vista anterior para entregar la lista de clientes que ha arrendado más de 5 películas de acción. 
*/
create view info209.clientes_peliculas_accion as
select
	c.last_name,
    c.first_name,
    count(distinct f.film_id) as pelis_accion
from sakila.customer c
join sakila.rental r on c.customer_id = r.customer_id
join sakila.inventory i on r.inventory_id = i.inventory_id
join sakila.film f on i.film_id = f.film_id
join sakila.film_category fc on f.film_id = fc.film_id
join sakila.category ca on fc.category_id = ca.category_id
group by c.last_name, c.first_name
order by pelis_accion ASC;

create view info209.clientes_pelis_accion_mayor_a_5 as
select * from info209.clientes_peliculas_accion cpa
where info209.cpa.pelis_accion > 5;

select * from info209.clientes_pelis_accion_mayor_a_5;

/*PARTE 2*/
CREATE VIEW info209.pelis_no_arrendadas AS
SELECT
    f.title,
    f.release_year,
    l.name AS language_name,
    f.replacement_cost,
    COUNT(i.film_id) AS cantidad_copias
FROM sakila.film f
JOIN sakila.language l ON f.language_id = l.language_id
JOIN sakila.inventory i ON f.film_id = i.film_id
WHERE f.film_id NOT IN (
    SELECT DISTINCT i.film_id
    FROM sakila.rental r
    JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
)
GROUP BY f.title, f.release_year, l.name, f.replacement_cost
ORDER BY f.title;

/*a-
Peliculas que han sido arrendadas 1 o mas veces*/
select distinct f.film_id
from sakila.film f
join sakila.inventory i on f.film_id = i.film_id
join sakila.rental r on i.inventory_id = r.inventory_id; 

/* 
b.	Haga una consulta que entregue el listado de películas que no ha sido arrendada nunca.
Hint: Utilice la consulta anterior en la condición (WHERE), indicando “film_id NOT IN (select …)
*/
select f.film_id
from sakila.film f
where f.film_id not in 
(select distinct f.film_id
from sakila.film f
join sakila.inventory i on f.film_id = i.film_id
join sakila.rental r on i.inventory_id = r.inventory_id);

/*
c.	Utilizando la consulta anterior, cree una vista que entregue las películas que nunca han sido arrendadas. 
Debe contener la siguiente información: 
Title
Release year
Language.name
Replacement cost
Cantidad de copias en inventario

Utilice la vista anterior para realizar una consulta que haga un join entre la vista y la tabla category, 
y entregue la siguiente información: 
Category.name
Cantidad de películas que nunca han sido arrendada. 

*/
CREATE VIEW info209.pelis_no_arrendadas AS
SELECT
	f.film_id,
    f.title,
    f.release_year,
    l.name AS language_name,
    f.replacement_cost,
    COUNT(i.film_id) AS cantidad_copias
FROM sakila.film f
JOIN sakila.language l ON f.language_id = l.language_id
JOIN sakila.inventory i ON f.film_id = i.film_id
WHERE f.film_id NOT IN (
    SELECT DISTINCT i.film_id
    FROM sakila.rental r
    JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
)
GROUP BY f.film_id, f.title, f.release_year, l.name, f.replacement_cost
ORDER BY f.title;



SELECT 
    ca.name AS category_name,
    COUNT(pna.title) AS cantidad_pelis_no_arrendadas
FROM sakila.category ca
JOIN sakila.film_category fc ON ca.category_id = fc.category_id
JOIN info209.pelis_no_arrendadas pna ON fc.film_id = pna.film_id
GROUP BY ca.name
ORDER BY cantidad_pelis_no_arrendadas DESC;

drop view info209.pelis_no_arrendadas;    


    
	
	


	
