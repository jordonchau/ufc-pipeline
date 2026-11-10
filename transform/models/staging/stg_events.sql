select
    event_id,
    trim(event_name)                          as event_name,
    cast(event_date as date)                  as event_date,
    trim(location)                            as location,
    trim(string_split(location, ',')[-1])     as country,
    event_url
from {{ source('raw', 'events') }}