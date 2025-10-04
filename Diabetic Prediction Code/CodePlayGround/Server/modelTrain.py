import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from mlxtend.plotting import plot_decision_regions
from sklearn.datasets import make_circles
data=pd.read_csv('/content/diabetes_dataset.csv')
cols_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_to_replace] = data[cols_to_replace].replace(0, np.nan)
def median_target(var):
    temp = data[data[var].notnull()]
    temp = temp[[var, 'Outcome']].groupby(['Outcome'])[[var]].median().reset_index()
    return temp
# The values to be given for incomplete observations are given the median value of people who are not sick and the median values of people who are sick.
columns = data.columns
columns = columns.drop("Outcome")
for i in columns:
    median_target(i)
    data.loc[(data['Outcome'] == 0 ) & (data[i].isnull()), i] = median_target(i)[i][0]
    data.loc[(data['Outcome'] == 1 ) & (data[i].isnull()), i] = median_target(i)[i][1]

    
columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction']

for col in columns:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Keep only the rows within the IQR range
    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]

print("Shape after outlier removal:", data.shape)

# According to BMI, some ranges were determined and categorical variables were assigned.
NewBMI = pd.Series(["Underweight", "Normal", "Overweight", "Obesity 1", "Obesity 2", "Obesity 3"], dtype = "category")
data["NewBMI"] = NewBMI
data.loc[data["BMI"] < 18.5, "NewBMI"] = NewBMI[0]
data.loc[(data["BMI"] > 18.5) & (data["BMI"] <= 24.9), "NewBMI"] = NewBMI[1]
data.loc[(data["BMI"] > 24.9) & (data["BMI"] <= 29.9), "NewBMI"] = NewBMI[2]
data.loc[(data["BMI"] > 29.9) & (data["BMI"] <= 34.9), "NewBMI"] = NewBMI[3]
data.loc[(data["BMI"] > 34.9) & (data["BMI"] <= 39.9), "NewBMI"] = NewBMI[4]
data.loc[data["BMI"] > 39.9 ,"NewBMI"] = NewBMI[5]

def set_insulin(row):
    if row["Insulin"] >= 16 and row["Insulin"] <= 166:
        return "Normal"
    else:
        return "Abnormal"
    
data = data.assign(NewInsulinScore=data.apply(set_insulin, axis=1))

data.head()

# Some intervals were determined according to the glucose variable and these were assigned categorical variables.
NewGlucose = pd.Series(["Low", "Normal", "Overweight", "Secret", "High"], dtype = "category")
data["NewGlucose"] = NewGlucose
data.loc[data["Glucose"] <= 70, "NewGlucose"] = NewGlucose[0]
data.loc[(data["Glucose"] > 70) & (data["Glucose"] <= 99), "NewGlucose"] = NewGlucose[1]
data.loc[(data["Glucose"] > 99) & (data["Glucose"] <= 126), "NewGlucose"] = NewGlucose[2]
data.loc[data["Glucose"] > 126 ,"NewGlucose"] = NewGlucose[3]

# Here, by making One Hot Encoding transformation, categorical variables were converted into numerical values. It is also protected from the Dummy variable trap.
data = pd.get_dummies(data, columns =["NewBMI","NewInsulinScore", "NewGlucose"], drop_first = True)

categorical_data = data[['NewBMI_Obesity 1','NewBMI_Obesity 2', 'NewBMI_Obesity 3', 'NewBMI_Overweight','NewBMI_Underweight',
                     'NewInsulinScore_Normal','NewGlucose_Low','NewGlucose_Normal', 'NewGlucose_Overweight', 'NewGlucose_Secret']]

y = data["Outcome"]
x = data.drop(["Outcome",'NewBMI_Obesity 1','NewBMI_Obesity 2', 'NewBMI_Obesity 3', 'NewBMI_Overweight','NewBMI_Underweight',
                     'NewInsulinScore_Normal','NewGlucose_Low','NewGlucose_Normal', 'NewGlucose_Overweight', 'NewGlucose_Secret'], axis = 1)
cols = x.columns
index = x.index

# The variables in the data set are an effective factor in increasing the performance of the models by standardization.
# There are multiple standardization methods. These are methods such as" Normalize"," MinMax"," Robust" and "Scale".
from sklearn.preprocessing import RobustScaler
transformer = RobustScaler().fit(x)
x = transformer.transform(x)
x = pd.DataFrame(x, columns = cols, index = index)

X = pd.concat([x,categorical_data], axis = 1)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score

abc = AdaBoostClassifier()

np.mean(cross_val_score(abc,X,y,scoring='accuracy',cv=10))
abc = AdaBoostClassifier(n_estimators=1500,learning_rate=0.1)
abc.fit(x_train,y_train)
# plot_decision_boundary(abc)
y_pred=abc.predict(x_test)
print("Accuracy score",accuracy_score(y_test,y_pred))

cm = confusion_matrix(y_test, y_pred, labels=[1, 0])

TP, FN, FP, TN = cm.ravel()

print("Modified Confusion Matrix (TP in [0][0]):")
print(f"[[TP: {TP}  FN: {FN}]")
print(f" [FP: {FP}  TN: {TN}]]")
print("\nClassification Report:\n", classification_report(y_test, y_pred))
import pickle
with open("adaboost_model.pkl", "wb") as file:
    pickle.dump(abc, file)
    import pickle

# Save the scaler using pickle
with open("scaler.pkl", "wb") as f:
    pickle.dump(transformer, f)




# Step 1: Input
input_data = [2, 130, 70, 28, 100, 30.5, 0.5, 25]
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
input_df = pd.DataFrame([input_data], columns=columns)

# Step 2: BMI Category
NewBMI = pd.Series(["Underweight", "Normal", "Overweight", "Obesity 1", "Obesity 2", "Obesity 3"], dtype="category")
input_df["NewBMI"] = None
input_df.loc[input_df["BMI"] < 18.5, "NewBMI"] = NewBMI[0]
input_df.loc[(input_df["BMI"] > 18.5) & (input_df["BMI"] <= 24.9), "NewBMI"] = NewBMI[1]
input_df.loc[(input_df["BMI"] > 24.9) & (input_df["BMI"] <= 29.9), "NewBMI"] = NewBMI[2]
input_df.loc[(input_df["BMI"] > 29.9) & (input_df["BMI"] <= 34.9), "NewBMI"] = NewBMI[3]
input_df.loc[(input_df["BMI"] > 34.9) & (input_df["BMI"] <= 39.9), "NewBMI"] = NewBMI[4]
input_df.loc[input_df["BMI"] > 39.9, "NewBMI"] = NewBMI[5]

# Step 3: Insulin Score
def set_insulin(row):
    return "Normal" if 16 <= row["Insulin"] <= 166 else "Abnormal"

input_df = input_df.assign(NewInsulinScore=input_df.apply(set_insulin, axis=1))

# Step 4: Glucose Category
NewGlucose = pd.Series(["Low", "Normal", "Overweight", "Secret", "High"], dtype="category")
input_df["NewGlucose"] = None
input_df.loc[input_df["Glucose"] <= 70, "NewGlucose"] = NewGlucose[0]
input_df.loc[(input_df["Glucose"] > 70) & (input_df["Glucose"] <= 99), "NewGlucose"] = NewGlucose[1]
input_df.loc[(input_df["Glucose"] > 99) & (input_df["Glucose"] <= 126), "NewGlucose"] = NewGlucose[2]
input_df.loc[input_df["Glucose"] > 126, "NewGlucose"] = NewGlucose[3]

# Step 5: One-Hot Encoding
input_df = pd.get_dummies(input_df, columns=["NewBMI", "NewInsulinScore", "NewGlucose"], drop_first=True)

# Step 6: Ensure required dummy columns are present
required_dummies = [
    # NewBMI categories
    'NewBMI_Normal',
    'NewBMI_Obesity 1',
    'NewBMI_Obesity 2',
    'NewBMI_Obesity 3',
    'NewBMI_Overweight',
    'NewBMI_Underweight',

    # NewInsulinScore categories
    'NewInsulinScore_Abnormal',
    'NewInsulinScore_Normal',

    # NewGlucose categories
    'NewGlucose_Low',
    'NewGlucose_Normal',
    'NewGlucose_Overweight',
    'NewGlucose_Secret',
    'NewGlucose_High'
]

for col in required_dummies:
    if col not in input_df.columns:
        input_df[col] = 0

categorical_data = input_df[required_dummies]

# Step 7: Standardize numerical features
x = input_df.drop(required_dummies, axis=1)
cols = x.columns
index = x.index


x = transformer.transform(x)
x = pd.DataFrame(x, columns=cols, index=index)

# Step 8: Final input for model
X = pd.concat([x, categorical_data], axis=1)

x.head()
