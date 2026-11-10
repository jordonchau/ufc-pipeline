
    

    create  table
      "ufc"."main"."dim_fighter__dbt_tmp"
  
    
    as (
      with appearances as (
    select f.fighter_1_id as fighter_id, f.fighter_1_name as fighter_name, e.event_date
    from "ufc"."main"."stg_fights" f
    join "ufc"."main"."stg_events" e using (event_id)

    union all

    select f.fighter_2_id, f.fighter_2_name, e.event_date
    from "ufc"."main"."stg_fights" f
    join "ufc"."main"."stg_events" e using (event_id)
)

select
    fighter_id,
    arg_max(fighter_name, event_date) as fighter_name,   -- most recent spelling of their name
    min(event_date)                   as first_fight_date,
    max(event_date)                   as last_fight_date,
    count(*)                          as total_ufc_fights
from appearances
group by fighter_id
    );
    
  