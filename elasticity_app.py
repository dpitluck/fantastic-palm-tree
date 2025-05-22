import streamlit as st
import matplotlib.pyplot as plt

# Set default inputs
st.title("Elasticity of Contribution Profit")
st.write("Explore how changes in revenue or marketing spend impact contribution profit.")

# Input fields
baseline_revenue = st.number_input("Baseline Revenue", value=5000000)
baseline_marketing_spend = st.number_input("Baseline Marketing Spend", value=650000)
product_margin = st.slider("Product Margin", min_value=0.0, max_value=1.0, value=0.45)
cogs_pct = 1 - product_margin
other_costs_pct = st.slider("Other Costs (% of Revenue)", min_value=0.0, max_value=1.0, value=0.30)

delta_pct = 0.01 
# = st.slider("Delta % for Elasticity Calculation", min_value=0.001, max_value=0.1, value=0.01)

# Elasticity function
def calculate_elasticities(revenue, marketing_spend, cogs_pct, other_costs, delta_pct=0.01):
    baseline_cp = revenue - (revenue * cogs_pct) - (revenue * other_costs) - marketing_spend

    # Revenue elasticity
    revenue_up = revenue * (1 + delta_pct)
    cp_revenue_up = revenue_up - (revenue_up * cogs_pct) - (revenue_up * other_costs) - marketing_spend
    elasticity_revenue = ((cp_revenue_up - baseline_cp) / baseline_cp) / delta_pct

    # Marketing spend elasticity
    marketing_up = marketing_spend * (1 + delta_pct)
    cp_marketing_up = revenue - (revenue * cogs_pct) - (revenue * other_costs) - marketing_up
    elasticity_marketing = ((cp_marketing_up - baseline_cp) / baseline_cp) / delta_pct

    return {
        "Revenue Elasticity": elasticity_revenue,
        "Marketing Spend Elasticity": elasticity_marketing
    }

# Run calc
elasticity_results = calculate_elasticities(
    revenue=baseline_revenue,
    marketing_spend=baseline_marketing_spend,
    cogs_pct=cogs_pct,
    other_costs=other_costs_pct,
    delta_pct=delta_pct
)

# Display results
st.subheader("Elasticity Results")
st.json(elasticity_results)

# Plotting
fig, ax = plt.subplots()
ax.bar(elasticity_results.keys(), elasticity_results.values(), color=['green', 'red'])
ax.set_ylabel("Elasticity of Contribution Profit")
ax.set_title("Elasticity of Contribution Profit\nwith Respect to Revenue and Marketing Spend")
ax.axhline(0, color='black', linewidth=0.8)
st.pyplot(fig)

# Re-import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define sensitivity ranges
revenue_changes = np.arange(-0.25, 0.26, 0.05)
marketing_changes = np.arange(-0.25, 0.26, 0.05)

# Create the sensitivity table
sensitivity_table = pd.DataFrame(
    index=[f"{int(rc * 100)}%" for rc in revenue_changes],
    columns=[f"{int(mc * 100)}%" for mc in marketing_changes]
)

sensitivity_matrix = []

for rc in revenue_changes:
    row = []
    for mc in marketing_changes:
        new_revenue = baseline_revenue * (1 + rc)
        new_cogs = new_revenue * cogs_pct
        new_marketing = baseline_marketing_spend * (1 + mc)
        new_other_costs = new_revenue * other_costs_pct
        contribution_profit = new_revenue - new_cogs - new_other_costs - new_marketing
        profit_millions = round(contribution_profit / 1_000_000, 2)
        sensitivity_table.loc[f"{int(rc * 100)}%", f"{int(mc * 100)}%"] = profit_millions
        row.append(profit_millions)
    sensitivity_matrix.append(row)

# Plotting with matplotlib
fig, ax = plt.subplots(figsize=(12, 8))
cax = ax.matshow(sensitivity_matrix, cmap="YlGn", aspect="auto")

# Set axis labels
ax.set_xticks(np.arange(len(marketing_changes)))
ax.set_xticklabels([f"{int(mc*100)}%" for mc in marketing_changes])
ax.set_yticks(np.arange(len(revenue_changes)))
ax.set_yticklabels([f"{int(rc*100)}%" for rc in revenue_changes])

# Add text annotations
for i in range(len(revenue_changes)):
    for j in range(len(marketing_changes)):
        ax.text(j, i, f"{sensitivity_matrix[i][j]:.2f}",
                ha="center", va="center", color="black")

# Titles and labels
ax.set_title("Contribution Profit Sensitivity Table\n(in millions of dollars)", pad=20)
ax.set_xlabel("Marketing Spend Change")
ax.set_ylabel("Revenue Change")

# Colorbar
fig.colorbar(cax, label="Contribution Profit ($M)")

# Render in Streamlit
st.subheader("Contribution Profit Sensitivity Table")
st.pyplot(fig)

# CSV download
csv = sensitivity_table.to_csv().encode('utf-8')
st.download_button(
    label="📥 Download Sensitivity Table as CSV",
    data=csv,
    file_name='sensitivity_table.csv',
    mime='text/csv'
)