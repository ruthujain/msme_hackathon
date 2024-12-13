import './App.css';
import { useState } from 'react';
import { create } from 'ipfs-http-client';
// import DocumentHandler from './components/DocumentHandler'; // File not found, commenting for now

const client = create({
  host: 'localhost',
  port: 5001,
  protocol: 'http',
});

function App() {
  const [fileUrl, updateFileUrl] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [showFiles, setShowFiles] = useState(false);
  const [description, setDescription] = useState('');
  const [hsnCode, setHsnCode] = useState('');
  const [responseData, setResponseData] = useState(null);

  async function sendToFlask(fileData) {
    try {
      const response = await fetch('http://localhost:5000/extract-bol-fields', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fileData),
      });

      if (response.ok) {
        const data = await response.json();
        setResponseData(data); // Save Flask response to state
        console.log('File sent to Flask successfully:', data);
      } else {
        const errorText = await response.text();
        setResponseData({ status: 'failure', message: errorText }); // Handle errors gracefully
        console.error('Error sending file to Flask:', errorText);
      }
    } catch (error) {
      setResponseData({ status: 'failure', message: error.message });
      console.error('Error in sendToFlask:', error);
    }
  }

  async function onChange(e) {
    const file = e.target.files[0];
    try {
      const added = await client.add(file);
      const url = `http://localhost:8080/ipfs/${added.path}`;
      updateFileUrl(url);
      console.log('IPFS URI:', url);

      const fileData = {
        name: file.name || 'Bill of Lading',
        hash: added.path,
        file_url: url,
      };
  
      setUploadedFiles((prevFiles) => [...prevFiles, fileData]);
  
      // Send the file data to Flask
      await sendToFlask(fileData);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }

  async function deleteFile(hash) {
    try {
      await client.pin.rm(hash); // Unpin the file from IPFS
      setUploadedFiles((prevFiles) => prevFiles.filter((file) => file.hash !== hash));
      console.log(`File with hash ${hash} deleted successfully.`);
    } catch (error) {
      console.error('Error deleting file:', error);
    }
  } 

  async function generateHsnCode() {
    if (description.trim()) {
      try {
        const response = await fetch('http://localhost:5000/predict-hscode', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description }),
        });
  
        if (response.ok) {
          const data = await response.json();
          setHsnCode(data.hscode);
        } else {
          const errorData = await response.json();
          setHsnCode(`Error: ${errorData.error}`);
        }
      } catch (error) {
        console.error('Error generating HSN code:', error);
        setHsnCode('Error: Unable to generate HSN code.');
      }
    } else {
      setHsnCode('Please enter a description');
    }
  }

  async function fetchPinnedFiles() {
    try {
      const pins = await client.pin.ls();
      const files = [];
      for await (const { cid, type } of pins) {
        if (type === 'recursive') {
          const url = `http://localhost:8080/ipfs/${cid.toString()}`;
          files.push({ name: 'Bill of Lading', hash: cid.toString(), url });
        }
      }
      setUploadedFiles(files);
    } catch (error) {
      console.error('Error fetching pinned files:', error);
    }
  }

  return (
    <div className="App">
      <nav className="navbar">
        <h2>IPFS Project Manager</h2>
      </nav>
  
      <header>
        <h3>Securely Store and Generate Unique Identifiers for Your Projects</h3>
      </header>
  
      <h1>IPFS Example with Local Node</h1>
      <input type="file" onChange={onChange} />
      {fileUrl && (
        <div>
          <h3>Uploaded File Preview</h3>
          <img src={fileUrl} width="600px" alt="Uploaded File Preview" />
          <a href={fileUrl} target="_blank" rel="noopener noreferrer">
            {fileUrl}
          </a>
        </div>
      )}
  
      <button
        onClick={() => {
          if (!showFiles) fetchPinnedFiles();
          setShowFiles(!showFiles);
        }}
        style={{
          margin: '20px 0',
          padding: '10px 20px',
          fontSize: '16px',
          cursor: 'pointer',
        }}
      >
        {showFiles ? 'Hide Uploaded Files' : 'Show Uploaded Files'}
      </button>
  
      {showFiles && (
        <div style={{ marginTop: '20px', textAlign: 'left' }}>
          <h3>Uploaded Files</h3>
          <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
            {uploadedFiles.map((file, index) => (
              <li
                key={index}
                style={{
                  padding: '10px',
                  border: '1px solid #ccc',
                  marginBottom: '10px',
                  borderRadius: '5px',
                  backgroundColor: '#f9f9f9',
                }}
              >
                <p>
                  <strong>Name:</strong> {file.name}
                </p>
                <p>
                  <strong>Hash:</strong> {file.hash}
                </p>
                <a
                  href={file.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    textDecoration: 'none',
                    color: 'white',
                    backgroundColor: '#007BFF',
                    padding: '5px 10px',
                    borderRadius: '3px',
                    marginRight: '10px',
                  }}
                >
                  View File
                </a>
                <button
                  onClick={() => deleteFile(file.hash)}
                  style={{
                    backgroundColor: 'red',
                    color: 'white',
                    border: 'none',
                    padding: '5px 10px',
                    borderRadius: '3px',
                    cursor: 'pointer',
                  }}
                >
                  Delete File
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
  
      <div>
        <h1>Bill of Lading Fields Extraction</h1>
        {/* Display Flask response */}
        {responseData && (
          <div className={`response ${responseData.status}`}>
            {responseData.status === 'success' ? (
              <>
                <h2>Extracted Fields:</h2>
                <pre>{JSON.stringify(responseData.bill_of_lading_fields, null, 2)}</pre>
              </>
            ) : (
              <p>Error: {responseData.message}</p>
            )}
          </div>
        )}
      </div>
  
      <div
        className="hsn-section"
        style={{ margin: '20px', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}
      >
        <h2 style={{ color: '#4CAF50' }}>Generate HSN Code</h2>
  
        <textarea
          placeholder="Enter description..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{
            width: '300px',
            height: '80px',
            padding: '10px',
            fontSize: '14px',
            border: '2px solid #4CAF50',
            borderRadius: '5px',
            marginBottom: '10px',
            resize: 'none',
          }}
        ></textarea>
  
        <button
          onClick={generateHsnCode}
          style={{
            backgroundColor: '#4CAF50',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            fontSize: '16px',
            cursor: 'pointer',
            marginTop: '10px',
          }}
        >
          Generate
        </button>
  
        {hsnCode && (
          <div
            style={{
              marginTop: '20px',
              padding: '15px',
              width: '300px',
              textAlign: 'center',
              fontSize: '16px',
              fontWeight: 'bold',
              border: '2px solid #4CAF50',
              borderRadius: '5px',
              backgroundColor: '#f9f9f9',
              marginLeft: 'auto',
              marginRight: 'auto',
            }}
          >
            {hsnCode}
          </div>
        )}
      </div>
  
      {/* Commenting out TradeTrust Component for now */}
      {/* <div className="tradetrust-section">
        <DocumentHandler />
      </div> */}
  
      <footer>
        <p>© 2024 IPFS Project Manager. All rights reserved.</p>
      </footer>
    </div>
  );  
}

export default App;
