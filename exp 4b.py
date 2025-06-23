import pandas as pd

# -----------------------------
# Step 1: Sample Work Hours Data
# -----------------------------
data = {
    'employee': ['Alice', 'Bob', 'Alice', 'Bob', 'Alice', 'Bob', 'Alice', 'Bob'],
    'date': [
        '2023-06-17', '2023-06-17',
        '2023-06-18', '2023-06-18',
        '2023-06-19', '2023-06-19',
        '2023-06-20', '2023-06-20'
    ],
    'hours_worked': [8, 7, 9, 8, 8, 6, 7, 8]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime

print("🔹 Original Employee Work Hours Data:")
print(df)

# -----------------------------
# Step 2: Total Hours by Employee
# -----------------------------
total_by_employee = df.groupby('employee')['hours_worked'].sum().reset_index()

print("\n🔹 Total Hours Worked by Each Employee:")
print(total_by_employee)

# -----------------------------
# Step 3: Total Hours by Date
# -----------------------------
total_by_date = df.groupby('date')['hours_worked'].sum().reset_index()

print("\n🔹 Total Hours Worked by Date:")
print(total_by_date)

# -----------------------------
# Step 4: Total Weekly Hours by Employee
# -----------------------------
df['week'] = df['date'].dt.isocalendar().week
weekly_hours = df.groupby(['employee', 'week'])['hours_worked'].sum().reset_index()

print("\n🔹 Total Weekly Hours by Each Employee:")
print(weekly_hours)
