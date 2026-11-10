
    
    

with child as (
    select winner_id as from_field
    from "ufc"."main"."fct_fights"
    where winner_id is not null
),

parent as (
    select fighter_id as to_field
    from "ufc"."main"."dim_fighter"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


