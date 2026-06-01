with source as (

    select *
    from {{ ref('banking_customers') }}

),

renamed as (

    select
        cast(customer_id as integer) as customer_id,
        trim(customer_name) as customer_name,
        cast(document_number as varchar(20)) as document_number,
        cast(birth_date as date) as birth_date,
        upper(trim(city)) as city,
        upper(trim(state)) as state,
        lower(trim(customer_segment)) as customer_segment,
        cast(created_at as date) as created_at
    from source

)

select *
from renamed