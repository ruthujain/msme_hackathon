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
    } catch (error) {
      console.error('Error uploading file:', error);
    }
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
  /* this is a dummy fn for hsn add the actual oen!*/
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
