with source as (

    select *
    from {{ ref('banking_transactions') }}

),

renamed as (

    select
        cast(transaction_id as integer) as transaction_id,
        cast(account_id as integer) as account_id,
        cast(transaction_date as date) as transaction_date,
        lower(trim(transaction_type)) as transaction_type,
        lower(trim(channel)) as channel,
        cast(amount as numeric(12, 2)) as amount,
        upper(trim(currency)) as currency,
        lower(trim(status)) as status
    from source

)

select *
from renamed