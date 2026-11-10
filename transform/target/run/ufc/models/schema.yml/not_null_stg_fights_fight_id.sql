
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select fight_id
from "ufc"."main"."stg_fights"
where fight_id is null



  
  
      
    ) dbt_internal_test