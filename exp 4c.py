import seaborn as sns
import matplotlib.pyplot as plt

# Load built-in 'tips' dataset
df = sns.load_dataset('tips')

# -------------------------------
# 1. Countplot – Total counts by day
# -------------------------------
plt.figure(figsize=(6, 4))
sns.countplot(x='day', data=df, palette='Set2')
plt.title('Number of Tips by Day')
plt.tight_layout()
plt.show()

# -------------------------------
# 2. Barplot – Average total bill by day
# -------------------------------
plt.figure(figsize=(6, 4))
sns.barplot(x='day', y='total_bill', data=df, palette='Blues_d')
plt.title('Average Total Bill by Day')
plt.tight_layout()
plt.show()

# -------------------------------
# 3. Scatterplot – Total bill vs tip
# -------------------------------
plt.figure(figsize=(6, 4))
sns.scatterplot(x='total_bill', y='tip', hue='sex', style='time', data=df)
plt.title('Tip vs Total Bill')
plt.tight_layout()
plt.show()

# -------------------------------
# 4. Boxplot – Total bill by smoker/non-smoker
# -------------------------------
plt.figure(figsize=(6, 4))
sns.boxplot(x='smoker', y='total_bill', data=df, palette='Set3')
plt.title('Total Bill Distribution by Smoker Status')
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Heatmap – Correlation matrix
# -------------------------------
plt.figure(figsize=(6, 4))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()
