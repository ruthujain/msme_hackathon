import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
df = pd.read_csv('C:/Users/aman/Downloads/compliance_automation/upc_corpus_reduced.csv')
df = df[['description', 'category']]

# Remove rows where 'description' is missing
df = df.dropna(subset=['description'])

# Handle missing HSN codes (category column)
missing_hsn = df[df['category'].isnull()]
if not missing_hsn.empty:
    print(f"Warning: Missing HSN codes found: \n{missing_hsn}")

# Fill missing values in 'category' with 'Unknown'
df['category'].fillna('Unknown', inplace=True)

# Ensure the 'category' column is of type string (to prevent issues with LabelEncoder)
df['category'] = df['category'].astype(str)

# Encode 'category' if it's categorical
le = LabelEncoder()
df['category'] = le.fit_transform(df['category'])

# Split dataset into train and validation sets
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Preprocess text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))  # Added stop_words and ngram_range
X_train = vectorizer.fit_transform(train_df['description'])
X_val = vectorizer.transform(val_df['description'])

y_train = train_df['category']
y_val = val_df['category']

# Initialize Random Forest Regressor with hyperparameters
model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=10, min_samples_split=10)

# Stratified KFold cross-validation
skf = StratifiedKFold(n_splits=2, random_state=42, shuffle=True)  # Stratified KFold to handle class imbalance

# Hyperparameter tuning example using GridSearchCV with StratifiedKFold
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 10],
}

grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=skf,
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)

# Print best parameters and score from grid search
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_}")

# Train the model with the best parameters found from grid search
best_model = grid_search.best_estimator_

# Train the best model on the entire training data
best_model.fit(X_train, y_train)

# Save the trained model and vectorizer
joblib.dump(best_model, 'hsn_model.pkl')  # Save the trained RandomForest model
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')  # Save the TF-IDF vectorizer

print("Model and vectorizer saved successfully.")

# Make predictions
y_pred = best_model.predict(X_val)

# Evaluate the model using Mean Squared Error (MSE) and R-squared (R2)
mse = mean_squared_error(y_val, y_pred)
r2 = r2_score(y_val, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Function to classify HSN code
def classify_hsn(description):
    try:
        # Preprocess the description text using the TF-IDF vectorizer
        description_vector = vectorizer.transform([description])

        # Predict the category (HSN code) using the trained model
        predicted_category = best_model.predict(description_vector)

        # Return the predicted HSN code (category)
        return predicted_category[0] if predicted_category else "Unknown"
    
    except Exception as e:
        return "Unknown"

# Example of using classify_hsn to validate a description
description = "Cotton fabric roll for textile manufacturing"
hsn_code = classify_hsn(description)
print(f"HSN code for the description '{description}': {hsn_code}")
