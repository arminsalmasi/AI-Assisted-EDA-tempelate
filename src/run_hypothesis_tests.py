import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = BASE_DIR / "report" / "hypothesis_testing_results.txt"

def load_first_order_rows():
    orders = pd.read_csv(DATA_DIR / "master_orders.csv")
    customers = pd.read_csv(DATA_DIR / "customer_features.csv")
    
    first_orders = orders[orders['customer_order_number'] == 1].copy()
    
    # Select columns to merge
    cols_to_use = [
        'customer_id', 'order_value_usd', 'items_count', 'delay_minutes',
        'customer_rating', 'delivery_status', 'order_accuracy', 'promo_used',
        'discount_amount_usd', 'vendor_category', 'delivery_type'
    ]
    
    merged = pd.merge(
        customers[[
            'customer_id', 'customer_segment', 'preferred_device',
            'returned_after_first_order_30d', 'returned_after_first_order_60d', 'returned_after_first_order_90d',
            'full_30d_observation_flag', 'full_60d_observation_flag', 'full_90d_observation_flag'
        ]],
        first_orders[cols_to_use],
        on='customer_id',
        how='inner'
    )
    return merged

def benjamini_hochberg_adjust(pvalues):
    pvals = np.array(pvalues)
    n = len(pvals)
    sorted_indices = np.argsort(pvals)
    sorted_pvals = pvals[sorted_indices]
    
    adjusted = np.zeros(n)
    running_min = 1.0
    for i in range(n - 1, -1, -1):
        p = sorted_pvals[i]
        adj = p * n / (i + 1)
        adj = min(1.0, adj)
        running_min = min(running_min, adj)
        adjusted[sorted_indices[i]] = running_min
        
    return list(adjusted)

def format_pvalue(p_val):
    if pd.isna(p_val) or p_val is None:
        return "N/A"
    if p_val < 0.0001:
        return "<0.0001"
    return f"{p_val:.4f}"

def format_rate(retained, total):
    if total == 0:
        return "0/0 (0.0%)"
    return f"{retained}/{total} ({retained/total:.1%})"

def run_logistic_regression(df, formula):
    try:
        # Fit logistic regression
        model = smf.logit(formula, data=df).fit(disp=False)
        return model
    except Exception as e:
        return str(e)

def build_report():
    df = load_first_order_rows()
    windows = [30, 60, 90]
    lines = [
        "UrbanCart Hypothesis Testing Results",
        "",
        "Method note",
        "- Unit of analysis: customer first order only",
        "- Eligible cohorts exclude customers without a full observation window for the tested outcome",
        "- Primary outcome per section is first-order return within 30 days, with 60-day and 90-day robustness checks",
        "- Logistic regressions were estimated with statsmodels API using maximum likelihood estimation (MLE)",
        "",
    ]
    
    for w in windows:
        # Filter eligible rows
        outcome_col = f"returned_after_first_order_{w}d"
        obs_flag_col = f"full_{w}d_observation_flag"
        
        cohort = df[(df[obs_flag_col] == 1) & (df[outcome_col].notna())]
        total = len(cohort)
        retained = int(cohort[outcome_col].sum())
        
        lines.extend([
            f"Cohort overview: {w}-day window",
            f"- Eligible first-order customers: {total}",
            f"- Retained within {w} days: {format_rate(retained, total)}",
            ""
        ])
        
    for w in windows:
        outcome_col = f"returned_after_first_order_{w}d"
        obs_flag_col = f"full_{w}d_observation_flag"
        cohort = df[(df[obs_flag_col] == 1) & (df[outcome_col].notna())].copy()
        cohort[outcome_col] = cohort[outcome_col].astype(int)
        
        lines.extend([
            f"Hypothesis 1: Delivery reliability and {w}-day retention",
            "Descriptive view"
        ])
        
        # delivery_status vs retention
        for val in sorted(cohort['delivery_status'].unique()):
            subset = cohort[cohort['delivery_status'] == val]
            retained = subset[outcome_col].sum()
            lines.append(f"- delivery_status = {val}: {format_rate(retained, len(subset))}")
            
        # order_accuracy vs retention
        for val in sorted(cohort['order_accuracy'].unique()):
            subset = cohort[cohort['order_accuracy'] == val]
            retained = subset[outcome_col].sum()
            lines.append(f"- order_accuracy = {val}: {format_rate(retained, len(subset))}")
            
        # delay_minutes by outcome
        ret_delays = cohort[cohort[outcome_col] == 1]['delay_minutes']
        not_delays = cohort[cohort[outcome_col] == 0]['delay_minutes']
        lines.append(f"- Delay minutes: retained mean={ret_delays.mean():.2f}, median={ret_delays.median():.2f}; not retained mean={not_delays.mean():.2f}, median={not_delays.median():.2f}")
        
        # customer_rating by outcome
        ret_ratings = cohort[cohort[outcome_col] == 1]['customer_rating']
        not_ratings = cohort[cohort[outcome_col] == 0]['customer_rating']
        lines.append(f"- Customer rating: retained mean={ret_ratings.mean():.2f}, median={ret_ratings.median():.2f}; not retained mean={not_ratings.mean():.2f}, median={not_ratings.median():.2f}")
        
        # Statistical tests
        # Chi-square status
        contingency_status = pd.crosstab(cohort['delivery_status'], cohort[outcome_col])
        chi2_status, p_status, dof_status, _ = stats.chi2_contingency(contingency_status)
        
        # Chi-square accuracy
        contingency_accuracy = pd.crosstab(cohort['order_accuracy'], cohort[outcome_col])
        chi2_accuracy, p_accuracy, dof_accuracy, _ = stats.chi2_contingency(contingency_accuracy)
        
        # Mann-Whitney delay
        mw_delay, p_delay = stats.mannwhitneyu(ret_delays, not_delays, alternative='two-sided')
        # Calculate standard normal z-score approximation from scipy output
        # z = (U - mean) / std. Statsmodels/scipy provides this or we can compute z-score
        n1 = len(ret_delays)
        n2 = len(not_delays)
        mu_u = n1 * n2 / 2.0
        # Compute tied ranks correction
        combined = pd.concat([ret_delays, not_delays])
        ranks = combined.rank()
        tie_counts = combined.value_counts()
        t_correction = sum(t**3 - t for t in tie_counts)
        std_u = np.sqrt((n1 * n2 / 12.0) * ((n1 + n2 + 1) - t_correction / ((n1 + n2) * (n1 + n2 - 1))))
        z_delay = (mw_delay - mu_u) / std_u if std_u > 0 else 0.0
        
        # Mann-Whitney rating
        mw_rating, p_rating = stats.mannwhitneyu(ret_ratings, not_ratings, alternative='two-sided')
        combined_ratings = pd.concat([ret_ratings, not_ratings])
        ranks_ratings = combined_ratings.rank()
        tie_counts_ratings = combined_ratings.value_counts()
        t_correction_ratings = sum(t**3 - t for t in tie_counts_ratings)
        std_u_ratings = np.sqrt((n1 * n2 / 12.0) * ((n1 + n2 + 1) - t_correction_ratings / ((n1 + n2) * (n1 + n2 - 1))))
        z_rating = (mw_rating - mu_u) / std_u_ratings if std_u_ratings > 0 else 0.0
        
        # Adjust p-values using Benjamini-Hochberg
        pvals = [p_status, p_accuracy, p_delay, p_rating]
        adjusted = benjamini_hochberg_adjust(pvals)
        
        lines.extend([
            "Statistical tests",
            f"- Chi-square for delivery status vs retention: chi2={chi2_status:.3f}, df={dof_status}, p={format_pvalue(p_status)}, BH-adjusted p={format_pvalue(adjusted[0])}",
            f"- Chi-square for order accuracy vs retention: chi2={chi2_accuracy:.3f}, df={dof_accuracy}, p={format_pvalue(p_accuracy)}, BH-adjusted p={format_pvalue(adjusted[1])}",
            f"- Mann-Whitney U for delay minutes: U={mw_delay:.1f}, z={z_delay:.3f}, p={format_pvalue(p_delay)}, BH-adjusted p={format_pvalue(adjusted[2])}",
            f"- Mann-Whitney U for customer rating: U={mw_rating:.1f}, z={z_rating:.3f}, p={format_pvalue(p_rating)}, BH-adjusted p={format_pvalue(adjusted[3])}"
        ])
        
        # Logistic Regression Hypothesis 1
        lines.append("Adjusted logistic regression")
        # Define features:
        # C(order_accuracy) has categories: Correct (ref), Partial, Wrong.
        # C(customer_segment) has categories: New (ref), Regular, Premium.
        # C(preferred_device) has categories: Mobile App (ref), Web.
        formula = f"{outcome_col} ~ delay_minutes + customer_rating + C(order_accuracy, Treatment('Correct')) + I(order_value_usd / 10.0) + items_count + C(customer_segment, Treatment('New')) + C(preferred_device, Treatment('Mobile App'))"
        model = run_logistic_regression(cohort, formula)
        
        if isinstance(model, str):
            lines.append(f"- Model error: {model}")
        else:
            lines.append(f"- n={int(model.nobs)}, McFadden pseudo-R2={model.prsquared:.4f}")
            # delay_minutes
            coef = model.params['delay_minutes']
            se = model.bse['delay_minutes']
            pval = model.pvalues['delay_minutes']
            lines.append(f"- delay_minutes: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
            # customer_rating
            coef = model.params['customer_rating']
            se = model.bse['customer_rating']
            pval = model.pvalues['customer_rating']
            lines.append(f"- customer_rating: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
            # accuracy_partial
            coef = model.params["C(order_accuracy, Treatment('Correct'))[T.Partial]"]
            se = model.bse["C(order_accuracy, Treatment('Correct'))[T.Partial]"]
            pval = model.pvalues["C(order_accuracy, Treatment('Correct'))[T.Partial]"]
            lines.append(f"- accuracy_partial: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
            # accuracy_wrong
            coef = model.params["C(order_accuracy, Treatment('Correct'))[T.Wrong]"]
            se = model.bse["C(order_accuracy, Treatment('Correct'))[T.Wrong]"]
            pval = model.pvalues["C(order_accuracy, Treatment('Correct'))[T.Wrong]"]
            lines.append(f"- accuracy_wrong: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
            
        lines.append("")
        
    for w in windows:
        outcome_col = f"returned_after_first_order_{w}d"
        obs_flag_col = f"full_{w}d_observation_flag"
        cohort = df[(df[obs_flag_col] == 1) & (df[outcome_col].notna())].copy()
        cohort[outcome_col] = cohort[outcome_col].astype(int)
        promo_users = cohort[cohort['promo_used'] == 'Yes'].copy()
        
        lines.extend([
            f"Hypothesis 2: Promotion-driven engagement and {w}-day retention",
            "Descriptive view"
        ])
        
        # promo_used vs retention
        for val in sorted(cohort['promo_used'].unique()):
            subset = cohort[cohort['promo_used'] == val]
            retained = subset[outcome_col].sum()
            lines.append(f"- promo_used = {val}: {format_rate(retained, len(subset))}")
            
        # discount_amount_usd overall
        ret_disc = cohort[cohort[outcome_col] == 1]['discount_amount_usd']
        not_disc = cohort[cohort[outcome_col] == 0]['discount_amount_usd']
        lines.append(f"- Discount amount across all first orders: retained mean={ret_disc.mean():.2f}, median={ret_disc.median():.2f}; not retained mean={not_disc.mean():.2f}, median={not_disc.median():.2f}")
        
        # discount_amount_usd promo users only
        if len(promo_users) > 0:
            ret_disc_promo = promo_users[promo_users[outcome_col] == 1]['discount_amount_usd']
            not_disc_promo = promo_users[promo_users[outcome_col] == 0]['discount_amount_usd']
            lines.append(f"- Discount amount among promo users only: retained mean={ret_disc_promo.mean():.2f}, median={ret_disc_promo.median():.2f}; not retained mean={not_disc_promo.mean():.2f}, median={not_disc_promo.median():.2f}")
            
        # Statistical tests
        # Chi-square promo
        contingency_promo = pd.crosstab(cohort['promo_used'], cohort[outcome_col])
        chi2_promo, p_promo, dof_promo, _ = stats.chi2_contingency(contingency_promo)
        
        # Mann-Whitney discount overall
        mw_disc_all, p_disc_all = stats.mannwhitneyu(ret_disc, not_disc, alternative='two-sided')
        n1 = len(ret_disc)
        n2 = len(not_disc)
        mu_u = n1 * n2 / 2.0
        combined_disc = pd.concat([ret_disc, not_disc])
        tie_counts_disc = combined_disc.value_counts()
        t_correction_disc = sum(t**3 - t for t in tie_counts_disc)
        std_u_disc = np.sqrt((n1 * n2 / 12.0) * ((n1 + n2 + 1) - t_correction_disc / ((n1 + n2) * (n1 + n2 - 1))))
        z_disc_all = (mw_disc_all - mu_u) / std_u_disc if std_u_disc > 0 else 0.0
        
        pvals_h2 = [p_promo, p_disc_all]
        
        # Mann-Whitney promo discount
        if len(promo_users) > 0:
            mw_disc_promo, p_disc_promo = stats.mannwhitneyu(ret_disc_promo, not_disc_promo, alternative='two-sided')
            n1_p = len(ret_disc_promo)
            n2_p = len(not_disc_promo)
            mu_u_p = n1_p * n2_p / 2.0
            combined_disc_p = pd.concat([ret_disc_promo, not_disc_promo])
            tie_counts_disc_p = combined_disc_p.value_counts()
            t_correction_disc_p = sum(t**3 - t for t in tie_counts_disc_p)
            std_u_disc_p = np.sqrt((n1_p * n2_p / 12.0) * ((n1_p + n2_p + 1) - t_correction_disc_p / ((n1_p + n2_p) * (n1_p + n2_p - 1))))
            z_disc_promo = (mw_disc_promo - mu_u_p) / std_u_disc_p if std_u_disc_p > 0 else 0.0
            pvals_h2.append(p_disc_promo)
        else:
            p_disc_promo = None
            
        adjusted_h2 = benjamini_hochberg_adjust(pvals_h2)
        
        lines.extend([
            "Statistical tests",
            f"- Chi-square for promo usage vs retention: chi2={chi2_promo:.3f}, df={dof_promo}, p={format_pvalue(p_promo)}, BH-adjusted p={format_pvalue(adjusted_h2[0])}",
            f"- Mann-Whitney U for discount amount across all first orders: U={mw_disc_all:.1f}, z={z_disc_all:.3f}, p={format_pvalue(p_disc_all)}, BH-adjusted p={format_pvalue(adjusted_h2[1])}"
        ])
        if p_disc_promo is not None:
            lines.append(f"- Mann-Whitney U for discount amount among promo users: U={mw_disc_promo:.1f}, z={z_disc_promo:.3f}, p={format_pvalue(p_disc_promo)}, BH-adjusted p={format_pvalue(adjusted_h2[2])}")
            
        # Logistic Regression Hypothesis 2
        lines.append("Adjusted logistic regression")
        formula_h2 = f"{outcome_col} ~ C(promo_used, Treatment('No')) + I(order_value_usd / 10.0) + items_count + delay_minutes + customer_rating + C(customer_segment, Treatment('New')) + C(preferred_device, Treatment('Mobile App')) + C(delivery_type, Treatment('On-Demand')) + C(vendor_category, Treatment('Restaurant'))"
        model_h2 = run_logistic_regression(cohort, formula_h2)
        
        if isinstance(model_h2, str):
            lines.append(f"- Model error: {model_h2}")
        else:
            lines.append(f"- n={int(model_h2.nobs)}, McFadden pseudo-R2={model_h2.prsquared:.4f}")
            coef = model_h2.params["C(promo_used, Treatment('No'))[T.Yes]"]
            se = model_h2.bse["C(promo_used, Treatment('No'))[T.Yes]"]
            pval = model_h2.pvalues["C(promo_used, Treatment('No'))[T.Yes]"]
            lines.append(f"- promo_used_yes: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
            
        # Promo discount depth model
        if len(promo_users) > 0:
            lines.append("Promo-user discount-depth model")
            formula_depth = f"{outcome_col} ~ discount_amount_usd + I(order_value_usd / 10.0) + items_count + delay_minutes + customer_rating + C(customer_segment, Treatment('New')) + C(preferred_device, Treatment('Mobile App'))"
            model_depth = run_logistic_regression(promo_users, formula_depth)
            if isinstance(model_depth, str):
                lines.append(f"- Model error: {model_depth}")
            else:
                lines.append(f"- n={int(model_depth.nobs)}, McFadden pseudo-R2={model_depth.prsquared:.4f}")
                coef = model_depth.params['discount_amount_usd']
                se = model_depth.bse['discount_amount_usd']
                pval = model_depth.pvalues['discount_amount_usd']
                lines.append(f"- discount_amount_usd: OR={np.exp(coef):.3f}, 95% CI [{np.exp(coef - 1.96*se):.3f}, {np.exp(coef + 1.96*se):.3f}], p={format_pvalue(pval)}")
                
        lines.append("")
        
    lines.extend([
        "Overall conclusion",
        "- Hypothesis 1 is supported in direction, with the strongest and most consistent signal coming from customer rating. Customers with delayed first orders also show lower retention descriptively, but delay minutes are not a stable adjusted predictor once the other covariates are included.",
        "- Hypothesis 2 is not supported for the promotion-driven portion of the question. Promo usage and discount depth do not show statistically reliable retention lifts in these first-order models.",
        "- Personalization still cannot be tested with the available data because there are no exposure fields for campaigns, recommendations, or CRM interactions.",
        "- The 90-day logistic models are less stable because nearly all eligible customers return within 90 days, leaving very few non-return cases for estimation."
    ])
    
    return "\n".join(lines) + "\n"

def main():
    report = build_report()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Wrote hypothesis testing results to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
