with accounts as (

    select *
    from {{ ref('stg_banking__accounts') }}

),

transactions as (

    select *
    from {{ ref('stg_banking__transactions') }}

),

joined as (

    select
        transactions.transaction_id,
        transactions.account_id,
        accounts.customer_id,
        transactions.transaction_date,
        transactions.transaction_type,
        transactions.channel,
        transactions.amount,
        transactions.currency,
        transactions.status,

        case
            when transactions.status <> 'approved' then 0
            when transactions.transaction_type in ('withdrawal', 'payment', 'transfer_out') then transactions.amount * -1
            else transactions.amount
        end as signed_amount,

        accounts.account_type,
        accounts.account_status,
        accounts.opened_at
    from transactions
    left join accounts
        on transactions.account_id = accounts.account_id

)

select *
from joined