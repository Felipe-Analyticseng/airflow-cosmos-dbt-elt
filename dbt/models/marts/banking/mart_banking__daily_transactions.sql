with account_transactions as (

    select *
    from {{ ref('int_banking__account_transactions') }}

),

final as (

    select
        transaction_date,
        status,
        transaction_type,
        count(transaction_id) as total_transactions,
        sum(amount) as gross_amount,
        sum(signed_amount) as net_amount
    from account_transactions
    group by
        transaction_date,
        status,
        transaction_type

)

select *
from final