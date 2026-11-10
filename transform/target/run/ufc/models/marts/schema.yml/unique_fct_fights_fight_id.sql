
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    fight_id as unique_field,
    count(*) as n_records

from "ufc"."main"."fct_fights"
where fight_id is not null
group by fight_id
having count(*) > 1



  
  
      
    ) dbt_internal_test