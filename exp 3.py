import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PART 1: NumPy Arrays
# -----------------------------
print("🔹 NumPy Array Creation and Operations")

# Create a NumPy array
arr = np.array([10, 20, 30, 40, 50])
print("Array:", arr)

# Perform operations
print("Array + 5:", arr + 5)
print("Array * 2:", arr * 2)
print("Mean:", np.mean(arr))
print("Standard Deviation:", np.std(arr))

# -----------------------------
# PART 2: Pandas DataFrame
# -----------------------------
print("\n🔹 Creating a DataFrame with Pandas")

# Create dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Marks': [85, 90, 78, 92, 88],
    'Age': [20, 21, 19, 22, 20]
}

# Convert to DataFrame
df = pd.DataFrame(data)
print("DataFrame:\n", df)

# Describe data
print("\n🔹 Statistical Summary:")
print(df.describe())

# Accessing specific column
print("\nMarks column:\n", df['Marks'])

# Filter students with marks > 85
high_scorers = df[df['Marks'] > 85]
print("\nStudents with Marks > 85:\n", high_scorers)

# -----------------------------
# PART 3: Basic Plots with Matplotlib
# -----------------------------
print("\n🔹 Plotting using Matplotlib")

# Bar plot: Names vs Marks
plt.figure(figsize=(6, 4))
plt.bar(df['Name'], df['Marks'], color='skyblue')
plt.title('Student Marks')
plt.xlabel('Name')
plt.ylabel('Marks')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Line plot: Age vs Marks
plt.figure(figsize=(6, 4))
plt.plot(df['Age'], df['Marks'], marker='o', color='green')
plt.title('Marks by Age')
plt.xlabel('Age')
plt.ylabel('Marks')
plt.grid(True)
plt.tight_layout()
plt.show()

# Pie chart of Age distribution
age_counts = df['Age'].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Age Distribution')
plt.tight_layout()
plt.show()
