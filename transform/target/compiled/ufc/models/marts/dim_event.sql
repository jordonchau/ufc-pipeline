select
    event_id,
    event_name,
    event_date,
    extract(year from event_date) as event_year,
    location,
    country,
    event_url
from "ufc"."main"."stg_events"