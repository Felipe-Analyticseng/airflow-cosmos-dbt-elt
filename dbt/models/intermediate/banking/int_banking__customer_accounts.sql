with customers as (

    select *
    from {{ ref('stg_banking__customers') }}

),

accounts as (

    select *
    from {{ ref('stg_banking__accounts') }}

),

joined as (

    select
        customers.customer_id,
        customers.customer_name,
        customers.document_number,
        customers.birth_date,
        customers.city,
        customers.state,
        customers.customer_segment,
        customers.created_at as customer_created_at,

        accounts.account_id,
        accounts.agency_number,
        accounts.account_number,
        accounts.account_type,
        accounts.account_status,
        accounts.opened_at
    from customers
    left join accounts
        on customers.customer_id = accounts.customer_id

)

select *
from joined
