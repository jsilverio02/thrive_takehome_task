--- Users Dimensions Table Schema

create view dim_users as
select distinct id, name, is_customer from users order by id;