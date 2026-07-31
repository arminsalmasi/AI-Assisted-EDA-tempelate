import base64
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "report"
OUTPUT_PATH = REPORT_DIR / "urban_cart_retention_report.html"

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
        # Bivariate
        "bi_status": get_image_base64(REPORT_DIR / "figures" / "bivariate_status_retention.png"),
        "bi_rating": get_image_base64(REPORT_DIR / "figures" / "bivariate_rating_retention.png"),
        "bi_promo": get_image_base64(REPORT_DIR / "figures" / "bivariate_promo_retention.png"),
        "bi_vs_spend": get_image_base64(REPORT_DIR / "figures" / "bivariate_promo_vs_spend.png"),
        "bi_breadth": get_image_base64(REPORT_DIR / "figures" / "bivariate_usage_breadth_vs_churn.png"),
        "bi_demo": get_image_base64(REPORT_DIR / "figures" / "bivariate_demographics_vs_churn.png"),
        # Multivariate
        "multi_corr": get_image_base64(REPORT_DIR / "figures" / "multivariate_correlation_matrix.png"),
        "multi_scatter": get_image_base64(REPORT_DIR / "figures" / "multivariate_delay_rating_scatter.png"),
        "multi_promo": get_image_base64(REPORT_DIR / "figures" / "multivariate_segment_promo_churn.png")
    }
    
    # 2. Load statistical text files
    descriptive_stats_md = load_text_file(REPORT_DIR / "descriptive_stats.md")
    hypothesis_testing_results_txt = load_text_file(REPORT_DIR / "hypothesis_testing_results.txt")
    
    # Simple markdown parser for descriptive stats tables in html
    # Let's read descriptive stats and convert markdown tables to simple html tables
    import markdown
    descriptive_html = markdown.markdown(descriptive_stats_md, extensions=['tables'])
    
    # Create HTML structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UrbanCart Customer Retention Dashboard</title>
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
            font-size: 3rem;
            background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        header p {{
            font-size: 1.2rem;
            color: var(--text-muted);
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
            margin-bottom: 2rem;
        }}
        
        .tab-btn {{
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 0.8rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .tab-btn:hover, .tab-btn.active {{
            background: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-glow);
            border-color: var(--accent-color);
            color: #0f172a;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
            animation: fadeIn 0.5s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Layout Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .card.full-width {{
            grid-column: 1 / -1;
        }}
        
        .card img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin-top: 1rem;
            background: white; /* Contrast for light charts */
        }}
        
        .card p.desc {{
            color: var(--text-muted);
            margin-bottom: 1rem;
        }}
        
        pre {{
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
            color: #a855f7;
            white-space: pre-wrap;
        }}
        
        /* Table Styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
        }}
        
        th, td {{
            padding: 0.8rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        th {{
            background: rgba(15, 23, 42, 0.5);
            color: var(--accent-color);
            font-weight: 600;
        }}
        
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
        
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>UrbanCart Customer Retention Dashboard</h1>
            <p>Unbiased Cohort Retention, Operational Experience & Hypothesis Testing Analysis</p>
        </header>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab(event, 'univariate')">Univariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'bivariate')">Bivariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'multivariate')">Multivariate Analysis</button>
            <button class="tab-btn" onclick="openTab(event, 'stats')">Hypothesis Testing</button>
            <button class="tab-btn" onclick="openTab(event, 'desc')">Descriptive Statistics</button>
        </div>
        
        <!-- UNIVARIATE -->
        <div id="univariate" class="tab-content active">
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
                    <h3>Customer Demographics</h3>
                    <p class="desc">Customer splits by gender, age groups, and business segments.</p>
                    <img src="{figures['uni_demo']}" alt="Demographics">
                </div>
                
                <div class="card">
                    <h3>Geographic Concentrations</h3>
                    <p class="desc">Splits across active urban cities and regional states.</p>
                    <img src="{figures['uni_loc']}" alt="Locations">
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
