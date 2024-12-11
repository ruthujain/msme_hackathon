import pandas as pd
from hsn_classifier import classify_hsn

def get_valid_hsn_codes(dataset_path):
    try:
        # Load the dataset
        df = pd.read_csv(dataset_path)

        # Check for valid HSN codes (assuming the column is named 'hsn_code')
        # If 'hsn_code' is different, replace it with the correct column name
        unique_hsn_codes = df['category'].unique()

        # If there are invalid or missing HSN codes, handle them
        missing_hsn = df[df['category'].isnull()]
        if not missing_hsn.empty:
            print(f"Warning: Missing HSN codes found: \n{missing_hsn}")

        invalid_hsn = df[~df['category'].str.isnumeric()]
        if not invalid_hsn.empty:
            print(f"Warning: Invalid HSN codes found: \n{invalid_hsn}")

        return list(unique_hsn_codes)
    
    except Exception as e:
        return {"error": f"An error occurred while loading the dataset: {str(e)}"}

def validate_compliance(description, valid_hsn_codes):
    try:
        # Get HSN code from the classifier
        hsn_code = classify_hsn(description)

        if hsn_code == "Unknown":
            raise ValueError("HSN code could not be classified. Please check the product description.")

        # Check if the HSN code is in the valid HSN codes list
        if hsn_code not in valid_hsn_codes:
            raise ValueError(f"Invalid HSN code: {hsn_code}. Please check the product description.")
        
        return hsn_code

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Path to your dataset file (CSV)
    dataset_path = r'C:\Users\aman\Downloads\compliance_automation\upc_corpus_reduced.csv'

    # Get valid HSN codes from the dataset
    valid_hsn_codes = get_valid_hsn_codes(dataset_path)
    
    if isinstance(valid_hsn_codes, list):
        description = "Cotton fabric roll for textile manufacturing"
        
        try:
            hsn_code = validate_compliance(description, valid_hsn_codes)
            print(f"Valid HSN code for '{description}': {hsn_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(valid_hsn_codes['error'])  # In case there was an error loading the dataset
