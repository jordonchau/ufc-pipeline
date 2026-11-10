with fights as (
    select * from "ufc"."main"."fct_fights"
)

select
    fight_id, event_id, event_date,
    fighter_1_id as fighter_id,
    fighter_2_id as opponent_id,
    case outcome when 'win' then 'W' when 'draw' then 'D' when 'no contest' then 'NC' end as result,
    method_group, weight_class, end_round, fight_duration_seconds
from fights

union all

select
    fight_id, event_id, event_date,
    fighter_2_id as fighter_id,
    fighter_1_id as opponent_id,
    case outcome when 'win' then 'L' when 'draw' then 'D' when 'no contest' then 'NC' end as result,
    method_group, weight_class, end_round, fight_duration_seconds
from fights