import pandas as pd

# Load the dataset
data_file_path = r"C:\Users\aman\Downloads\compliance_automation\upc_corpus.csv"
data = pd.read_csv(data_file_path)

# Reduce the dataset to 2000 rows
reduced_data = data.head(2000)

# Save the reduced dataset to a new file
reduced_file_path = r"C:\Users\aman\Downloads\compliance_automation\upc_corpus_reduced.csv"
reduced_data.to_csv(reduced_file_path, index=False)

print(f"Reduced dataset saved at: {reduced_file_path}")

