select
    f.fight_id,
    f.event_id,
    e.event_date,
    f.bout_order,
    f.is_main_event,
    f.fighter_1_id,
    f.fighter_2_id,
    f.winner_id,
    f.outcome,
    f.weight_class,
    f.method_group,
    f.method_raw,
    f.method_detail,
    f.end_round,
    f.end_time_seconds,
    (f.end_round - 1) * 300 + f.end_time_seconds as fight_duration_seconds
from {{ ref('stg_fights') }} f
join {{ ref('stg_events') }} e using (event_id)