import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Titanic dataset (can also load from seaborn for built-in version)
df = sns.load_dataset('titanic')

# Display first few rows
print("First 5 rows of the dataset:")
print(df.head())

# Basic Data Info
print("\nDataset Summary:")
print(df.info())

# Drop rows with missing 'age' or 'embarked'
df.dropna(subset=['age', 'embarked'], inplace=True)

# Analysis: Survival Rate by Gender
survival_by_gender = df.groupby('sex')['survived'].mean()
print("\nSurvival Rate by Gender:")
print(survival_by_gender)

# Visualization 1: Bar plot of survival by gender
plt.figure(figsize=(6, 4))
survival_by_gender.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Survival Rate by Gender')
plt.ylabel('Survival Rate')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Analysis: Survival by Passenger Class
survival_by_class = df.groupby('pclass')['survived'].mean()
print("\nSurvival Rate by Class:")
print(survival_by_class)

# Visualization 2: Bar plot of survival by class
plt.figure(figsize=(6, 4))
survival_by_class.plot(kind='bar', color='green')
plt.title('Survival Rate by Passenger Class')
plt.xlabel('Class')
plt.ylabel('Survival Rate')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Visualization 3: Heatmap - Correlation Matrix
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()
