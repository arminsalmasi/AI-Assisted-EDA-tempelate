import os
import pandas as pd
import numpy as np

def prepare_datasets():
    # 1. Load Raw Datasets
    print("Loading raw datasets...")
    customers_path = 'data/raw/users_profile.csv'
    orders_path = 'data/raw/transactions_log.csv'
    deliveries_path = 'data/raw/fulfillments_log.csv'
    
    customers = pd.read_csv(customers_path)
    orders = pd.read_csv(orders_path)
    deliveries = pd.read_csv(deliveries_path)
    
    # Convert dates to datetime
    customers['registration_date'] = pd.to_datetime(customers['registration_date'])
    orders['transaction_date'] = pd.to_datetime(orders['transaction_date'])
    
    # 2. Build Master Order-level Dataset
    print("Building master order-level dataset...")
    # Merge orders and deliveries (1-to-1 mapping on transaction_id)
    orders_deliveries = pd.merge(orders, deliveries, on='transaction_id', how='inner')
    
    # Merge with customers on user_id
    master_orders = pd.merge(orders_deliveries, customers, on='user_id', how='inner')
    
    # Sort chronologically by user and date
    master_orders = master_orders.sort_values(by=['user_id', 'transaction_date', 'transaction_id']).reset_index(drop=True)
    
    # Calculate chronological sequence of orders for each user
    master_orders['order_seq'] = master_orders.groupby('user_id').cumcount() + 1
    master_orders['customer_order_number'] = master_orders['order_seq']
    
    # Next order date tracking
    master_orders['next_order_date'] = master_orders.groupby('user_id')['transaction_date'].shift(-1)
    
    # Calculate gap to next order (in days)
    master_orders['days_to_next_order'] = (master_orders['next_order_date'] - master_orders['transaction_date']).dt.days
    
    # Return within window indicators (default to 0 if they didn't place a next order)
    master_orders['returned_within_30d'] = (master_orders['days_to_next_order'] <= 30).astype(int)
    master_orders['returned_within_60d'] = (master_orders['days_to_next_order'] <= 60).astype(int)
    master_orders['returned_within_90d'] = (master_orders['days_to_next_order'] <= 90).astype(int)
    
    # Fill return indicators as 0 for the last order of users (where days_to_next_order is NaN)
    master_orders.loc[master_orders['days_to_next_order'].isna(), ['returned_within_30d', 'returned_within_60d', 'returned_within_90d']] = 0
    
    # Basic engineered features
    master_orders['is_late'] = (master_orders['late_status'] == 'Late').astype(int)
    master_orders['is_inaccurate'] = master_orders['accuracy_status'].isin(['Incomplete', 'Incorrect']).astype(int)
    master_orders['days_since_registration'] = (master_orders['transaction_date'] - master_orders['registration_date']).dt.days
    master_orders['customer_tenure_at_order_days'] = master_orders['days_since_registration']
    master_orders['net_amount_usd'] = master_orders['gross_amount_usd'] - master_orders['coupon_discount_usd']
    master_orders['is_coupon_applied'] = (master_orders['coupon_applied'] == 'Yes').astype(int)
    
    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # Save master order-level dataset
    master_orders_path = 'data/processed/master_orders.csv'
    master_orders.to_csv(master_orders_path, index=False)
    print(f"Saved master orders: {master_orders.shape} to {master_orders_path}")
    
    # 3. Build Aggregated Customer-level Dataset
    print("Building customer-level aggregated dataset...")
    
    # Timeline metadata for Churn and Tenure calculations
    max_dataset_date = master_orders['transaction_date'].max()
    print(f"Max date in dataset: {max_dataset_date.strftime('%Y-%m-%d')}")
    
    # Get first and last order details per user
    first_orders = master_orders[master_orders['customer_order_number'] == 1].copy()
    last_orders = master_orders.loc[master_orders.groupby('user_id')['customer_order_number'].idxmax()].copy()
    
    # Aggregations using group by
    grouped = master_orders.groupby('user_id')
    
    # Compute counts for specific vendor categories
    eatery_orders = grouped.apply(lambda df: (df['merchant_category'] == 'Eatery').sum(), include_groups=False)
    supermarket_orders = grouped.apply(lambda df: (df['merchant_category'] == 'Supermarket').sum(), include_groups=False)
    medical_orders = grouped.apply(lambda df: (df['merchant_category'] == 'Medical').sum(), include_groups=False)
    boutique_orders = grouped.apply(lambda df: (df['merchant_category'] == 'Boutique').sum(), include_groups=False)
    
    # Compute counts for specific delivery types
    instant_orders = grouped.apply(lambda df: (df['fulfillment_type'] == 'Instant').sum(), include_groups=False)
    planned_orders = grouped.apply(lambda df: (df['fulfillment_type'] == 'Planned').sum(), include_groups=False)
    priority_orders = grouped.apply(lambda df: (df['fulfillment_type'] == 'Priority').sum(), include_groups=False)
    
    # Compute counts for delivery success and accuracy
    prompt_deliveries = grouped.apply(lambda df: (df['late_status'] == 'Prompt').sum(), include_groups=False)
    late_deliveries = grouped.apply(lambda df: (df['late_status'] == 'Late').sum(), include_groups=False)
    
    accurate_fulfillments = grouped.apply(lambda df: (df['accuracy_status'] == 'Accurate').sum(), include_groups=False)
    incomplete_fulfillments = grouped.apply(lambda df: (df['accuracy_status'] == 'Incomplete').sum(), include_groups=False)
    incorrect_fulfillments = grouped.apply(lambda df: (df['accuracy_status'] == 'Incorrect').sum(), include_groups=False)
    
    # General aggregation
    cust_agg = grouped.agg(
        frequency=('transaction_id', 'count'),
        total_spend=('gross_amount_usd', 'sum'),
        total_net_spend=('net_amount_usd', 'sum'),
        total_discount=('coupon_discount_usd', 'sum'),
        average_order_value=('gross_amount_usd', 'mean'),
        average_items_count=('quantity_items', 'mean'),
        average_rating=('user_rating', 'mean'),
        average_delay_minutes=('late_minutes', 'mean'),
        delayed_order_ratio=('is_late', 'mean'),
        inaccurate_order_ratio=('is_inaccurate', 'mean'),
        promo_order_ratio=('is_coupon_applied', 'mean'),
        promo_orders_count=('is_coupon_applied', 'sum'),
        unique_vendors=('merchant_id', 'nunique'),
        unique_vendor_categories=('merchant_category', 'nunique'),
        unique_delivery_types=('fulfillment_type', 'nunique'),
        max_delay_minutes=('late_minutes', 'max')
    ).reset_index()
    
    # Map calculated counts
    cust_agg['eatery_orders'] = cust_agg['user_id'].map(eatery_orders)
    cust_agg['supermarket_orders'] = cust_agg['user_id'].map(supermarket_orders)
    cust_agg['medical_orders'] = cust_agg['user_id'].map(medical_orders)
    cust_agg['boutique_orders'] = cust_agg['user_id'].map(boutique_orders)
    
    cust_agg['instant_orders'] = cust_agg['user_id'].map(instant_orders)
    cust_agg['planned_orders'] = cust_agg['user_id'].map(planned_orders)
    cust_agg['priority_orders'] = cust_agg['user_id'].map(priority_orders)
    
    cust_agg['prompt_deliveries'] = cust_agg['user_id'].map(prompt_deliveries)
    cust_agg['late_deliveries'] = cust_agg['user_id'].map(late_deliveries)
    
    cust_agg['accurate_fulfillments'] = cust_agg['user_id'].map(accurate_fulfillments)
    cust_agg['incomplete_fulfillments'] = cust_agg['user_id'].map(incomplete_fulfillments)
    cust_agg['incorrect_fulfillments'] = cust_agg['user_id'].map(incorrect_fulfillments)
    
    # Compute rates
    cust_agg['prompt_delivery_rate'] = (cust_agg['prompt_deliveries'] / cust_agg['frequency']).round(4)
    cust_agg['accurate_fulfillment_rate'] = (cust_agg['accurate_fulfillments'] / cust_agg['frequency']).round(4)
    
    # Flags
    cust_agg['repeat_customer_flag'] = (cust_agg['frequency'] > 1).astype(int)
    cust_agg['multi_category_user_flag'] = (cust_agg['unique_vendor_categories'] > 1).astype(int)
    cust_agg['multi_delivery_type_user_flag'] = (cust_agg['unique_delivery_types'] > 1).astype(int)
    
    # Join customer demographic features
    cust_agg = pd.merge(cust_agg, customers, on='user_id', how='inner')
    
    # Map first and last order dates
    first_order_dates = first_orders.set_index('user_id')['transaction_date']
    last_order_dates = last_orders.set_index('user_id')['transaction_date']
    
    cust_agg['first_order_date'] = cust_agg['user_id'].map(first_order_dates)
    cust_agg['last_order_date'] = cust_agg['user_id'].map(last_order_dates)
    
    # Lifespan and recency calculations
    cust_agg['active_lifespan_days'] = (cust_agg['last_order_date'] - cust_agg['registration_date']).dt.days
    cust_agg['active_span_days'] = (cust_agg['last_order_date'] - cust_agg['first_order_date']).dt.days
    cust_agg['tenure_days_at_dataset_end'] = (max_dataset_date - cust_agg['registration_date']).dt.days
    cust_agg['days_since_latest_order'] = (max_dataset_date - cust_agg['last_order_date']).dt.days
    cust_agg['is_churned'] = (cust_agg['days_since_latest_order'] > 90).astype(int)
    
    # Early experience metrics (First 3 Orders)
    print("Engineering early experience features (First 3 Orders)...")
    first_3_orders = master_orders[master_orders['order_seq'] <= 3]
    first_3_grouped = first_3_orders.groupby('user_id')
    
    first_3_agg = first_3_grouped.agg(
        first_3_delayed_ratio=('is_late', 'mean'),
        first_3_inaccurate_ratio=('is_inaccurate', 'mean'),
        first_3_rating_avg=('user_rating', 'mean')
    ).reset_index()
    
    cust_features = pd.merge(cust_agg, first_3_agg, on='user_id', how='left')
    
    # Fill early experience missing values with general averages
    cust_features['first_3_delayed_ratio'] = cust_features['first_3_delayed_ratio'].fillna(cust_features['delayed_order_ratio'])
    cust_features['first_3_inaccurate_ratio'] = cust_features['first_3_inaccurate_ratio'].fillna(cust_features['inaccurate_order_ratio'])
    cust_features['first_3_rating_avg'] = cust_features['first_3_rating_avg'].fillna(cust_features['average_rating'])
    
    # 4. Integrate First-Order return tracking with right-censoring logic
    print("Engineering first-order return outcomes with right-censoring...")
    first_orders_return = first_orders.set_index('user_id')[['returned_within_30d', 'returned_within_60d', 'returned_within_90d', 'transaction_date']]
    
    cust_features = pd.merge(cust_features, first_orders_return, on='user_id', how='left')
    
    # Rename columns to match Codex output
    cust_features = cust_features.rename(columns={
        'returned_within_30d': 'returned_after_first_order_30d',
        'returned_within_60d': 'returned_after_first_order_60d',
        'returned_within_90d': 'returned_after_first_order_90d'
    })
    
    # Calculate observation window eligibility flags (from first order date to dataset end date)
    days_since_first_order = (max_dataset_date - cust_features['first_order_date']).dt.days
    cust_features['full_30d_observation_flag'] = (days_since_first_order >= 30).astype(int)
    cust_features['full_60d_observation_flag'] = (days_since_first_order >= 60).astype(int)
    cust_features['full_90d_observation_flag'] = (days_since_first_order >= 90).astype(int)
    
    # Apply right-censoring: set return flags to NaN if they did not return and look-forward window was not complete
    cust_features.loc[(cust_features['returned_after_first_order_30d'] == 0) & (cust_features['full_30d_observation_flag'] == 0), 'returned_after_first_order_30d'] = np.nan
    cust_features.loc[(cust_features['returned_after_first_order_60d'] == 0) & (cust_features['full_60d_observation_flag'] == 0), 'returned_after_first_order_60d'] = np.nan
    cust_features.loc[(cust_features['returned_after_first_order_90d'] == 0) & (cust_features['full_90d_observation_flag'] == 0), 'returned_after_first_order_90d'] = np.nan
    
    # Convert first_order_date and last_order_date to standard string ISO format for CSV consistency
    cust_features['first_order_date'] = cust_features['first_order_date'].dt.strftime('%Y-%m-%d')
    cust_features['last_order_date'] = cust_features['last_order_date'].dt.strftime('%Y-%m-%d')
    
    # Save customer features dataset
    customer_features_path = 'data/processed/customer_features.csv'
    cust_features.to_csv(customer_features_path, index=False)
    print(f"Saved customer features: {cust_features.shape} to {customer_features_path}")
    print("Data preparation and feature engineering successfully completed!")

if __name__ == '__main__':
    prepare_datasets()
