
    
    

with all_values as (

    select
        result as value_field,
        count(*) as n_records

    from "ufc"."main"."fct_fighter_fights"
    group by result

)

select *
from all_values
where value_field not in (
    'W','L','D','NC'
)


