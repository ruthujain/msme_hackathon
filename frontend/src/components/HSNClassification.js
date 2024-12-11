import React, { useState } from "react";
import axios from "axios";

const HSNClassification = () => {
  const [description, setDescription] = useState("");
  const [hsnCode, setHsnCode] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/api/hsn_classify", { description });
      setHsnCode(response.data.hsnCode);
      setError("");
    } catch (err) {
      setError("Error classifying HSN code.");
    }
  };

  return (
    <div>
      <h3>HSN Code Classification</h3>
      <textarea 
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Enter product description"
      />
      <button onClick={handleSubmit}>Classify HSN Code</button>
      {hsnCode && <p>Classified HSN Code: {hsnCode}</p>}
      {error && <p>{error}</p>}
    </div>
  );
};

export default HSNClassification;

