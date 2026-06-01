with customer_accounts as (

    select *
    from {{ ref('int_banking__customer_accounts') }}

),

final as (

    select
        customer_id,
        customer_name,
        document_number,
        birth_date,
        city,
        state,
        customer_segment,
        customer_created_at,

        count(account_id) as total_accounts,
        min(opened_at) as first_account_opened_at,
        max(opened_at) as last_account_opened_at
    from customer_accounts
    group by
        customer_id,
        customer_name,
        document_number,
        birth_date,
        city,
        state,
        customer_segment,
        customer_created_at

)

select *
from final