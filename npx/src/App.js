import './App.css';
import { useState } from 'react';
import { create } from 'ipfs-http-client';
import DocumentHandler from "./components/DocumentHandler"; // Import new component

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

  async function onChange(e) {
    const file = e.target.files[0];
    try {
      // Upload the file to your local IPFS node
      const added = await client.add(file);
      const url = `http://localhost:8080/ipfs/${added.path}`; // Local gateway URL
      updateFileUrl(url);
      console.log('IPFS URI:', url);

      // Add to uploadedFiles list
      setUploadedFiles((prevFiles) => [
        ...prevFiles,
        { name: file.name || 'Bill of Lading', hash: added.path, url },
      ]);


    } catch (error) {
      console.error('Error uploading file:', error);
    }
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

  function generateHsnCode() {
    if (description.trim()) {
      // Simple logic for demonstration purposes
      const hash = description.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
      setHsnCode(`HSN-${hash.toString().slice(0, 6)}`);
    } else {
      setHsnCode('Please enter a description');
    }
  }

  async function fetchPinnedFiles() {
    try {
      const pins = await client.pin.ls();
      const files = [];
      for await (const { cid, type } of pins) {
        if (type === 'recursive') { // Only include recursive pins
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
      {/* Navigation Bar */}
      <nav className="navbar">
        <h2>IPFS Project Manager</h2>
      </nav>

      {/* Tagline */}
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

      {/* File Upload Section */}
      <div className="upload-section">
        <h1>IPFS File Upload</h1>
        <input type="file" onChange={onChange} />
        {fileUrl && (
          <div>
            <img src={fileUrl} width="600px" alt="Uploaded File Preview" />
            <a href={fileUrl} target="_blank" rel="noopener noreferrer">
              {fileUrl}
            </a>
          </div>
        )}
      </div>

      {/* Description Input Section */}
      <div className="hsn-section">
        <h2>Generate HSN Code</h2>
        <textarea
          placeholder="Enter description..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <button onClick={generateHsnCode}>Generate HSN Code</button>
        {hsnCode && <p>{hsnCode}</p>}
      </div>

      {/* Include TradeTrust Component */}
      <div className="tradetrust-section">
        <DocumentHandler />
      </div>

      {/* Footer */}
      <footer>
        <p>© 2024 IPFS Project Manager. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
