import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the flagged transaction data
df = pd.read_csv('flagged_transactions.csv')

# 1. Time-Series Graph of Transaction Volumes
# Group by Date and count the number of transactions per day
df['Date'] = pd.to_datetime(df['Date'])
transaction_volumes = df.groupby(df['Date'].dt.date).size()

# Plotting the time-series graph
plt.figure(figsize=(10, 6))
transaction_volumes.plot(kind='line', color='#1f77b4', linewidth=2)
plt.title('Transaction Volumes Over Time', fontsize=16, color='#333333')
plt.xlabel('Date', fontsize=12, color='#555555')
plt.ylabel('Number of Transactions', fontsize=12, color='#555555')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot as a JPEG file
plt.savefig('transaction_volumes_time_series.jpeg', format='jpeg', dpi=300)
plt.close()

# 2. Heatmap of High-Risk Jurisdictions (Origin vs Destination Country)
# We will create a pivot table and plot the heatmap for transaction counts between origin and destination countries
# Filter high-risk flagged transactions
risk_df = df[df['Flag'].isin(['High-Risk Jurisdiction', 'Structuring'])]
heatmap_data = risk_df.groupby(
    ['Origin_Country', 'Destination_Country']).size().unstack(fill_value=0)

# Plotting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='d',
            linewidths=0.5, cbar_kws={'label': 'Number of Transactions'})
plt.title('High-Risk Jurisdictions: Transaction Flow',
          fontsize=16, color='#333333')
plt.xlabel('Destination Country', fontsize=12, color='#555555')
plt.ylabel('Origin Country', fontsize=12, color='#555555')
plt.tight_layout()

# Save the heatmap as a JPEG file
plt.savefig('high_risk_jurisdictions_heatmap.jpeg', format='jpeg', dpi=300)
plt.close()

# 3. Pie Chart of Flagged vs. Normal Transactions
# Count the number of flagged vs. normal transactions
flagged_count = df[df['Flag'] != 'Normal'].shape[0]
normal_count = df[df['Flag'] == 'Normal'].shape[0]

# Pie chart for flagged vs normal transactions
labels = ['Flagged', 'Normal']
sizes = [flagged_count, normal_count]
colors = ['#ff9999', '#66b3ff']  # Use contrasting colors for clarity

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, wedgeprops={'edgecolor': 'black'})
plt.title('Proportion of Flagged vs. Normal Transactions',
          fontsize=16, color='#333333')
plt.tight_layout()

# Save the pie chart as a JPEG file
plt.savefig('flagged_vs_normal_transactions_pie_chart.jpeg',
            format='jpeg', dpi=300)
plt.close()

# 4. Export Flagged Transactions to CSV
flagged_transactions = df[df['Flag'] != 'Normal']
flagged_transactions.to_csv('flagged_transactions_report.csv', index=False)
print("Flagged transactions exported to 'flagged_transactions_report.csv'.")
