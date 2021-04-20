-- вывести количество фильмов в каждой категории, отсортировать по убыванию.
select count(film_id) as "number of films", category.name as "category name" from film_category 
join category using (category_id)
group by category.name 
order by 1 desc;

-- вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию.
select a.first_name, a.last_name, count(r.rental_id) as "number of rentals" from rental r
join inventory using (inventory_id)
join film_actor using (film_id)
join actor a using (actor_id)
group by a.first_name, a.last_name
order by 3 desc
limit 10;

-- вывести категорию фильмов, на которую потратили больше всего денег.
select c.name, count(p.amount) as "money spent" from payment p
join rental using (rental_id)
join inventory using (inventory_id)
join film_category using (film_id)
join category c using (category_id)
group by c.name
order by 2 desc
limit 1;

-- вывести названия фильмов, которых нет в inventory. Написать запрос без использования оператора IN.
select f.title from film f
left join inventory i using (film_id)
where i.film_id is NULL;

-- вывести топ 3 актеров, которые больше всего появлялись в фильмах в категории “Children”. Если у нескольких актеров одинаковое кол-во фильмов, вывести всех..
-- Mykola Bocharov - как виполнить второе условие я не понял :(

select a.first_name, a.last_name, count(fa.film_id) from actor a
join film_actor fa using (actor_id)
join film_category fc using (film_id)
join (select * from category where name = 'Children') c on c.category_id=fc.category_id
group by a.first_name, a.last_name
order by 3 desc
limit 3;

-- вывести города с количеством активных и неактивных клиентов (активный — customer.active = 1). Отсортировать по количеству неактивных клиентов по убыванию.
select
c.city
, count(case when active = 1 then 1 end) as "active cutomers"
, count(case when active <> 1 then 1 end) as "inactive customers"
from customer
join address a using (address_id)
join city c using (city_id)
group by c.city
order by 3 desc

-- вывести категорию фильмов, у которой самое большое кол-во часов суммарной аренды в городах (customer.address_id в этом city), и которые начинаются на букву “a”. То же самое сделать для городов в которых есть символ “-”. Написать все в одном запросе.
-- Mykola Bocharov - задовбався )))