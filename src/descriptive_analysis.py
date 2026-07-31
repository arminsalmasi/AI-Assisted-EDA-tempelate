import pandas as pd
import numpy as np
import os

def run_descriptive_analysis():
    print("Loading processed datasets...")
    orders_path = 'data/processed/master_orders.csv'
    customers_path = 'data/processed/customer_features.csv'
    
    orders = pd.read_csv(orders_path)
    customers = pd.read_csv(customers_path)
    
    # Convert dates
    orders['transaction_date'] = pd.to_datetime(orders['transaction_date'])
    orders['registration_date'] = pd.to_datetime(orders['registration_date'])
    customers['last_order_date'] = pd.to_datetime(customers['last_order_date'])
    customers['registration_date'] = pd.to_datetime(customers['registration_date'])
    
    print("Calculating statistics...")
    
    # 1. Order-level Numeric Statistics
    order_numeric_cols = ['quantity_items', 'gross_amount_usd', 'coupon_discount_usd', 'net_amount_usd', 'late_minutes', 'user_rating']
    order_stats = orders[order_numeric_cols].describe().transpose()
    order_stats['median'] = orders[order_numeric_cols].median()
    order_stats = order_stats[['count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max']]
    
    # 2. Customer-level Numeric Statistics
    customer_numeric_cols = [
        'frequency', 'total_spend', 'total_net_spend', 'total_discount',
        'average_order_value', 'average_items_count', 'average_rating',
        'average_delay_minutes', 'delayed_order_ratio', 'inaccurate_order_ratio',
        'promo_order_ratio', 'active_lifespan_days', 'days_since_latest_order'
    ]
    customer_stats = customers[customer_numeric_cols].describe().transpose()
    customer_stats['median'] = customers[customer_numeric_cols].median()
    customer_stats = customer_stats[['count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max']]
    
    # 3. Categorical Distributions
    # Preferred Device
    device_dist = customers['device_type'].value_counts()
    device_pct = customers['device_type'].value_counts(normalize=True) * 100
    device_summary = pd.DataFrame({'Count': device_dist, 'Percentage (%)': device_pct})
    
    # Customer Segment
    segment_dist = customers['account_segment'].value_counts()
    segment_pct = customers['account_segment'].value_counts(normalize=True) * 100
    segment_summary = pd.DataFrame({'Count': segment_dist, 'Percentage (%)': segment_pct})
    
    # Churn Status
    churn_dist = customers['is_churned'].value_counts()
    churn_pct = customers['is_churned'].value_counts(normalize=True) * 100
    churn_summary = pd.DataFrame({'Count': churn_dist, 'Percentage (%)': churn_pct})
    churn_summary.index = ['Active', 'Churned'] if churn_summary.index[0] == 0 else ['Churned', 'Active']
    
    # Vendor Category (from orders)
    vendor_dist = orders['merchant_category'].value_counts()
    vendor_pct = orders['merchant_category'].value_counts(normalize=True) * 100
    vendor_summary = pd.DataFrame({'Count': vendor_dist, 'Percentage (%)': vendor_pct})
    
    # Delivery Type (from orders)
    delivery_dist = orders['fulfillment_type'].value_counts()
    delivery_pct = orders['fulfillment_type'].value_counts(normalize=True) * 100
    delivery_summary = pd.DataFrame({'Count': delivery_dist, 'Percentage (%)': delivery_pct})
    
    # State distribution (from customers)
    state_dist = customers['location_state'].value_counts()
    state_pct = customers['location_state'].value_counts(normalize=True) * 100
    state_summary = pd.DataFrame({'Count': state_dist, 'Percentage (%)': state_pct})

    # 4. Generate Markdown Report
    report_path = 'report/descriptive_stats.md'
    os.makedirs('report', exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# DESCRIPTIVE ANALYSIS REPORT\n\n")
        f.write("This report provides summary statistics for the feature-engineered datasets at the order and customer level.\n\n")
        
        # Section 1
        f.write("## 1. Order-Level Transaction Statistics\n")
        f.write("Summary statistics based on all transactions in the dataset:\n\n")
        f.write(order_stats.to_markdown() + "\n\n")
        
        # Section 2
        f.write("## 2. Customer-Level Aggregated Statistics\n")
        f.write("Summary statistics based on customers aggregated from registration date to latest transaction:\n\n")
        f.write(customer_stats.to_markdown() + "\n\n")
        
        # Section 3
        f.write("## 3. Categorical Distributions & Proportions\n\n")
        
        f.write("### A. Customer Churn Rate (90-Day Inactivity Window)\n")
        f.write(churn_summary.to_markdown() + "\n\n")
        
        f.write("### B. Preferred Devices\n")
        f.write(device_summary.to_markdown() + "\n\n")
        
        f.write("### C. Customer Demographics Segment\n")
        f.write(segment_summary.to_markdown() + "\n\n")
        
        f.write("### D. Orders by Vendor Category\n")
        f.write(vendor_summary.to_markdown() + "\n\n")
        
        f.write("### E. Orders by Delivery Type\n")
        f.write(delivery_summary.to_markdown() + "\n\n")
        
        f.write("### F. Customers by State\n")
        f.write(state_summary.to_markdown() + "\n\n")
        
    print(f"Descriptive statistics successfully exported to {report_path}!")

if __name__ == '__main__':
    run_descriptive_analysis()
