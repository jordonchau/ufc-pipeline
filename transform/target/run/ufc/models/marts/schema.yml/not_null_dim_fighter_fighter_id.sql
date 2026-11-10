
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select fighter_id
from "ufc"."main"."dim_fighter"
where fighter_id is null



  
  
      
    ) dbt_internal_test