import './App.css';
import { useState } from 'react';
import { create } from 'ipfs-http-client';

const client = create({
  host: 'localhost',
  port: 5001,       
  protocol: 'http', 
});

function App() {
  const [fileUrl, updateFileUrl] = useState(``);

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

  return (
    <div className="App">
      <h1>IPFS Example with Local Node</h1>
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
  );
}

export default App;

