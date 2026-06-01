with source as (

    select *
    from {{ ref('banking_accounts') }}

),

renamed as (

    select
        cast(account_id as integer) as account_id,
        cast(customer_id as integer) as customer_id,
        cast(agency_number as integer) as agency_number,
        cast(account_number as integer) as account_number,
        lower(trim(account_type)) as account_type,
        lower(trim(account_status)) as account_status,
        cast(opened_at as date) as opened_at
    from source

)

select *
from renamed