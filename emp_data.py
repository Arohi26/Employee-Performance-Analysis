import pandas as pd

data = {
    "Employee_Name": ["Arohi", "Rahul", "Neha", "Vikrant", "Anjali"],
    "Department": ["IT", "HR", "IT", "Finance", "Marketing"],
    "Attendance": [92, 85, 97, 80, 90],
    "Project_Completion": [15, 12, 18, 10, 14],
    "Appraisal_Score": [88, 72, 94, 65, 82]
}

df = pd.DataFrame(data)


df.to_excel("employee_data.xlsx", index=False)
print("employee_data.xlsx created successfully!")
