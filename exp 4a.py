import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Create sample dataset
# -----------------------------
data = {
    'date': pd.date_range(start='2023-01-01', periods=14),  # 2 weeks
    'city': ['CityA', 'CityB'] * 7,
    'temperature': [28, 30, 27, 32, 29, 33, 31, 30, 34, 29, 35, 28, 33, 30]
}

df = pd.DataFrame(data)

# Display dataset
print("🔹 Original Temperature Dataset:")
print(df)

# -----------------------------
# Step 2: Add Week Number Column
# -----------------------------
df['week'] = df['date'].dt.isocalendar().week

print("\n🔹 With Week Number:")
print(df[['date', 'city', 'temperature', 'week']])

# -----------------------------
# Step 3: Group By Week and City, then Sum
# -----------------------------
grouped = df.groupby(['week', 'city'])['temperature'].sum().reset_index()

print("\n🔹 Grouped by Week and City (Sum of Temperatures):")
print(grouped)

# -----------------------------
# Step 4: Plot the Result
# -----------------------------
plt.figure(figsize=(6, 4))
for city in grouped['city'].unique():
    weekly_data = grouped[grouped['city'] == city]
    plt.plot(weekly_data['week'], weekly_data['temperature'], marker='o', label=city)

plt.title("Total Weekly Temperatures by City")
plt.xlabel("Week Number")
plt.ylabel("Total Temperature")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
