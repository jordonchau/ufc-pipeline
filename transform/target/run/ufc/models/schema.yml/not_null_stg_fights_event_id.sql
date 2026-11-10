
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_id
from "ufc"."main"."stg_fights"
where event_id is null



  
  
      
    ) dbt_internal_test