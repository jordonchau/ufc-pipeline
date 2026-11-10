select
    fight_id,
    event_id,
    bout_order,
    bout_order = 1                             as is_main_event,
    fighter_1_id,
    fighter_1                                  as fighter_1_name,
    fighter_2_id,
    fighter_2                                  as fighter_2_name,
    outcome,
    case when outcome = 'win' then fighter_1_id end as winner_id,
    weight_class,
    method                                     as method_raw,
    case
        when method like 'KO/TKO%' then 'KO/TKO'
        when method = 'SUB'        then 'Submission'
        when method like '%DEC'    then 'Decision'
        when method = 'DQ'         then 'Disqualification'
        else 'Other'
    end                                        as method_group,
    method_detail,
    try_cast("round" as integer)               as end_round,
    try_cast(split_part(cast("time" as varchar), ':', 1) as integer) * 60
      + try_cast(split_part(cast("time" as varchar), ':', 2) as integer)
                                               as end_time_seconds,
    fight_url
from {{ source('raw', 'fights') }}