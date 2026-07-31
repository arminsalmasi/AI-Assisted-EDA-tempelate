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
            'order_id', 'customer_id', 'order_date', 'is_delayed', 
            'is_inaccurate', 'days_since_signup', 'net_value_usd', 
            'is_promo_used', 'order_seq'
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing required column: {col}")
        
        # Check null values (none expected)
        self.assertEqual(df[required_cols].isnull().sum().sum(), 0, "Null values found in master_orders engineered columns!")

    def test_customer_features_schema(self):
        df = pd.read_csv(self.customer_features_path)
        print(f"[PASS] Read customer_features.csv successfully: shape {df.shape}")
        
        # Check required columns
        required_cols = [
            'customer_id', 'frequency', 'total_spend', 'total_net_spend', 
            'average_order_value', 'delayed_order_ratio', 'inaccurate_order_ratio', 
            'active_lifespan_days', 'days_since_latest_order', 'is_churned',
            'first_3_delayed_ratio', 'first_3_inaccurate_ratio', 'first_3_rating_avg'
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Missing required column: {col}")
            
        # Check null values
        self.assertEqual(df[required_cols].isnull().sum().sum(), 0, "Null values found in customer_features engineered columns!")
        
        # Verify churn flags are binary
        self.assertTrue(set(df['is_churned'].unique()).issubset({0, 1}), "is_churned values must be binary!")

if __name__ == '__main__':
    unittest.main()
