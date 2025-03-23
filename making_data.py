import pandas as pd
import random
from faker import Faker
from datetime import timedelta, datetime

# Initialize Faker and seed random number generator for reproducibility
fake = Faker()
random.seed(42)

# Define function to generate random transactions


def generate_transaction(transaction_id):
    date = fake.date_this_year()
    amount = random.choices([random.randint(100, 5000), random.randint(9500, 15000)],
                            weights=[0.8, 0.2])[0]  # 80% normal, 20% outliers
    origin_country = fake.country()
    destination_country = fake.country()
    customer_id = fake.uuid4()
    customer_risk_rating = random.choice(["Low", "Medium", "High"])

    return {
        "Transaction_ID": transaction_id,
        "Date": date,
        "Amount": amount,
        "Origin_Country": origin_country,
        "Destination_Country": destination_country,
        "Customer_ID": customer_id,
        "Customer_Risk_Rating": customer_risk_rating
    }


# Generate 1000+ synthetic transactions
transactions = [generate_transaction(i) for i in range(1, 1001)]

# Convert list of transactions to a DataFrame
df = pd.DataFrame(transactions)

# Save DataFrame to CSV
df.to_csv('transactions.csv', index=False)

print("Synthetic transaction data generated and saved as 'transactions.csv'.")
