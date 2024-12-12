import axios from "axios";

// Endpoints from TradeTrust documentation
const STORAGE_URL = process.env.REACT_APP_TRADETRUST_STORAGE_URL;
const VERIFY_URL = process.env.REACT_APP_TRADETRUST_VERIFY_URL;

// Function to upload a document to the storage endpoint
export const uploadDocument = async (document) => {
  try {
    const response = await axios.post(STORAGE_URL, document, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data; // Return file storage details
  } catch (error) {
    console.error("Error uploading document:", error);
    throw error;
  }
};

// Function to verify a document using its hash
export const verifyDocument = async (documentHash) => {
  try {
    const response = await axios.post(
      VERIFY_URL,
      { documentHash },
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    return response.data; // Return verification result
} catch (error) {
    console.error("Error uploading document:", error);
    if (error.response) {
      console.error("API Response:", error.response.data); // Log API error details
    }
    throw error;
  }
  

};
