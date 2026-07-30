import os
import pandas as pd
import numpy as np

def prepare_datasets():
    # 1. Load Raw Datasets
    print("Loading raw datasets...")
    customers_path = 'data/raw/customers.csv'
    orders_path = 'data/raw/orders.csv'
    deliveries_path = 'data/raw/deliveries.csv'
    
    customers = pd.read_csv(customers_path)
    orders = pd.read_csv(orders_path)
    deliveries = pd.read_csv(deliveries_path)
    
    # Convert dates to datetime
    customers['signup_date'] = pd.to_datetime(customers['signup_date'])
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # 2. Build Master Order-level Dataset
    print("Building master order-level dataset...")
    # Merge orders and deliveries (1-to-1 mapping on order_id)
    orders_deliveries = pd.merge(orders, deliveries, on='order_id', how='inner')
    
    # Merge with customers on customer_id
    master_orders = pd.merge(orders_deliveries, customers, on='customer_id', how='inner')
    
    # Sort chronologically by customer and date
    master_orders = master_orders.sort_values(by=['customer_id', 'order_date']).reset_index(drop=True)
    
    # Engineer Order-level Features
    master_orders['is_delayed'] = (master_orders['delivery_status'] == 'Delayed').astype(int)
    master_orders['is_inaccurate'] = master_orders['order_accuracy'].isin(['Partial', 'Wrong']).astype(int)
    master_orders['days_since_signup'] = (master_orders['order_date'] - master_orders['signup_date']).dt.days
    master_orders['net_value_usd'] = master_orders['order_value_usd'] - master_orders['discount_amount_usd']
    master_orders['is_promo_used'] = (master_orders['promo_used'] == 'Yes').astype(int)
    
    # Calculate chronological sequence of orders for each customer
    master_orders['order_seq'] = master_orders.groupby('customer_id').cumcount() + 1
    
    # Ensure intermediate directory exists
    os.makedirs('data/interim', exist_ok=True)
    
    # Save master order-level dataset
    master_orders_path = 'data/interim/master_orders.csv'
    master_orders.to_csv(master_orders_path, index=False)
    print(f"Saved master orders: {master_orders.shape} to {master_orders_path}")
    
    # 3. Build Aggregated Customer-level Dataset
    print("Building customer-level aggregated dataset...")
    
    # Timeline metadata for Churn calculation
    max_dataset_date = master_orders['order_date'].max()
    print(f"Max date in dataset: {max_dataset_date.strftime('%Y-%m-%d')}")
    
    # General groupings
    grouped = master_orders.groupby('customer_id')
    
    # Aggregate basic features
    cust_agg = grouped.agg(
        frequency=('order_id', 'count'),
        total_spend=('order_value_usd', 'sum'),
        total_net_spend=('net_value_usd', 'sum'),
        total_discount=('discount_amount_usd', 'sum'),
        average_order_value=('order_value_usd', 'mean'),
        average_items_count=('items_count', 'mean'),
        average_rating=('customer_rating', 'mean'),
        average_delay_minutes=('delay_minutes', 'mean'),
        delayed_order_ratio=('is_delayed', 'mean'),
        inaccurate_order_ratio=('is_inaccurate', 'mean'),
        promo_order_ratio=('is_promo_used', 'mean'),
        unique_categories_ordered=('vendor_category', 'nunique'),
        latest_order_date=('order_date', 'max')
    ).reset_index()
    
    # Join customer demographic and signup features
    cust_agg = pd.merge(cust_agg, customers, on='customer_id', how='inner')
    
    # Engineer Customer-level Features
    # Active lifespan
    cust_agg['active_lifespan_days'] = (cust_agg['latest_order_date'] - cust_agg['signup_date']).dt.days
    
    # Recency and Churn flag (90 days of inactivity)
    cust_agg['days_since_latest_order'] = (max_dataset_date - cust_agg['latest_order_date']).dt.days
    cust_agg['is_churned'] = (cust_agg['days_since_latest_order'] > 90).astype(int)
    
    # 4. Engineer Early Experience (First 3 Orders) Features
    print("Engineering early experience features (First 3 Orders)...")
    first_3_orders = master_orders[master_orders['order_seq'] <= 3]
    first_3_grouped = first_3_orders.groupby('customer_id')
    
    first_3_agg = first_3_grouped.agg(
        first_3_delayed_ratio=('is_delayed', 'mean'),
        first_3_inaccurate_ratio=('is_inaccurate', 'mean'),
        first_3_rating_avg=('customer_rating', 'mean')
    ).reset_index()
    
    # Merge early experience metrics
    cust_features = pd.merge(cust_agg, first_3_agg, on='customer_id', how='left')
    
    # Fill early experience missing values with general averages (in case they have 0 reviews or orders)
    cust_features['first_3_delayed_ratio'] = cust_features['first_3_delayed_ratio'].fillna(cust_features['delayed_order_ratio'])
    cust_features['first_3_inaccurate_ratio'] = cust_features['first_3_inaccurate_ratio'].fillna(cust_features['inaccurate_order_ratio'])
    cust_features['first_3_rating_avg'] = cust_features['first_3_rating_avg'].fillna(cust_features['average_rating'])
    
    # Save customer features dataset
    customer_features_path = 'data/interim/customer_features.csv'
    cust_features.to_csv(customer_features_path, index=False)
    print(f"Saved customer features: {cust_features.shape} to {customer_features_path}")
    print("Data preparation and feature engineering successfully completed!")

if __name__ == '__main__':
    prepare_datasets()
