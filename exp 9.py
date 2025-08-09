import pandas as pd import 
numpy as np import 
seaborn as sns 
import matplotlib.pyplot as plt 
np.random.seed(42) employee_id = 
range(1, 101) 
age = np.random.randint(22, 60, size=100) 
gender = np.random.choice(['Male', 'Female'], size=100) 
department = np.random.choice(['HR', 'Sales', 'IT', 'Marketing'], size=100) 
years_of_experience = np.random.randint(1, 15, size=100) performance_rating = 
np.random.randint(1, 6, size=100) 
salary = np.random.randint(40000, 120000, size=100) 
employee_data = pd.DataFrame({ 
'EmployeeID': employee_id, 'Age': 
age, 
'Gender': gender, 'Department': 
department, 
'YearsOfExperience': years_of_experience, 
'PerformanceRating': performance_rating, 
'Salary': salary 
}) 
employee_data.to_csv('employee_data.csv', index=False) 
employee_data = pd.read_csv('employee_data.csv') 
print(employee_data.info()) print(employee_data.describe()) 
print(employee_data.isnull().sum()) 
department_distribution = employee_data['Department'].value_counts() 
print(department_distribution) 
import matplotlib.pyplot as plt import seaborn as sns 
sns.histplot(employee_data['Age'], bins=20, kde=True)  
 
 
 
lOMoARcPSD|15081951 
 
 
plt.title('Distribution of Employee Ages') 
plt.show() 
sns.boxplot(x='Department', y='PerformanceRating', data=employee_data) 
plt.title('Performance Ratings by Department') 
plt.show()
