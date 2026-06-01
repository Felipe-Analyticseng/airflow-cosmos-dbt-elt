with account_transactions as (

    select *
    from {{ ref('int_banking__account_transactions') }}

),

final as (

    select
        account_id,
        customer_id,
        account_type,
        account_status,
        opened_at,

        count(transaction_id) as total_transactions,
        sum(signed_amount) as current_balance,
        min(transaction_date) as first_transaction_date,
        max(transaction_date) as last_transaction_date
    from account_transactions
    group by
        account_id,
        customer_id,
        account_type,
        account_status,
        opened_at

)

select *
from final