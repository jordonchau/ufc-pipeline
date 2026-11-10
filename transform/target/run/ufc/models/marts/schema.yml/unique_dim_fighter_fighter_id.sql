
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    fighter_id as unique_field,
    count(*) as n_records

from "ufc"."main"."dim_fighter"
where fighter_id is not null
group by fighter_id
having count(*) > 1



  
  
      
    ) dbt_internal_test