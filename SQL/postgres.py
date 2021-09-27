import psycopg2

def start_planning(year: int, quarter: int, user: str, pwd: str):
    con = psycopg2.connect(database='2020_plans_Yaroslav', user=user, password=pwd, host='localhost')
    cur = con.cursor()
    # delete plan data related to the target year and quarter
    query = f'''
            delete from plan_data as pd where pd.quarterid = '{year}.{quarter}'
            '''
    cur.execute(query)
    # delete records in plan status related to the target quarter
    query = f'''
            delete from plan_status as ps where right(ps.quarterid, 1) = '{quarter}'
            '''
    cur.execute(query)
    # create planning status records
    query = f'''
            insert into plan_status
            select distinct 
                '{year}.{quarter}' as quarterid,
                'R' as status,
                current_timestamp as modifieddatetime,
                current_user as author,
                c.countrycode as country
            from company as c
            '''
    cur.execute(query)
    # generate plan data
    query = f'''
            insert into plan_data
            select
                'N' as versionid,
                coalesce(data_avg.countrycode, country_category.countrycode) as country,
                '{year}.{quarter}' as quarterid,
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
                        where cs."year" in ({year}-1, {year}-2) and quarter_yr = {quarter} and cs.ccls != 'C'
                    group by cs."year", cs.quarter_yr, c.countrycode, cs.categoryid) as data
                group by data.countrycode, data.categoryid
                order by data.countrycode) as data_avg
            right join
                (select c.countrycode, p.productcategoryid as categoryid
                from country2 as c
                cross join productcategory as p) as country_category
            on country_category.countrycode = data_avg.countrycode and country_category.categoryid = data_avg.categoryid
            '''
    cur.execute(query)
    # copy data from version N into version P
    query = f'''
            insert into plan_data 
            select 'P' as versionid,
                    plan_data.country,
                    plan_data.quarterid,
                    plan_data.pcid,
                    plan_data.salesamt
            from plan_data where plan_data.versionid = 'N'
            '''
    cur.execute(query)

    con.commit()
    con.close()
    
    print('Done.')

def set_lock(year: int, quarter: int, user: str, pwd: str):
    con = psycopg2.connect(database='2020_plans_Yaroslav', user=user, password=pwd, host='localhost')
    cur = con.cursor()
    query = f'''
            update plan_status
            set status = 'L',
                modifieddatetime = current_timestamp,
                author = current_user
                where quarterid = '{year}.{quarter}' and country in (select cm.country from country_managers as cm where cm.username = current_user)
        '''
    cur.execute(query)

    con.commit()
    con.close()
    print('Done.')

def remove_lock(year: int, quarter: int, user: str, pwd: str):
    con = psycopg2.connect(database='2020_plans_Yaroslav', user=user, password=pwd, host='localhost')
    cur = con.cursor()
    query = f'''
            update plan_status
            set status = 'R',
                modifieddatetime = current_timestamp,
                author = current_user
                where quarterid = '{year}.{quarter}' and country in (select cm.country from country_managers as cm where cm.username = current_user)
        '''
    cur.execute(query)

    con.commit()
    con.close()
    print('Done.')

def accept_plan(year: int, quarter: int, user: str, pwd: str):
    con = psycopg2.connect(database='2020_plans_Yaroslav', user=user, password=pwd, host='localhost')
    cur = con.cursor()
    # delete plan data with version A
    query = f'''
            delete from plan_data as pd
            where
                right(pd.quarterid, 1) = '{quarter}' and
                pd.versionid = 'A' and
                pd.country in (select cm.country from country_managers as cm where cm.username = current_user)
            '''
    cur.execute(query)
    # save a copy into plan data
    query = f'''
            insert into plan_data
            select 'A' as versionid,
                    pd.country,
                    pd.quarterid,
                    pd.pcid,
                    pd.salesamt
            from plan_data as pd
            where 
                pd.quarterid = '{year}.{quarter}' and 
                pd.versionid = 'P' and
                pd.country in (select cm.country from country_managers as cm where cm.username = current_user) and
                pd.country in (select ps.country from plan_status as ps where ps.status = 'R' and ps.quarterid = '{year}.{quarter}')
            '''
    cur.execute(query)
    # update plan status
    query = f'''
            update plan_status
            set status = 'A',
                modifieddatetime = current_timestamp,
                author = current_user
                where quarterid = '{year}.{quarter}' and country in (select cm.country from country_managers as cm where cm.username = current_user)
        '''
    cur.execute(query)

    con.commit()
    con.close()
    print('Done.')


if __name__ == '__main__':
    start_planning(2014, 1, 'ivan', 'sql0')

    # set_lock(2014, 1, 'sophie', 'sql1')
    # set_lock(2014, 1, 'kirill', 'sql2')

    # remove_lock(2014, 1, 'sophie', 'sql1')
    # remove_lock(2014, 1, 'kirill', 'sql2')

    # accept_plan(2014, 1, 'sophie', 'sql1')
    # accept_plan(2014, 1, 'kirill', 'sql2')