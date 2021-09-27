-- TASK 1
grant select on all tables in schema "public" to planadmin;
grant update, insert, delete on  public.plan_data, public.plan_status, public.country_managers to planadmin;
revoke select on public.v_plan, public.v_plan_edit from planadmin;

grant select on all tables in schema "public" to planmanager;
grant update, insert, delete on  public.plan_data to planmanager;
grant update on public.plan_status, public.v_plan_edit to planmanager;

create user ivan with password 'sql0';
create user sophie with password 'sql1';
create user kirill with password 'sql2';

grant planadmin to ivan;
grant planmanager to sophie, kirill;

insert into public.country_managers (username, country)
	values ('sophie','US'), ('sophie', 'CA');
insert into public.country_managers (username, country)
	values ('kirill', 'FR'), ('kirill', 'GB'), ('kirill', 'DE'), ('kirill', 'AU');

-- TASK 2
create materialized view product2 as
select pc.productcategoryid as pcid, p.productid as productid, pc."name" as pcname, p."name" as pname
from product as p
	left join productsubcategory as psc using(productsubcategoryid)
	left join productcategory as pc using(productcategoryid)
with no data;

refresh materialized view product2;

create materialized view country2 as
select distinct a.countryregioncode as countrycode from address as a
with no data;

refresh materialized view country2;

grant select on product2, country2 to planadmin, planmanager;


-- TASK 3
insert into company (cname, countrycode, city)
select distinct c.companyname as cname, a.countryregioncode as countrycode, a.city
from (select min(customerid) as customerid, companyname from customer group by companyname) as c
	join customeraddress as ca on c.customerid = ca.customerid
	join address as a on ca.addressid = a.addressid
where ca.addresstype = 'Main Office';

-- TASK 4
insert into company_abc
select cid, 
	s as salestotal,
	case
		when srt <= sa then 'A'
		when srt <= sb then 'B'
		else 'C'
	end as cls,
	sales_total.yr as year
from 
	(select date_part('y', s.orderdate) as yr, sum(s.subtotal) as s, sum(s.subtotal) * 0.8 as sa, sum(s.subtotal) * 0.95 as sb
	from salesorderheader as s
		join customer as c on c.customerid = s.customerid
		join company as cm on cm.cname = c.companyname
	group by date_part('y', s.orderdate)
	having date_part('y', s.orderdate) in (2012, 2013)) as sales_total
join 
	(select cid, cname, yr, st,
	sum(st) over (partition by yr order by yr desc, st desc, row_num) as srt
	from
		(select cm.id as cid, 
				cm.cname, 
				date_part('y', s.orderdate) as yr, 
				sum(s.subtotal) as st,
				row_number() over(order by date_part('y', s.orderdate) desc, sum(s.subtotal) desc) as row_num
		from salesorderheader as s
			join customer as c on c.customerid = s.customerid
			join company as cm on cm.cname = c.companyname
		group by cm.id, cm.cname, date_part('y', s.orderdate)
		having date_part('y', s.orderdate) in (2012, 2013)
		order by yr desc, st desc) as data_st) as sales_rating
on sales_total.yr = sales_rating.yr;

/*select cname, yr, st,
	sum(st) over (partition by yr order by yr desc, st desc rows between (select count(*) from company c2) preceding and current row) as srt
from
	(select cm.cname, date_part('y', s.orderdate) as yr, sum(s.subtotal) as st
		from salesorderheader as s
			join customer as c on c.customerid = s.customerid
			join company as cm on cm.cname = c.companyname
		group by cm.cname, date_part('y', s.orderdate)
		having date_part('y', s.orderdate) in (2012, 2013)
		order by yr desc, st desc) as data_st


select cm.id as cid, cm.cname, date_part('y', s.orderdate) as yr, sum(s.subtotal) as st
		from salesorderheader as s
			join customer as c on c.customerid = s.customerid
			join company as cm on cm.cname = c.companyname
		group by cm.id, cm.cname, date_part('y', s.orderdate)
		having date_part('y', s.orderdate) in (2012, 2013)
		order by st desc

		
select date_part('y', s.orderdate) as yr, sum(s.subtotal) as s, sum(s.subtotal) * 0.8 as sa, sum(s.subtotal) * 0.95 as sb
	from salesorderheader as s
		join customer as c on c.customerid = s.customerid
		join company as cm on cm.cname = c.companyname
	group by date_part('y', s.orderdate)
	having date_part('y', s.orderdate) in (2012, 2013)*/


-- TASK 5
insert into company_sales
select 
	cm.id as cid,
	sum(sd.linetotal) as salesamt,
	date_part('y', sh.orderdate) as year,
	date_part('quarter', sh.orderdate) as quarter_yr,
	''|| date_part('y', sh.orderdate) || '.' || date_part('quarter', sh.orderdate) as qr,
	p2.pcid as categoryid,
	cabc.cls as ccls
from
	salesorderheader as sh
	join salesorderdetail as sd on sd.salesorderid = sh.salesorderid
	join customer as c on c.customerid = sh.customerid
	join company as cm on cm.cname = c.companyname
	join product2 as p2 on p2.productid = sd.productid
	join company_abc as cabc on cabc.cid = cm.id and cabc."year" = date_part('y', sh.orderdate)
group by date_part('y', sh.orderdate), 
		date_part('quarter', sh.orderdate),
		''|| date_part('y', sh.orderdate) || '.' || date_part('quarter', sh.orderdate),
		cm.id, p2.pcid, cabc.cls;

		
/*select distinct 
	cm.id as cid,
	date_part('y', sh.orderdate) as year,
	date_part('quarter', sh.orderdate) as quarter_yr,
	''|| date_part('y', sh.orderdate) || '.' || date_part('quarter', sh.orderdate) as qr,
	p2.pcid as categoryid,
	cabc.cls as ccls,
	sum(sd.linetotal) over (partition by date_part('y', sh.orderdate), date_part('quarter', sh.orderdate), cm.id, p2.pcid)
from
	salesorderheader as sh
	join salesorderdetail as sd on sd.salesorderid = sh.salesorderid
	join customer as c on c.customerid = sh.customerid
	join company as cm on cm.cname = c.companyname
	join product2 as p2 on p2.productid = sd.productid
	join company_abc as cabc on cabc.cid = cm.id and cabc."year" = date_part('y', sh.orderdate)*/
	
-- TASK 6
insert into plan_status
select distinct 
	'2014.1' as quarterid,
	'R' as status,
	current_timestamp as modifieddatetime,
	'ivan' as author,
	c.countrycode as country
from company as c;


insert into plan_data
select
	'N' as versionid,
	coalesce(data_avg.countrycode, country_category.countrycode) as country,
	'2014.1' as quarterid,
	coalesce(data_avg.categoryid, country_category.categoryid) as pcid,
	coalesce(data_avg.avg, 0) as salesamt
from
	(select 
		data.countrycode, data.categoryid,
		avg(s)
	from
		(select 
			cs."year" as yr,
			cs.quarter_yr as quarter_yr,
			c.countrycode as countrycode,
			cs.categoryid as categoryid,
			sum(salesamt) as s
		from company_sales as cs 
			join company as c on cs.cid = c.id
			where cs."year" in (2014-1, 2014-2) and quarter_yr = 1 and cs.ccls != 'C'
		group by cs."year", cs.quarter_yr, c.countrycode, cs.categoryid) as data
	group by data.countrycode, data.categoryid
	order by data.countrycode) as data_avg
right join
	(select c.countrycode, p.productcategoryid as categoryid
	from country2 as c
	cross join productcategory as p) as country_category
on country_category.countrycode = data_avg.countrycode and country_category.categoryid = data_avg.categoryid

insert into plan_data 
select 'R' as versionid,
		plan_data.country,
		plan_data.quarterid,
		plan_data.pcid,
		plan_data.salesamt
from plan_data where plan_data.versionid = 'N'



select 
	cs."year" as yr,
	cs.quarter_yr as quarter_yr,
	c.countrycode as countrycode,
	cs.categoryid as categoryid,
	sum(salesamt) as s
from company_sales as cs 
	join company as c on cs.cid = c.id
where cs."year" in (2014-1, 2014-2) and quarter_yr = 1 and cs.ccls != 'C'
group by cs."year", cs.quarter_yr, c.countrycode, cs.categoryid

/*select 
		cs."year" as yr,
		cs.quarter_yr as quarter_yr,
		c.countrycode as countrycode,
		cs.categoryid as categoryid,
		sum(salesamt) as s
	from company_sales as cs 
		join company as c on cs.cid = c.id
		where cs."year" in (2014-1, 2014-2) and quarter_yr = 1 and cs.ccls != 'C'
	group by cs."year", cs.quarter_yr, c.coun	trycode, cs.categoryid;
	
select c.countryregioncode, p.productcategoryid
	from country2 as c
	cross join productcategory as p*/

-- TASK 7
update plan_status
set status = 'L',
	modifieddatetime = current_timestamp,
	author = 'sophie'
	where quarterid = '2014.1' and country in (select cm.country from country_managers as cm where cm.username = 'sophie');


-- TASK 8
insert into plan_data
select 'A' as versionid,
		pd.country,
		pd.quarterid,
		pd.pcid,
		pd.salesamt
from plan_data as pd
where 
	pd.quarterid = '2014.1' and 
	pd.versionid = 'P' and
	pd.country in (select cm.country from country_managers as cm where cm.username = 'kirill') and
	pd.country in (select ps.country from plan_status as ps where ps.status = 'R' and ps.quarterid = '2014.1')
	

delete from plan_data as pd
where
	pd.quarterid = '2014.1' and
	pd.versionid = 'A' and
	pd.country in (select cm.country from country_managers as cm where cm.username = 'kirill');
	
	
-- TASK 9
create materialized view mv_plan_fact_2014_q1 as 
select
	quarterid as quarter,
	sales_plan.country,
	category_name as category_name,
	round(sales_plan.salesamt - sales_fact.salesamt, 0) as dev,
	case
		when sales_plan.salesamt = 0 then null
		else ''|| round((sales_plan.salesamt - sales_fact.salesamt)/sales_plan.salesamt * 100, 0) || '%' 
	end as dev_perc
from
	(select 
		cm.countrycode as country,
		p2.pcid,
		p2.pcname as category_name,
		sum(sd.linetotal) as salesamt
	from 
		salesorderheader as sh
		join salesorderdetail as sd on sd.salesorderid = sh.salesorderid
		join customer as c on c.customerid = sh.customerid
		join company as cm on cm.cname = c.companyname
		join product2 as p2 on p2.productid = sd.productid
	where
		date_part('y', sh.orderdate) = 2014 and
		date_part('quarter', sh.orderdate) = 1 and
		cm.id in (select c_abc.cid from company_abc as c_abc where c_abc.cls in ('A', 'B') and c_abc."year" = 2013)
	group by cm.countrycode, p2.pcid, p2.pcname) as sales_fact
join
	(select * from plan_data as pd where pd.versionid = 'A') as sales_plan
on sales_plan.country = sales_fact.country and sales_plan.pcid = sales_fact.pcid
order by sales_plan.country;

refresh materialized view mv_plan_fact_2014_q1;

--round(sales_plan.salesamt, 0) as s_plan,
--round(sales_fact.salesamt, 0) as s_fact,

select 
	cm.countrycode as country,
	p2.pcid,
	p2.pcname as category_name,
	sum(sd.linetotal) as s
from 
	salesorderheader as sh
	join salesorderdetail as sd on sd.salesorderid = sh.salesorderid
	join customer as c on c.customerid = sh.customerid
	join company as cm on cm.cname = c.companyname
	join product2 as p2 on p2.productid = sd.productid
where
	date_part('y', sh.orderdate) = 2014 and
	date_part('quarter', sh.orderdate) = 1 and
	cm.id in (select c_abc.cid from company_abc as c_abc where c_abc.cls in ('A', 'B') and c_abc."year" = 2013)
group by cm.countrycode, p2.pcid, p2.pcname


select * from plan_data as pd where pd.versionid = 'A'
	
	