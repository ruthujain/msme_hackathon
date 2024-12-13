from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=PerformanceWarning)
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import requests
from io import BytesIO
import os
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from paddleocr import PaddleOCR
from tempfile import NamedTemporaryFile

app = Flask(__name__)
CORS(app)

'''azure_endpoint = "https://liquidmindinvoice.cognitiveservices.azure.com/"
azure_key = "137454561e0c45598dee07adc71e75d1"

if not azure_key:
    print("axure key not valid")

document_analysis_client = DocumentAnalysisClient(
    endpoint=azure_endpoint, credential=AzureKeyCredential(azure_key)
)'''

# Load classifiers and vectorizer
section_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\section_classifier.pkl')
parent_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\parent_classifier.pkl')
digit_classifier = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\digit_classifier.pkl')
vectorizer = joblib.load(r'C:\Users\Ajay Kanna\Desktop\liquidmind\hackathon\tutorial\ipfs-example\src\saved_hsn_model_parameters\vectorizer.pkl')

model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

questions = [
        "What is the date on the Bill of Lading?",
        "What is the Bill of Lading (BOL) number?",
        "What is the ship from name?",
        "What is the ship to name?",
        "What is the SID?",
        "What is the CID?",
        "What is the grand total amount?"
    ]

def extract_data_from_text(ocr_text):
    extracted_data = {}
    for question in questions:
        # Use the QA pipeline to extract the answer
        result = qa_pipeline(question=question, context=ocr_text)
        extracted_data[question] = result.get("answer", "Not Available")

    return extracted_data


@app.route('/extract-bol-fields', methods=['POST'])
def extract_bol_fields():
    data = request.get_json()
    file_url = data.get('file_url')
    print(file_url)

    if not file_url:
        return jsonify({"status": "failure", "message": "No file URL provided"}), 400

    try:
        response = requests.get(file_url, timeout=10)
        if response.status_code != 200:
            return jsonify({"status": "failure", "message": f"Failed to retrieve file. HTTP status code: {response.status_code}"}), 400
        
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
            temp_image.write(response.content)
            temp_image_path = temp_image.name

        # Use PaddleOCR with the saved file path
        result = ocr.ocr(temp_image_path, det=True, rec=True)
        ocr_text = " ".join([word_info[1][0] for line in result for word_info in line])

        # Extract invoice data using the QA model
        data = extract_data_from_text(ocr_text)

        # Format the extracted data for response
        formatted_data = {key: data.get(key, 'Not Available') for key in questions}

        return jsonify({
            "status": "success",
            "bill_of_lading_fields": formatted_data,
            "formatted_bol": "\n".join([f"{key}: {value}" for key, value in formatted_data.items()])
        })

    except Exception as e:
        return jsonify({"status": "failure", "message": f"Error processing document: {str(e)}"}), 500


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
