with account_transactions as (

    select *
    from {{ ref('int_banking__account_transactions') }}

),

final as (

    select
        customer_id,
        count(distinct account_id) as total_accounts,
        count(transaction_id) as total_transactions,
        sum(signed_amount) as current_balance,
        sum(case when signed_amount > 0 then signed_amount else 0 end) as total_inflow,
        sum(case when signed_amount < 0 then signed_amount else 0 end) as total_outflow
    from account_transactions
    group by customer_id

)

select *
from final