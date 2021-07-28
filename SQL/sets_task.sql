select 'GLE' as Indicator, * from 
	(select lifeexpectancy as Federal_Republic from country where governmentform = 'Federal Republic' order by lifeexpectancy desc limit 1) as fr,
	(select lifeexpectancy as Republic from country where governmentform = 'Republic' order by lifeexpectancy desc limit 1) as r,
	(select lifeexpectancy as Others from country where governmentform not in ('Republic', 'Federal Republic') and lifeexpectancy is not null order by lifeexpectancy desc limit 1) as o
union all
select 'LLE' as Indicator, * from 
	(select lifeexpectancy as Federal_Republic from country where governmentform = 'Federal Republic' order by lifeexpectancy limit 1) as fr,
	(select lifeexpectancy as Republic from country where governmentform = 'Republic' order by lifeexpectancy limit 1) as r,
	(select lifeexpectancy as Others from country where governmentform not in ('Republic', 'Federal Republic') and lifeexpectancy is not null order by lifeexpectancy limit 1) as o