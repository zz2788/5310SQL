--drop table amenities, basement, basic_info, bathroom, dwelling, electricity, fireplace, garage, kitchen, msinformation, neighborhood_info, pool, porch, quality_and_condition, rooms, sales_info;

--Q1
select neighborhood, avg(lotarea) as avg_lot_area
from basic_info b join neighborhood_info n on b.id = n.neighborhood_id
group by neighborhood; 

--Q2
select garage_num, avg(tot_room_num) as avg_room
from rooms
where garage_num = 0
group by garage_num;

--Q3
select sales_id
from sales_info
where yrsold = 2009
order by saleprice
limit 1;

--Q4
create view room_number as 
	select * from rooms;
	
select * from room_number;

--Q5
select yrsold, avg(saleprice) as avgprice 
from neighborhood_info n join sales_info s on n.neighborhood_id=s.sales_id
where yrsold > 2007 and neighborhood = 'Sawyer'
group by neighborhood, yrsold;


--Q6
create or replace function quality_info_for (neighborhood_name varchar(100))
returns table ( id int,
		neighborhood varchar(100),
		overallqual varchar(100)) as
$$ 
	begin 
	return query
	select b.id, n.neighborhood, q.overallqual from basic_info b
	join neighborhood_info n on b.id=n.neighborhood_id
	join quality_and_condition q on n.neighborhood_id=q.id
	where n.neighborhood = quality_info_for.neighborhood_name;
 END
$$
language plpgsql;
 
select * from quality_info_for ('Veenker');

--Q7
select bldgtype, saleprice
from dwelling d join sales_info s on d.dwelling_id = s.sales_id
where yrsold = '2010'
order by saleprice 
limit 1;

--Q8
select housestyle, avg(saleprice) as avgprice, yrsold
from dwelling d join sales_info s on d.dwelling_id = s.sales_id
where yrsold = '2010' and housestyle = '1Story'
group by yrsold, housestyle;

--Q9
select lotarea 
from basic_info
Where lotarea > 10000
order by lotarea desc;

--Q10
select q.id
from quality_and_condition q inner join rooms r on q.id = r.room_id
where r.bathroom_num > 2 and q.yearbuilt between 2001 and 2021;