import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# 1. Prepare Data
# -----------------------

data = {
    "Year": list(range(2015, 2026)),
    "House Price (€)": [
        332942, 350000, 370000, 390000, 410000, 430000,
        460000, 598907, 610000, 603453, 610000
    ],
    "Monthly Rent (€)": [
        1300, 1400, 1500, 1600, 1700, 1800,
        1900, 2000, 2102, 2300, 2540
    ],
    "Annual Salary (€)": [
        45075, 46000, 47000, 48000, 49000, 50000,
        51000, 52000, 53000, 50000, 51000
    ]
}

df = pd.DataFrame(data)

# -----------------------
# 2. Compute Rent & Salary Ratios
# -----------------------

df["Annual Rent (€)"] = df["Monthly Rent (€)"] * 12
df["Price-to-Salary Ratio"] = df["House Price (€)"] / df["Annual Salary (€)"]
df["Rent-to-Salary Ratio"] = df["Annual Rent (€)"] / df["Annual Salary (€)"]
df["Rent-to-Price Ratio"] = df["Annual Rent (€)"] / df["House Price (€)"]

# -----------------------
# 3. Mortgage Metrics
# -----------------------

interest_rate = 0.04  # 4% annual
term_years = 30
n = term_years * 12
monthly_rate = interest_rate / 12

def calc_monthly_payment(principal):
    return principal * (monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)

df["Monthly Mortgage (€)"] = df["House Price (€)"].apply(calc_monthly_payment)
df["Annual Mortgage (€)"] = df["Monthly Mortgage (€)"] * 12
df["Mortgage-to-Salary Ratio"] = df["Annual Mortgage (€)"] / df["Annual Salary (€)"]
df["Total Payment (€)"] = df["Monthly Mortgage (€)"] * n
df["Total Interest (€)"] = df["Total Payment (€)"] - df["House Price (€)"]
df["Loan-to-Income Ratio"] = df["House Price (€)"] / df["Annual Salary (€)"]

# -----------------------
# 4. Visualization
# -----------------------

plt.figure(figsize=(14, 12))

plt.subplot(3, 1, 1)
plt.plot(df["Year"], df["Mortgage-to-Salary Ratio"], marker='o', color='purple')
plt.title('Annual Mortgage Payment to Salary Ratio (Dublin, 2015–2025)')
plt.ylabel('Ratio')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(df["Year"], df["Total Interest (€)"] / 1000, marker='o', color='orange')
plt.title('Total Interest Paid over 30-Year Mortgage (in €000)')
plt.ylabel('€ Thousands')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(df["Year"], df["Loan-to-Income Ratio"], marker='o', color='brown')
plt.title('Loan to Income Ratio (Dublin, 2015–2025)')
plt.xlabel('Year')
plt.ylabel('Ratio')
plt.grid(True)

plt.tight_layout()
plt.show()

# -----------------------
# 5. Display Summary
# -----------------------

pd.set_option("display.float_format", lambda x: f"€{x:,.2f}")
print(df[[
    "Year",
    "House Price (€)",
    "Monthly Mortgage (€)",
    "Mortgage-to-Salary Ratio",
    "Total Interest (€)"
]].tail())
