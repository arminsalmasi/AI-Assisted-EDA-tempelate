# DESCRIPTIVE ANALYSIS REPORT

This report provides summary statistics for the feature-engineered datasets at the order and customer level.

## 1. Order-Level Transaction Statistics
Summary statistics based on all 73,022 transactions in the dataset:

|                     |   count |     mean |      std |   min |   25% |   median |     75% |    max |
|:--------------------|--------:|---------:|---------:|------:|------:|---------:|--------:|-------:|
| items_count         |   73022 |  6.25524 |  6.02598 |  1    |  2    |    4     |  7      |  24    |
| order_value_usd     |   73022 | 51.247   | 31.8347  |  8.08 | 27.59 |   41.885 | 67.21   | 342.21 |
| discount_amount_usd |   73022 |  3.17851 |  5.37417 |  0    |  0    |    0     |  4.84   |  55.8  |
| net_value_usd       |   73022 | 48.0685  | 30.2705  |  6.18 | 25.67 |   39.23  | 62.9375 | 342.21 |
| delay_minutes       |   73022 |  5.00848 | 10.4397  |  0    |  0    |    0     |  0      | 130    |
| customer_rating     |   73022 |  3.97927 |  1.04457 |  1    |  3    |    4     |  5      |   5    |

## 2. Customer-Level Aggregated Statistics
Summary statistics based on 5,000 customers aggregated from signup date to latest transaction:

|                         |   count |        mean |        std |   min |        25% |      median |         75% |     max |
|:------------------------|--------:|------------:|-----------:|------:|-----------:|------------:|------------:|--------:|
| frequency               |    5000 |  14.6044    |  13.1023   |  1    |   5        |  11         |   20        |  126    |
| total_spend             |    5000 | 748.431     | 678.117    | 12.39 | 265.188    | 544.405     | 1022.04     | 6595.68 |
| total_net_spend         |    5000 | 702.011     | 633.851    |  9.8  | 250.162    | 515.505     |  943.352    | 6188.54 |
| total_discount          |    5000 |  46.4203    |  58.0844   |  0    |   8.99     |  27.22      |   62.04     |  566.57 |
| average_order_value     |    5000 |  51.4624    |  12.7194   | 12.39 |  44.4138   |  50.554     |   57.1752   |  167.46 |
| average_items_count     |    5000 |   6.27102   |   2.42505  |  1    |   4.8      |   6.08333   |    7.36917  |   24    |
| average_rating          |    5000 |   3.83322   |   0.745302 |  1    |   3.34582  |   4         |    4.42424  |    5    |
| average_delay_minutes   |    5000 |   5.45148   |   4.67735  |  0    |   2.5      |   4.71714   |    7.33333  |   66    |
| delayed_order_ratio     |    5000 |   0.263627  |   0.187751 |  0    |   0.142857 |   0.25      |    0.347826 |    1    |
| inaccurate_order_ratio  |    5000 |   0.0783864 |   0.102704 |  0    |   0        |   0.0555556 |    0.117647 |    1    |
| promo_order_ratio       |    5000 |   0.396289  |   0.26446  |  0    |   0.2      |   0.383484  |    0.583333 |    1    |
| active_lifespan_days    |    5000 | 207.992     | 185.379    |  0    |  63        | 151         |  302        |  831    |
| days_since_latest_order |    5000 | 212.131     | 224.868    |  0    |  18        | 114         |  377        |  820    |

## 3. Categorical Distributions & Proportions

### A. Customer Churn Rate (90-Day Inactivity Window)
|         |   Count |   Percentage (%) |
|:--------|--------:|-----------------:|
| Churned |    2650 |               53 |
| Active  |    2350 |               47 |

### B. Preferred Devices
| preferred_device   |   Count |   Percentage (%) |
|:-------------------|--------:|-----------------:|
| Mobile App         |    3863 |            77.26 |
| Web                |    1137 |            22.74 |

### C. Customer Demographics Segment
| customer_segment   |   Count |   Percentage (%) |
|:-------------------|--------:|-----------------:|
| Regular            |    2905 |            58.1  |
| Premium            |    1053 |            21.06 |
| New                |    1042 |            20.84 |

### D. Orders by Vendor Category
| vendor_category   |   Count |   Percentage (%) |
|:------------------|--------:|-----------------:|
| Restaurant        |   36580 |         50.0945  |
| Grocery           |   21909 |         30.0033  |
| Pharmacy          |    7293 |          9.9874  |
| Retail            |    7240 |          9.91482 |

### E. Orders by Delivery Type
| delivery_type   |   Count |   Percentage (%) |
|:----------------|--------:|-----------------:|
| On-Demand       |   43981 |          60.2298 |
| Scheduled       |   18145 |          24.8487 |
| Express         |   10896 |          14.9215 |

### F. Customers by State
| state   |   Count |   Percentage (%) |
|:--------|--------:|-----------------:|
| TX      |    1319 |            26.38 |
| CA      |    1280 |            25.6  |
| AZ      |     452 |             9.04 |
| IL      |     398 |             7.96 |
| MA      |     395 |             7.9  |
| NY      |     391 |             7.82 |
| PA      |     388 |             7.76 |
| WA      |     377 |             7.54 |

