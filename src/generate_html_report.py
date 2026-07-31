import base64
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "report"
OUTPUT_PATH = REPORT_DIR / "flash_delivery_retention_report.html"

def get_image_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"

def load_text_file(path):
    if not os.path.exists(path):
        return "File not found."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def compile_report():
    print("Compiling HTML dashboard report...")
    
    # 1. Base64 encode all figures
    figures = {
        # Univariate
        "uni_val": get_image_base64(REPORT_DIR / "figures" / "univariate_order_value.png"),
        "uni_items": get_image_base64(REPORT_DIR / "figures" / "univariate_items_discount.png"),
        "uni_delays": get_image_base64(REPORT_DIR / "figures" / "univariate_delays_cdf.png"),
        "uni_comp": get_image_base64(REPORT_DIR / "figures" / "univariate_promised_actual_comp.png"),
        "uni_spend": get_image_base64(REPORT_DIR / "figures" / "univariate_customer_frequency_spend.png"),
        "uni_life": get_image_base64(REPORT_DIR / "figures" / "univariate_customer_lifespan_recency.png"),
        "uni_demo": get_image_base64(REPORT_DIR / "figures" / "univariate_customer_demographics.png"),
        "uni_loc": get_image_base64(REPORT_DIR / "figures" / "univariate_customer_locations.png"),
        "uni_cohort_rates": get_image_base64(REPORT_DIR / "figures" / "univariate_cohort_return_rates.png"),
        "uni_cohort_comp": get_image_base64(REPORT_DIR / "figures" / "univariate_cohort_comparison.png"),
        # Bivariate
        "bi_status": get_image_base64(REPORT_DIR / "figures" / "bivariate_status_retention.png"),
        "bi_rating": get_image_base64(REPORT_DIR / "figures" / "bivariate_rating_retention.png"),
        "bi_promo": get_image_base64(REPORT_DIR / "figures" / "bivariate_promo_retention.png"),
        "bi_vs_spend": get_image_base64(REPORT_DIR / "figures" / "bivariate_promo_vs_spend.png"),
        "bi_breadth": get_image_base64(REPORT_DIR / "figures" / "bivariate_usage_breadth_vs_churn.png"),
        "bi_demo": get_image_base64(REPORT_DIR / "figures" / "bivariate_demographics_vs_churn.png"),
        "bi_delivery_churn": get_image_base64(REPORT_DIR / "figures" / "bivariate_delivery_experience_vs_churn.png"),
        "bi_spend_churn": get_image_base64(REPORT_DIR / "figures" / "bivariate_spend_behavior_vs_churn.png"),
        # Multivariate
        "multi_corr": get_image_base64(REPORT_DIR / "figures" / "multivariate_correlation_matrix.png"),
        "multi_scatter": get_image_base64(REPORT_DIR / "figures" / "multivariate_delay_rating_scatter.png"),
        "multi_promo": get_image_base64(REPORT_DIR / "figures" / "multivariate_segment_promo_churn.png")
    }
    
    # 2. Load statistical text files
    descriptive_stats_md = load_text_file(REPORT_DIR / "descriptive_stats.md")
    hypothesis_testing_results_txt = load_text_file(REPORT_DIR / "hypothesis_testing_results.txt")
    
    # Simple markdown parser for descriptive stats tables in html
    import markdown
    descriptive_html = markdown.markdown(descriptive_stats_md, extensions=['tables'])
    
    # Create HTML structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlashDelivery Customer Retention Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-color: #f1f5f9;
            --text-muted: #94a3b8;
            --accent-color: #0ea5e9;
            --accent-glow: rgba(14, 165, 233, 0.4);
            --border-color: rgba(255, 255, 255, 0.08);
            --success-color: #10b981;
            --warning-color: #f59e0b;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 2rem;
        }}
        
        h1, h2, h3, h4 {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            margin-bottom: 1rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 50%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        header p {{
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* Navigation Tabs */
        .tabs {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2.5rem;
            flex-wrap: wrap;
        }}
        
        .tab-btn {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 0.8rem 1.5rem;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .tab-btn:hover {{
            background: rgba(14, 165, 233, 0.1);
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }}
        
        .tab-btn.active {{
            background: var(--accent-color);
            color: #0f172a;
            border-color: var(--accent-color);
            box-shadow: 0 0 20px var(--accent-glow);
        }}
        
        /* Tab Contents */
        .tab-content {{
            display: none;
            opacity: 0;
            transition: opacity 0.4s ease;
        }}
        
        .tab-content.active {{
            display: block;
            opacity: 1;
        }}
        
        /* Grid Layout */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Cards */
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-4px);
        }}
        
        .card.full-width {{
            grid-column: 1 / -1;
        }}
        
        .card h2 {{
            font-size: 1.8rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            color: var(--accent-color);
        }}
        
        .card h3 {{
            font-size: 1.3rem;
            color: #38bdf8;
            margin-top: 1rem;
        }}
        
        .card p {{
            margin-bottom: 1rem;
            color: #e2e8f0;
            font-size: 1.05rem;
        }}
        
        .card p.desc {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: -0.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .card img {{
            width: 100%;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-top: 0.5rem;
            background: rgba(0, 0, 0, 0.2);
        }}
        
        /* Lists formatting */
        .card ul, .card ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
            color: #cbd5e1;
        }}
        
        .card li {{
            margin-bottom: 0.5rem;
        }}
        
        /* Tables in Markdown */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }}
        
        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            background-color: rgba(255, 255, 255, 0.05);
            font-family: 'Outfit', sans-serif;
            color: var(--accent-color);
            font-weight: 600;
        }}
        
        tr:hover {{
            background: rgba(255, 255, 255, 0.02);
        }}
        
        /* Statistical Log Output */
        pre {{
            background: #020617;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            color: #38bdf8;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            white-space: pre-wrap;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>FlashDelivery Customer Retention Dashboard</h1>
            <p>Unbiased Cohort Retention, Operational Experience & Hypothesis Testing Analysis</p>
        </header>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab(event, 'summary')">Executive Summary</button>
            <button class="tab-btn" onclick="openTab(event, 'univariate')">Univariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'bivariate')">Bivariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'multivariate')">Multivariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'stats')">Hypothesis Testing</button>
            <button class="tab-btn" onclick="openTab(event, 'desc')">Descriptive Statistics</button>
        </div>
        
        <!-- EXECUTIVE SUMMARY -->
        <div id="summary" class="tab-content active">
            <div class="card full-width">
                <h2>1. Business Context & Problem Statement</h2>
                <p>FlashDelivery is an online multi-category delivery platform connecting customers with restaurants, grocery stores, and pharmacies. The business operates across multiple cities offering on-demand, scheduled, and express delivery speeds. In a highly competitive market where customer acquisition costs (CAC) significantly outpace retention costs, FlashDelivery is facing a critical leak: <strong>53% of its active customer base has churned</strong> (showing no transactions in their final 90 days).</p>
                <p>Maintaining customer retention is critical to long-term profitability, customer lifetime value (CLV), and sustainable unit economics. This exploratory data analysis (EDA) and statistical testing investigate the drivers of customer churn and repeat purchasing to provide data-driven recommendations.</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>2. Data Overview & Profiling</h2>
                    <p>The analysis is conducted on three raw datasets consolidated into processed analytical tables:</p>
                    <ul>
                        <li><strong>users_profile.csv</strong>: 5,000 customers (demographics, device type, registration details).</li>
                        <li><strong>transactions_log.csv</strong>: 73,022 orders (merchant category, basket size, USD spend, coupons applied).</li>
                        <li><strong>fulfillments_log.csv</strong>: 73,022 delivery records (estimated vs actual times, delay minutes, content accuracy, star ratings).</li>
                    </ul>
                    <p>Datasets were merged into a master order-level table and customer-level feature matrices adjusted for right-censoring to prevent observation-window bias.</p>
                </div>
                
                <div class="card">
                    <h2>3. Actionable Recommendations</h2>
                    <ol style="margin-left: 1.5rem; margin-top: 0.5rem;">
                        <li style="margin-bottom: 0.5rem;"><strong>App Migration Campaign</strong>: Proactively transition web-based users to the mobile app (where churn is significantly lower) via download incentives and push notifications.</li>
                        <li style="margin-bottom: 0.5rem;"><strong>First-Order Service Guarantee</strong>: Prioritize courier dispatch and contents accuracy checks on a customer's first three orders. First-impression delays are permanent retention killers.</li>
                        <li style="margin-bottom: 0.5rem;"><strong>Cross-Category Cross-Selling</strong>: Implement recommendation engines to cross-promote services (e.g., offer grocery credits to restaurant diners). Category expansion is our strongest loyalty shield.</li>
                        <li style="margin-bottom: 0.5rem;"><strong>Promo Spending Optimization</strong>: Shift discount budgets away from high-promo deal-seekers (whose churn rates remain elevated) and invest in service reliability and loyalty points.</li>
                    </ol>
                </div>
            </div>

            <div class="card full-width">
                <h2>4. Key Insights & Cohesive Narrative</h2>
                
                <h3 style="margin-top: 1rem; color: var(--accent-color);">Insight A: The Silent Retention Crisis</h3>
                <p>We observe that 53% of all signups eventually churn. Adjusting for right-censoring shows that 15-20% of users fail to place a second order within 30 days. For cohorts like Dec 2023, who have been on the platform for 2.5 years, the raw churn rate reaches 92.3%. This underscores the urgency of early-stage intervention.</p>
                
                <h3 style="margin-top: 1rem; color: var(--accent-color);">Insight B: Delivery Friction Caps Satisfaction</h3>
                <p>Delays and contents inaccuracies on the first transaction severely depress return rates. A first-order delay directly leads to a lower return probability. Moreover, when customer-level delay averages cross 15 minutes, CSAT ratings rarely exceed 4.0 stars. Service speed is the baseline requirement for retention.</p>
                
                <h3 style="margin-top: 1rem; color: var(--accent-color);">Insight C: Breadth over Incentives</h3>
                <p>Promotions do not buy long-term loyalty; standard users who use promotions on more than 80% of orders exhibit elevated churn. Instead, usage breadth is the primary driver of customer lifetime value: users shopping across multiple merchant categories have a churn rate under 30% (compared to 63.5% for single-category users).</p>
            </div>
        </div>
        
        <!-- UNIVARIATE -->
        <div id="univariate" class="tab-content">
            <div class="grid">
                <div class="card">
                    <h3>Order Value Distributions</h3>
                    <p class="desc">Evaluating order values to observe right-skewed distributions and normal log-transforms.</p>
                    <img src="{figures['uni_val']}" alt="Order Value Distributions">
                </div>
                
                <div class="card">
                    <h3>Items Count & Discounts</h3>
                    <p class="desc">Distribution of item basket sizes and promo discount depth.</p>
                    <img src="{figures['uni_items']}" alt="Items & Discounts">
                </div>
                
                <div class="card">
                    <h3>Delivery Performance CDF</h3>
                    <p class="desc">Operational late-minutes density alongside the Cumulative Distribution Function (CDF).</p>
                    <img src="{figures['uni_delays']}" alt="Delivery Delays CDF">
                </div>
                
                <div class="card">
                    <h3>Promised vs. Actual Durations</h3>
                    <p class="desc">Comparing promised delivery windows against actual travel times.</p>
                    <img src="{figures['uni_comp']}" alt="Promised vs. Actual">
                </div>
                
                <div class="card">
                    <h3>Customer Order Frequency & Spend</h3>
                    <p class="desc">Aggregated order count frequencies and lifetime spends at the user level.</p>
                    <img src="{figures['uni_spend']}" alt="Engagement Frequency & Spend">
                </div>
                
                <div class="card">
                    <h3>Active Lifespans & Recency</h3>
                    <p class="desc">Tenure days between signup and last order compared against inactive recency days.</p>
                    <img src="{figures['uni_life']}" alt="Lifespan & Recency">
                </div>
                
                <div class="card">
                    <h3>Customer Demographics (2x2 Grid)</h3>
                    <p class="desc">Customer splits by gender, age groups, device types, and business segments.</p>
                    <img src="{figures['uni_demo']}" alt="Demographics">
                </div>
                
                <div class="card">
                    <h3>Geographic Concentrations</h3>
                    <p class="desc">Splits across active urban cities and regional states.</p>
                    <img src="{figures['uni_loc']}" alt="Locations">
                </div>
                
                <div class="card">
                    <h3>Monthly Cohort Return Rates</h3>
                    <p class="desc">First-order 30-day, 60-day, and 90-day return rates across monthly registration cohorts (censoring adjusted).</p>
                    <img src="{figures['uni_cohort_rates']}" alt="Cohort Return Rates">
                </div>
                
                <div class="card">
                    <h3>Cohort Comparison (Dec 2023 vs Jan 2024+)</h3>
                    <p class="desc">Comparing order frequency and active lifespan between the first-month cohort and later signups.</p>
                    <img src="{figures['uni_cohort_comp']}" alt="Cohort Comparison">
                </div>
            </div>
        </div>
        
        <!-- BIVARIATE -->
        <div id="bivariate" class="tab-content">
            <div class="grid">
                <div class="card">
                    <h3>First Order Delivery Status vs. Retention</h3>
                    <p class="desc">Return rates by 30-day, 60-day, and 90-day windows based on first order delivery success.</p>
                    <img src="{figures['bi_status']}" alt="First Order Success vs Retention">
                </div>
                
                <div class="card">
                    <h3>First Order Customer Ratings vs. 30-Day Return</h3>
                    <p class="desc">Direct association between delivery ratings and return probability.</p>
                    <img src="{figures['bi_rating']}" alt="Ratings vs Return">
                </div>
                
                <div class="card">
                    <h3>First Order Promo Application vs. 30-Day Return</h3>
                    <p class="desc">Impact of incentive-driven ordering on early user return rates.</p>
                    <img src="{figures['bi_promo']}" alt="Promo vs Return">
                </div>
                
                <div class="card">
                    <h3>Promo Sensitivity vs. Customer Lifetime Value</h3>
                    <p class="desc">Scatter plot comparing proportion of promo orders against customer lifetime spend.</p>
                    <img src="{figures['bi_vs_spend']}" alt="Promo Sensitivity vs LTV">
                </div>
                
                <div class="card">
                    <h3>Usage Breadth vs. Churn Rate</h3>
                    <p class="desc">Churn rates by number of unique vendor categories and service types ordered.</p>
                    <img src="{figures['bi_breadth']}" alt="Usage Breadth vs Churn">
                </div>
                
                <div class="card">
                    <h3>Demographics vs. Churn Rate</h3>
                    <p class="desc">Subgroup churn rates split by segments, devices, and age groups.</p>
                    <img src="{figures['bi_demo']}" alt="Demographics vs Churn">
                </div>
                
                <div class="card">
                    <h3>Delivery Experience Profile vs. Retention</h3>
                    <p class="desc">Customer-level box plots comparing prompt rate, delays, and CSAT for active vs. churned users.</p>
                    <img src="{figures['bi_delivery_churn']}" alt="Delivery Experience vs Retention">
                </div>
                
                <div class="card">
                    <h3>Spending Profile vs. Retention</h3>
                    <p class="desc">Customer-level box plots comparing AOV and items count for active vs. churned users.</p>
                    <img src="{figures['bi_spend_churn']}" alt="Spending vs Retention">
                </div>
            </div>
        </div>
        
        <!-- MULTIVARIATE -->
        <div id="multivariate" class="tab-content">
            <div class="grid">
                <div class="card full-width">
                    <h3>Correlation Matrix of Customer Features</h3>
                    <p class="desc">Correlation heatmap of user aggregates, operational performance, and ratings.</p>
                    <img src="{figures['multi_corr']}" alt="Correlation Matrix">
                </div>
                
                <div class="card">
                    <h3>Customer Ratings vs. Delays by Churn</h3>
                    <p class="desc">Scatter mapping delay minutes and ratings jointly, coded by user churn status.</p>
                    <img src="{figures['multi_scatter']}" alt="Ratings vs Delays scatter">
                </div>
                
                <div class="card">
                    <h3>Promotion Sensitivity vs. Segment Churn</h3>
                    <p class="desc">Churn rates across promo usage tiers stratified by New, Regular, and Premium customer tiers.</p>
                    <img src="{figures['multi_promo']}" alt="Segment Promo Churn">
                </div>
            </div>
        </div>
        
        <!-- STATS -->
        <div id="stats" class="tab-content">
            <div class="card full-width">
                <h3>Hypothesis Testing & Regression Outcomes</h3>
                <p class="desc">Log summaries of Chi-Square, Mann-Whitney U, and Binary Logistic Regression models.</p>
                <pre>{hypothesis_testing_results_txt}</pre>
            </div>
        </div>
        
        <!-- DESC -->
        <div id="desc" class="tab-content">
            <div class="card full-width">
                <h3>Descriptive Statistics Summary</h3>
                <p class="desc">Detailed tabular breakdown of order-level and customer-level features.</p>
                <div style="margin-top: 1rem;">
                    {descriptive_html}
                </div>
            </div>
        </div>
        
    </div>
    
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].style.display = "none";
                tabcontent[i].classList.remove("active");
            }}
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].classList.remove("active");
            }}
            document.getElementById(tabName).style.display = "block";
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}
    </script>
</body>
</html>
"""
    
    # Save compilation
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Stand-alone HTML dashboard report successfully generated at {OUTPUT_PATH}")

if __name__ == '__main__':
    compile_report()
