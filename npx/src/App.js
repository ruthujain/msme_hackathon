import './App.css';
import { useState, useEffect } from 'react';
import { create } from 'ipfs-http-client';

const client = create({
  host: 'localhost',
  port: 5001,       
  protocol: 'http', 
});

function App() {
  const [fileUrl, updateFileUrl] = useState(``);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [showFiles, setShowFiles] = useState(false);

  async function onChange(e) {
    const file = e.target.files[0];
    try {
      const added = await client.add(file);
      const url = `http://localhost:8080/ipfs/${added.path}`;
      updateFileUrl(url);

      // Add to uploadedFiles list
      setUploadedFiles((prevFiles) => [
        ...prevFiles,
        { name: file.name || 'Bill of Lading', hash: added.path, url },
      ]);
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
    </div>
  );
}

export default App;

