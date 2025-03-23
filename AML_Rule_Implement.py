import pandas as pd
from datetime import timedelta

# Define the FATF grey list (add more countries as necessary)
fatf_grey_list = ['Syria', 'Iran', 'Myanmar']

# Load the transactions data
df = pd.read_csv('transactions.csv')

# Convert date field to datetime format for easier manipulation
# Changed from 'Transaction_Date' to 'Date'
df['Date'] = pd.to_datetime(df['Date'])

# Initialize a new 'Flag' column
df['Flag'] = 'Normal'

# 1. Flagging Threshold Violations (Transactions > $10,000)
df.loc[df['Amount'] > 10000, 'Flag'] = 'Threshold Violation'

# 2. Structuring: Multiple transactions just below $10,000 from the same customer in 24 hours
# We need to group by 'Customer_ID' and check if there are multiple transactions below $10,000 within 24 hours

# Sort the DataFrame by customer and date to identify transactions in close proximity
df = df.sort_values(by=['Customer_ID', 'Date'])

# Add a new column to track if the transaction is part of structuring
df['Structuring_Flag'] = False

# Loop over each customer to check the structuring condition
for customer_id, group in df.groupby('Customer_ID'):
    for i in range(len(group) - 1):
        # Compare each transaction with the next one
        if (group.iloc[i+1]['Amount'] < 10000 and
            group.iloc[i]['Amount'] < 10000 and
                (group.iloc[i+1]['Date'] - group.iloc[i]['Date']) <= timedelta(hours=24)):  # Changed from 'Transaction_Date' to 'Date'
            df.loc[group.index[i], 'Structuring_Flag'] = True
            df.loc[group.index[i+1], 'Structuring_Flag'] = True

# Mark 'Structuring' transactions
df.loc[df['Structuring_Flag'] == True, 'Flag'] = 'Structuring'

# 3. Flagging High-Risk Jurisdictions (Transfers involving FATF grey list countries)
df.loc[df['Destination_Country'].isin(
    fatf_grey_list), 'Flag'] = 'High-Risk Jurisdiction'

# 4. Round-Number Clustering: Frequent transfers of exact amounts like 5,000 or 10,000
round_numbers = [5000, 10000]
df['Round_Amount_Flag'] = df['Amount'].isin(round_numbers)

# Mark round-number clustering transactions
df.loc[df['Round_Amount_Flag'] == True, 'Flag'] = 'Round-Number Clustering'

# Optionally: Save the flagged transactions to a new CSV
df.to_csv('flagged_transactions.csv', index=False)

# Show the flagged DataFrame
print(df[['Transaction_ID', 'Amount', 'Flag']])
