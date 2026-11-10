
    
    

select
    fight_id as unique_field,
    count(*) as n_records

from "ufc"."main"."stg_fights"
where fight_id is not null
group by fight_id
having count(*) > 1


