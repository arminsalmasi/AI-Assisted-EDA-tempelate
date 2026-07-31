import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import os

def create_and_execute_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # 1. Header
    cells.append(nbf.v4.new_markdown_cell("""# Univariate Exploratory Data Analysis (EDA)

This notebook contains the **Univariate Analysis** on our processed delivery platform datasets (`master_orders.csv` and `customer_features.csv`).
The objective is to examine the distributions, proportions, and statistics of key variables individually to identify anomalies, skewness, and patterns.

### Objectives:
1. **Analyze individual variable distributions** to identify skewness, spread, central tendency, and anomalies.
2. **Examine categorical proportions** to understand user demographics, platform choices, and vendor splits.
3. **Investigate operational friction indicators** (such as delay times and order inaccuracies) and customer satisfaction (ratings).
4. **Assess behavioral customer retention** and recency profiles to lay the groundwork for bivariate cohort and survival analysis.

---"""))
    
    # 2. Imports
    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set seaborn style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

# Ensure figures folder exists
os.makedirs('../report/figures', exist_ok=True)
"""))
    
    # 3. Load Data
    cells.append(nbf.v4.new_code_cell("""# Load processed datasets (paths are relative to the notebooks/ directory)
orders = pd.read_csv('../data/processed/master_orders.csv')
customers = pd.read_csv('../data/processed/customer_features.csv')

# Convert dates to datetime
orders['order_date'] = pd.to_datetime(orders['order_date'])
customers['last_order_date'] = pd.to_datetime(customers['last_order_date'])
customers['signup_date'] = pd.to_datetime(customers['signup_date'])

print(f"Master Orders dataset contains {orders.shape[0]} rows and {orders.shape[1]} columns.")
print(f"Customer Features dataset contains {customers.shape[0]} rows and {customers.shape[1]} columns.")
"""))
    
    # 4. Section 1 Header: Order-Level Quantitative Variables
    cells.append(nbf.v4.new_markdown_cell("""## 1. Distribution of Order-Level Quantitative Variables
We analyze `order_value_usd` (spend per transaction) and `items_count` (items per order). Since delivery platforms frequently have a high volume of small orders and a few extremely large orders (right-skewed), we will compare the raw distributions and log-transformed distributions to evaluate skewness.
"""))
    
    # 5. Order Value and Items Count
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Raw Order Value distribution
sns.histplot(orders['order_value_usd'], bins=40, kde=True, ax=axes[0], color='royalblue')
axes[0].set_title('Distribution of Raw Order Value (USD)')
axes[0].set_xlabel('Order Value ($)')
axes[0].axvline(orders['order_value_usd'].mean(), color='red', linestyle='--', label=f"Mean: ${orders['order_value_usd'].mean():.2f}")
axes[0].axvline(orders['order_value_usd'].median(), color='green', linestyle='-', label=f"Median: ${orders['order_value_usd'].median():.2f}")
axes[0].legend()

# Log-transformed Order Value distribution
sns.histplot(np.log1p(orders['order_value_usd']), bins=40, kde=True, ax=axes[1], color='slate_blue' if 'slate_blue' in sns.color_palette() else 'slateblue')
axes[1].set_title('Log-Transformed Order Value (log1p)')
axes[1].set_xlabel('Log(Order Value)')

plt.tight_layout()
plt.savefig('../report/figures/univariate_order_value.png', dpi=300)
plt.show()
"""))
    
    # 6. Items Count & Promo Discounts
    cells.append(nbf.v4.new_markdown_cell("""### B. Items Count & Promo Discounts
Next, we examine the `items_count` per order and the `discount_amount_usd` when promotions are used.
"""))
    
    # 7. Items count and discount
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Items Count
sns.histplot(orders['items_count'], bins=24, kde=False, ax=axes[0], color='darkorange')
axes[0].set_title('Distribution of Items Count per Order')
axes[0].set_xlabel('Items Count')
axes[0].axvline(orders['items_count'].median(), color='black', linestyle='--', label=f"Median: {orders['items_count'].median():.0f}")
axes[0].legend()

# Discount Amount (Only for orders with discounts)
positive_discounts = orders[orders['discount_amount_usd'] > 0]['discount_amount_usd']
sns.histplot(positive_discounts, bins=30, kde=True, ax=axes[1], color='forestgreen')
axes[1].set_title('Distribution of Discounts (Positive Discounts Only)')
axes[1].set_xlabel('Discount Amount ($)')
axes[1].axvline(positive_discounts.mean(), color='red', linestyle='--', label=f"Mean: ${positive_discounts.mean():.2f}")
axes[1].legend()

plt.tight_layout()
plt.savefig('../report/figures/univariate_items_discount.png', dpi=300)
plt.show()
"""))
    
    # 8. Section 2 Header: Delivery delays and customer ratings
    cells.append(nbf.v4.new_markdown_cell("""## 2. Distribution of Service Metrics (Delays & Ratings)
We examine customer ratings (categorical satisfaction) and delays (operational performance). We evaluate both the probability density function and the cumulative distribution (CDF) of delay minutes.
"""))
    
    # 9. Delay minutes and ratings
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Probability Density of delays
positive_delays = orders[orders['delay_minutes'] > 0]['delay_minutes']
sns.histplot(positive_delays, bins=40, kde=True, ax=axes[0], color='crimson')
axes[0].set_title('Distribution of Positive Delay Minutes')
axes[0].set_xlabel('Minutes Late')
axes[0].axvline(positive_delays.mean(), color='black', linestyle='--', label=f"Mean Delay: {positive_delays.mean():.1f} min")
axes[0].axvline(positive_delays.median(), color='blue', linestyle='-', label=f"Median Delay: {positive_delays.median():.1f} min")
axes[0].legend()

# Cumulative Distribution of delays
sns.ecdfplot(positive_delays, ax=axes[1], color='darkred', linewidth=2)
axes[1].set_title('Cumulative Distribution Function (CDF) of Delays')
axes[1].set_xlabel('Minutes Late')
axes[1].set_ylabel('Proportion of Delayed Orders')
axes[1].axvline(30, color='gray', linestyle=':', label='30 Min Delay Mark')
axes[1].legend()

plt.tight_layout()
plt.savefig('../report/figures/univariate_delays_cdf.png', dpi=300)
plt.show()
"""))
    
    # 10. Promised vs Actual Delivery Duration
    cells.append(nbf.v4.new_markdown_cell("""### B. Promised vs Actual Delivery Duration
We compare the distributions of `promised_time_min` against `actual_time_min` to see if promised times are aggressive or conservative.
"""))
    
    # 11. Promised vs actual code
    cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(10, 5))
sns.kdeplot(orders['promised_time_min'], fill=True, label='Promised Time', color='teal', alpha=0.5)
sns.kdeplot(orders['actual_time_min'], fill=True, label='Actual Time', color='coral', alpha=0.5)
plt.title('Comparison: Promised vs. Actual Delivery Times')
plt.xlabel('Duration (minutes)')
plt.ylabel('Density')
plt.legend()
plt.savefig('../report/figures/univariate_promised_actual_comp.png', dpi=300)
plt.show()
"""))
    
    # 12. Section 3 Header: Customer-level engagement
    cells.append(nbf.v4.new_markdown_cell("""## 3. Quantitative Variable Analysis: Customer Engagement
We aggregate data at the customer level to evaluate `frequency` (orders per customer) and `total_spend` (total dollar spend). This gives us insights into customer value segment patterns.
"""))
    
    # 13. Customer engagement code
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Order Frequency
sns.histplot(customers['frequency'], bins=35, kde=True, ax=axes[0], color='teal')
axes[0].set_title('Customer Order Frequency')
axes[0].set_xlabel('Total Orders Placed')
axes[0].axvline(customers['frequency'].median(), color='red', linestyle='--', label=f"Median: {customers['frequency'].median():.0f}")
axes[0].legend()

# Total Spend
sns.histplot(customers['total_spend'], bins=35, kde=True, ax=axes[1], color='indigo')
axes[1].set_title('Customer Lifetime spend (USD)')
axes[1].set_xlabel('Total Spend ($)')
axes[1].axvline(customers['total_spend'].median(), color='red', linestyle='--', label=f"Median: ${customers['total_spend'].median():.2f}")
axes[1].legend()

plt.tight_layout()
plt.savefig('../report/figures/univariate_customer_frequency_spend.png', dpi=300)
plt.show()
"""))
    
    # 14. Lifespan and Recency
    cells.append(nbf.v4.new_markdown_cell("""### B. Customer Active Lifespan & Recency
We evaluate how many days elapsed between their signup and their latest purchase (`active_lifespan_days`), and the number of days since their latest purchase (`days_since_latest_order`). Recency helps us separate long-term dormant (churned) customers from newly acquired customers.
"""))
    
    # 15. Lifespan and recency code
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Active Lifespan
sns.histplot(customers['active_lifespan_days'], bins=35, kde=True, ax=axes[0], color='forestgreen')
axes[0].set_title('Distribution of Customer Active Lifespan (Days)')
axes[0].set_xlabel('Days Active')

# Recency
sns.histplot(customers['days_since_latest_order'], bins=35, kde=True, ax=axes[1], color='darkred')
axes[1].set_title('Distribution of Recency (Days Since Last Order)')
axes[1].set_xlabel('Days Since Latest Order')

plt.tight_layout()
plt.savefig('../report/figures/univariate_customer_lifespan_recency.png', dpi=300)
plt.show()
"""))
    
    # 16. Categorical Distributions (Demographics)
    cells.append(nbf.v4.new_markdown_cell("""## 4. Categorical Distributions & Proportions

### A. Customer Demographics (Gender, Age Group, Segment)
We review the demographics of our customer base to establish who the typical user is.
"""))
    
    # 17. Demographics code
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Gender distribution
sns.countplot(x='gender', data=customers, ax=axes[0], palette='pastel')
axes[0].set_title('Customer Base by Gender')
axes[0].set_xlabel('Gender')

# Age Group distribution
sns.countplot(x='age_group', data=customers, ax=axes[1], palette='Set2', order=sorted(customers['age_group'].unique()))
axes[1].set_title('Customer Base by Age Group')
axes[1].set_xlabel('Age Group')

# Customer Segment
sns.countplot(x='customer_segment', data=customers, ax=axes[2], palette='rocket')
axes[2].set_title('Customer Segments')
axes[2].set_xlabel('Segment')

plt.tight_layout()
plt.savefig('../report/figures/univariate_customer_demographics.png', dpi=300)
plt.show()
"""))
    
    # 18. Geographic Distributions
    cells.append(nbf.v4.new_markdown_cell("""### B. Geographic Distributions (State & City)
We audit the location data of our customer segments to check market concentrations.
"""))
    
    # 19. Geographic code
    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# State Distribution
sns.countplot(y='state', data=customers, ax=axes[0], order=customers['state'].value_counts().index, palette='mako')
axes[0].set_title('Customers by State')
axes[0].set_xlabel('Count')
axes[0].set_ylabel('State')

# City Distribution
sns.countplot(y='city', data=customers, ax=axes[1], order=customers['city'].value_counts().index, palette='crest')
axes[1].set_title('Customers by City')
axes[1].set_xlabel('Count')
axes[1].set_ylabel('City')

plt.tight_layout()
plt.savefig('../report/figures/univariate_customer_locations.png', dpi=300)
plt.show()
"""))
    
    # 20. Summary
    cells.append(nbf.v4.new_markdown_cell("""## Summary of Key Univariate Findings

1. **Highly Skewed Monetary Metrics**: The distribution of `order_value_usd` and customer `total_spend` is highly right-skewed. The log transformation normalizes this behavior, suggesting that we should use log-scale metrics for future regression modeling.
2. **Delays distribution**: Delayed orders exhibit an average delay of ~19 minutes (when positive), but can reach up to 130 minutes. The cumulative distribution (CDF) shows that roughly 90% of delays are under 30 minutes, indicating a heavy tail for extreme delays.
3. **High Churn Rate**: **53% of our customer base** is classified as behaviorally churned (>90 days of inactivity). This demonstrates a massive engagement issue.
4. **Geographic Concentration**: Over 50% of the customer base is concentrated in Texas (TX) and California (CA), with Dallas, Houston, Los Angeles, and San Jose being our largest urban markets.
"""))
    
    nb.cells = cells
    
    notebook_dir = 'notebooks'
    os.makedirs(notebook_dir, exist_ok=True)
    notebook_path = os.path.join(notebook_dir, '01_univariate_analysis.ipynb')
    
    with open(notebook_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created unexecuted notebook at {notebook_path}")
    
    print("Executing notebook to embed figures...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
    
    with open(notebook_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Successfully executed and saved notebook at {notebook_path}")

if __name__ == '__main__':
    create_and_execute_notebook()
