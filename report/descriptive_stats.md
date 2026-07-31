# DESCRIPTIVE ANALYSIS REPORT

This report provides summary statistics for the feature-engineered datasets at the order and customer level.

## 1. Order-Level Transaction Statistics
Summary statistics based on all transactions in the dataset:

|                     |   count |     mean |      std |   min |   25% |   median |   75% |    max |
|:--------------------|--------:|---------:|---------:|------:|------:|---------:|------:|-------:|
| quantity_items      |   73022 |  6.25524 |  6.02598 |  1    |  2    |     4    |  7    |  24    |
| gross_amount_usd    |   73022 | 51.2626  | 32.0553  |  7.63 | 27.51 |    41.84 | 67.27 | 345.12 |
| coupon_discount_usd |   73022 |  4.22296 |  7.29853 |  0    |  0    |     0    |  6.3  |  80.07 |
| net_amount_usd      |   73022 | 47.0396  | 30.2091  |  5.26 | 24.87 |    38.25 | 61.43 | 345.12 |
| late_minutes        |   73022 |  5.70631 | 10.4752  |  0    |  0    |     0    |  6    | 137    |
| user_rating         |   73022 |  3.94359 |  1.0767  |  1    |  3    |     4    |  5    |   5    |

## 2. Customer-Level Aggregated Statistics
Summary statistics based on customers aggregated from registration date to latest transaction:

|                         |   count |        mean |        std |   min |        25% |      median |         75% |     max |
|:------------------------|--------:|------------:|-----------:|------:|-----------:|------------:|------------:|--------:|
| frequency               |    5000 |  14.6044    |  13.1023   |  1    |   5        |  11         |   20        |  126    |
| total_spend             |    5000 | 748.659     | 678.523    | 11.72 | 267.067    | 546.125     | 1017.47     | 6599.01 |
| total_net_spend         |    5000 | 686.985     | 620.233    |  8.85 | 244.648    | 501.89      |  927.533    | 6193.28 |
| total_discount          |    5000 |  61.6738    |  77.6548   |  0    |  11.43     |  35.86      |   82.4425   |  749.77 |
| average_order_value     |    5000 |  51.4578    |  12.771    | 11.72 |  44.389    |  50.6138    |   57.0907   |  181.71 |
| average_items_count     |    5000 |   6.27102   |   2.42505  |  1    |   4.8      |   6.08333   |    7.36917  |   24    |
| average_rating          |    5000 |   3.80795   |   0.727049 |  1    |   3.33333  |   3.94202   |    4.36842  |    5    |
| average_delay_minutes   |    5000 |   6.14714   |   4.66611  |  0    |   3.2      |   5.33333   |    8        |   57    |
| delayed_order_ratio     |    5000 |   0.46215   |   0.201272 |  0    |   0.333333 |   0.454545  |    0.557568 |    1    |
| inaccurate_order_ratio  |    5000 |   0.0783864 |   0.102704 |  0    |   0        |   0.0555556 |    0.117647 |    1    |
| promo_order_ratio       |    5000 |   0.396289  |   0.26446  |  0    |   0.2      |   0.383484  |    0.583333 |    1    |
| active_lifespan_days    |    5000 | 207.992     | 185.379    |  0    |  63        | 151         |  302        |  831    |
| days_since_latest_order |    5000 | 241.928     | 225.369    |  0    |  53.75     | 145         |  408        |  869    |

## 3. Categorical Distributions & Proportions

### A. Customer Churn Rate (90-Day Inactivity Window)
|         |   Count |   Percentage (%) |
|:--------|--------:|-----------------:|
| Churned |    2933 |            58.66 |
| Active  |    2067 |            41.34 |

### B. Preferred Devices
| device_type   |   Count |   Percentage (%) |
|:--------------|--------:|-----------------:|
| App           |    3863 |            77.26 |
| Website       |    1137 |            22.74 |

### C. Customer Demographics Segment
| account_segment   |   Count |   Percentage (%) |
|:------------------|--------:|-----------------:|
| Standard          |    2905 |            58.1  |
| Elite             |    1053 |            21.06 |
| Intro             |    1042 |            20.84 |

### D. Orders by Vendor Category
| merchant_category   |   Count |   Percentage (%) |
|:--------------------|--------:|-----------------:|
| Eatery              |   36580 |         50.0945  |
| Supermarket         |   21909 |         30.0033  |
| Medical             |    7293 |          9.9874  |
| Boutique            |    7240 |          9.91482 |

### E. Orders by Delivery Type
| fulfillment_type   |   Count |   Percentage (%) |
|:-------------------|--------:|-----------------:|
| Instant            |   43981 |          60.2298 |
| Planned            |   18145 |          24.8487 |
| Priority           |   10896 |          14.9215 |

### F. Customers by State
| location_state   |   Count |   Percentage (%) |
|:-----------------|--------:|-----------------:|
| TX               |    1319 |            26.38 |
| CA               |    1280 |            25.6  |
| AZ               |     452 |             9.04 |
| IL               |     398 |             7.96 |
| MA               |     395 |             7.9  |
| NY               |     391 |             7.82 |
| PA               |     388 |             7.76 |
| WA               |     377 |             7.54 |

