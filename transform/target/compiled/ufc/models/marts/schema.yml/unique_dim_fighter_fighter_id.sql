
    
    

select
    fighter_id as unique_field,
    count(*) as n_records

from "ufc"."main"."dim_fighter"
where fighter_id is not null
group by fighter_id
having count(*) > 1


