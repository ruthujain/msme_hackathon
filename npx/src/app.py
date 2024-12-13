from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=PerformanceWarning)

app = Flask(__name__)
CORS(app)

# Load classifiers and vectorizer
section_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\section_classifier.pkl')
parent_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\parent_classifier.pkl')
digit_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\digit_classifier.pkl')
vectorizer = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\vectorizer.pkl')

def predict_hscode(description):
    description_vectorized = vectorizer.transform([description])
    description_df = pd.DataFrame(description_vectorized.toarray())

    # Align columns with expected features
    expected_columns = [str(i) for i in range(section_classifier.n_features_in_)]
    for col in expected_columns:
        if col not in description_df.columns:
            description_df[col] = 0

    # Reorder columns to match training
    description_df = description_df[expected_columns]

    predicted_section = section_classifier.predict(description_vectorized)[0]
    description_df['predicted_section'] = predicted_section

    predicted_parent = parent_classifier.predict(description_df)[0]
    description_df['predicted_parent'] = predicted_parent

    predicted_2_digits = digit_classifier.predict(description_df)[0]
    hscode = f"{predicted_parent}{predicted_2_digits}"
    return hscode

@app.route('/predict-hscode', methods=['POST'])
def predict_hscode_api():
    data = request.json
    description = data.get('description', '')
    if not description.strip():
        return jsonify({'error': 'Description cannot be empty'}), 400

    try:
        hscode = predict_hscode(description)
        return jsonify({'hscode': hscode})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
