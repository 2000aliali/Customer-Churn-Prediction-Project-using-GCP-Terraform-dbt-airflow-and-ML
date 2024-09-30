import pandas as pd
from sklearn.model_selection import train_test_split  # Make sure this is imported
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib# Split the dataset into training and testing sets
import pandas as pd
from sklearn.model_selection import train_test_split  # Make sure this is imported
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
df = pd.read_csv("bank_data_postgresql.csv")
df1 = pd.read_csv("bank_data_xml.csv")
# Concatenate all DataFrames
final_df = pd.concat([df, df1])

columns_to_drop = ['CustomerID', 'RowNumber', 'Surname', 'Gender', 'Age', 'Geography', 
                   'CreditScore', 'Balance', 'EstimatedSalary', 'Tenure', 
                   'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Exited']

data_cleaned = final_df.drop(columns=columns_to_drop)

# Check for any remaining missing values and handle them
print(data_cleaned.isnull().sum())

# For simplicity, we can drop rows with missing values
data_cleaned = data_cleaned.dropna()

# Display the cleaned dataset structure
print(data_cleaned.info())

from sklearn.preprocessing import LabelEncoder

# Encode the categorical columns 'geography' and 'gender'
label_encoders = {}
for column in ['geography', 'gender']:
    le = LabelEncoder()
    data_cleaned[column] = le.fit_transform(data_cleaned[column])
    label_encoders[column] = le


# Define the features (X) and the target (y)
X = data_cleaned.drop(columns=['exited', 'rownumber', 'customerid', 'surname'])  # Drop unnecessary columns
y = data_cleaned['exited']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)
print(y_pred)
# Print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

for i in range(len(y_pred)):
    if y_pred[i]==0:
        print('his is not extied')
    else :
        print('his is  extied')
    
        
    import joblib

# Save the trained model to a file
joblib.dump(model, 'random_forest_model20.pkl')

         




import joblib
from sklearn.preprocessing import LabelEncoder

# Assuming you have a dataset df for training
label_encoders = {}

# Encode 'geography' and 'gender' columns
for column in ['geography', 'gender']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Save the encoders for later use
joblib.dump(label_encoders['gender'], 'gender_label_encoder21.pkl')
joblib.dump(label_encoders['geography'], 'geography_label_encoder20.pkl')
