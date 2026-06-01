from __future__ import annotations

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path


random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEEDS_DIR = PROJECT_ROOT / "dbt" / "seeds"

SEEDS_DIR.mkdir(parents=True, exist_ok=True)


CUSTOMER_SEGMENTS = ["retail", "premium", "private", "business"]
ACCOUNT_TYPES = ["checking", "savings", "salary"]
ACCOUNT_STATUS = ["active", "active", "active", "blocked", "closed"]
TRANSACTION_TYPES = ["deposit", "withdrawal", "payment", "transfer_in", "transfer_out"]
CHANNELS = ["mobile_app", "internet_banking", "atm", "branch"]
TRANSACTION_STATUS = ["approved", "approved", "approved", "pending", "rejected"]

CITIES_STATES = [
    ("Sao Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"),
    ("Florianopolis", "SC"),
    ("Salvador", "BA"),
    ("Recife", "PE"),
    ("Porto Alegre", "RS"),
    ("Goiania", "GO"),
    ("Brasilia", "DF"),
]


def random_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def document_number() -> str:
    """
    Documento fictício com 11 dígitos.

    Mantemos como string porque documentos não são métricas.
    Isso evita erro de integer out of range no dbt seed/Postgres.
    """
    return "".join(str(random.randint(0, 9)) for _ in range(11))


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    output_path = SEEDS_DIR / filename

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {output_path} with {len(rows)} rows")


def generate_customers(total_customers: int = 300) -> list[dict]:
    rows = []

    for customer_id in range(1, total_customers + 1):
        city, state = random.choice(CITIES_STATES)

        rows.append(
            {
                "customer_id": customer_id,
                "customer_name": f"Customer {customer_id:04d}",
                "document_number": document_number(),
                "birth_date": random_date(date(1960, 1, 1), date(2005, 12, 31)).isoformat(),
                "city": city,
                "state": state,
                "customer_segment": random.choice(CUSTOMER_SEGMENTS),
                "created_at": random_date(date(2021, 1, 1), date(2025, 12, 31)).isoformat(),
            }
        )

    return rows


def generate_accounts(customers: list[dict]) -> list[dict]:
    rows = []
    account_id = 1

    for customer in customers:
        number_of_accounts = random.choice([1, 1, 1, 2])

        for _ in range(number_of_accounts):
            rows.append(
                {
                    "account_id": account_id,
                    "customer_id": customer["customer_id"],
                    "agency_number": random.randint(1000, 9999),
                    "account_number": random.randint(100000, 999999),
                    "account_type": random.choice(ACCOUNT_TYPES),
                    "account_status": random.choice(ACCOUNT_STATUS),
                    "opened_at": random_date(date(2021, 1, 1), date(2026, 1, 31)).isoformat(),
                }
            )
            account_id += 1

    return rows


def generate_transactions(accounts: list[dict], total_transactions: int = 1000) -> list[dict]:
    rows = []

    for transaction_id in range(1, total_transactions + 1):
        account = random.choice(accounts)
        transaction_type = random.choice(TRANSACTION_TYPES)

        amount = round(random.uniform(10, 5000), 2)

        rows.append(
            {
                "transaction_id": transaction_id,
                "account_id": account["account_id"],
                "transaction_date": random_date(date(2025, 1, 1), date(2026, 5, 31)).isoformat(),
                "transaction_type": transaction_type,
                "channel": random.choice(CHANNELS),
                "amount": amount,
                "currency": "BRL",
                "status": random.choice(TRANSACTION_STATUS),
            }
        )

    return rows


def main() -> None:
    customers = generate_customers()
    accounts = generate_accounts(customers)
    transactions = generate_transactions(accounts)

    write_csv(
        "banking_customers.csv",
        [
            "customer_id",
            "customer_name",
            "document_number",
            "birth_date",
            "city",
            "state",
            "customer_segment",
            "created_at",
        ],
        customers,
    )

    write_csv(
        "banking_accounts.csv",
        [
            "account_id",
            "customer_id",
            "agency_number",
            "account_number",
            "account_type",
            "account_status",
            "opened_at",
        ],
        accounts,
    )

    write_csv(
        "banking_transactions.csv",
        [
            "transaction_id",
            "account_id",
            "transaction_date",
            "transaction_type",
            "channel",
            "amount",
            "currency",
            "status",
        ],
        transactions,
    )


if __name__ == "__main__":
    main()