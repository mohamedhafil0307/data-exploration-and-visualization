
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("winequality-red.csv", sep=";")


print("===== Dataset Shape =====")
print(df.shape)

print("\n===== First 5 Rows =====")
print(df.head())

print("\n===== Dataset Info =====")
print(df.info())

print("\n===== Summary Statistics =====")
print(df.describe())

print("\n===== Missing Values =====")
print(df.isnull().sum())

plt.figure(figsize=(6,4))
sns.countplot(x='quality', data=df, palette="viridis")
plt.title("Wine Quality Distribution")
plt.xlabel("Quality Score")
plt.ylabel("Count")
plt.show()


df.hist(bins=15, figsize=(15,10), color='skyblue', edgecolor='black')
plt.suptitle("Feature Distributions", fontsize=16)
plt.show()


plt.figure(figsize=(12,8))
corr = df.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()


plt.figure(figsize=(12,6))
sns.boxplot(x='quality', y='alcohol', data=df, palette="Set2")
plt.title("Alcohol Content vs Quality")
plt.show()

plt.figure(figsize=(12,6))
sns.boxplot(x='quality', y='volatile acidity', data=df, palette="Set3")
plt.title("Volatile Acidity vs Quality")
plt.show()

print("\n===== EDA Completed Successfully =====")
