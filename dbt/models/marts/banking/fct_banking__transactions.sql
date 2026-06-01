select
    transaction_id,
    account_id,
    customer_id,
    transaction_date,
    transaction_type,
    channel,
    amount,
    signed_amount,
    currency,
    status,
    account_type,
    account_status
from {{ ref('int_banking__account_transactions') }}