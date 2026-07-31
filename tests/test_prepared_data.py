import unittest
import os
import pandas as pd

class TestPreparedData(unittest.TestCase):
    def setUp(self):
        self.master_orders_path = 'data/processed/master_orders.csv'
        self.customer_features_path = 'data/processed/customer_features.csv'

    def test_files_exist(self):
        self.assertTrue(os.path.exists(self.master_orders_path), "master_orders.csv not found!")
        self.assertTrue(os.path.exists(self.customer_features_path), "customer_features.csv not found!")

    def test_master_orders_schema(self):
        df = pd.read_csv(self.master_orders_path)
        print(f"\n[PASS] Read master_orders.csv successfully: shape {df.shape}")
        
        # Check required columns
        required_cols = [
            'transaction_id', 'user_id', 'transaction_date', 'is_late', 
            'is_inaccurate', 'days_since_registration', 'net_amount_usd', 
            'is_coupon_applied', 'order_seq', 'customer_order_number',
            'next_order_date', 'days_to_next_order',
            'returned_within_30d', 'returned_within_60d', 'returned_within_90d',
            'customer_tenure_at_order_days'
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing required column: {col}")
        
        # Check null values on subset (next_order_date and days_to_next_order can be null for last orders)
        non_null_cols = [
            'transaction_id', 'user_id', 'transaction_date', 'is_late', 
            'is_inaccurate', 'days_since_registration', 'net_amount_usd', 
            'is_coupon_applied', 'order_seq', 'customer_order_number',
            'returned_within_30d', 'returned_within_60d', 'returned_within_90d',
            'customer_tenure_at_order_days'
        ]
        self.assertEqual(df[non_null_cols].isnull().sum().sum(), 0, "Null values found in master_orders engineered columns!")

    def test_customer_features_schema(self):
        df = pd.read_csv(self.customer_features_path)
        print(f"[PASS] Read customer_features.csv successfully: shape {df.shape}")
        
        # Check required columns
        required_cols = [
            'user_id', 'frequency', 'total_spend', 'total_net_spend', 
            'average_order_value', 'delayed_order_ratio', 'inaccurate_order_ratio', 
            'active_lifespan_days', 'days_since_latest_order', 'is_churned',
            'first_3_delayed_ratio', 'first_3_inaccurate_ratio', 'first_3_rating_avg',
            'repeat_customer_flag', 'tenure_days_at_dataset_end', 'first_order_date',
            'last_order_date', 'active_span_days', 'promo_orders_count',
            'unique_vendors', 'unique_vendor_categories', 'unique_delivery_types',
            'multi_category_user_flag', 'multi_delivery_type_user_flag',
            'eatery_orders', 'supermarket_orders', 'medical_orders', 'boutique_orders',
            'instant_orders', 'planned_orders', 'priority_orders',
            'prompt_deliveries', 'late_deliveries', 'prompt_delivery_rate',
            'accurate_fulfillments', 'incomplete_fulfillments', 'incorrect_fulfillments', 'accurate_fulfillment_rate',
            'returned_after_first_order_30d', 'returned_after_first_order_60d', 'returned_after_first_order_90d',
            'full_30d_observation_flag', 'full_60d_observation_flag', 'full_90d_observation_flag'
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing required column: {col}")
            
        # Check null values on subset (returned_after_first_order_30d etc. can have NaNs due to censoring)
        non_null_cols = [
            'user_id', 'frequency', 'total_spend', 'total_net_spend', 
            'average_order_value', 'delayed_order_ratio', 'inaccurate_order_ratio', 
            'active_lifespan_days', 'days_since_latest_order', 'is_churned',
            'first_3_delayed_ratio', 'first_3_inaccurate_ratio', 'first_3_rating_avg',
            'repeat_customer_flag', 'tenure_days_at_dataset_end', 'first_order_date',
            'last_order_date', 'active_span_days', 'promo_orders_count',
            'unique_vendors', 'unique_vendor_categories', 'unique_delivery_types',
            'multi_category_user_flag', 'multi_delivery_type_user_flag',
            'eatery_orders', 'supermarket_orders', 'medical_orders', 'boutique_orders',
            'instant_orders', 'planned_orders', 'priority_orders',
            'prompt_deliveries', 'late_deliveries', 'prompt_delivery_rate',
            'accurate_fulfillments', 'incomplete_fulfillments', 'incorrect_fulfillments', 'accurate_fulfillment_rate',
            'full_30d_observation_flag', 'full_60d_observation_flag', 'full_90d_observation_flag'
        ]
        self.assertEqual(df[non_null_cols].isnull().sum().sum(), 0, "Null values found in customer_features non-censored columns!")

if __name__ == '__main__':
    unittest.main()
