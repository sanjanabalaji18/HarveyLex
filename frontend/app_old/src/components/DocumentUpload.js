import React, { useState } from "react";
import { uploadDocument } from "../api";

function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const upload = async () => {
    if (!file) return;
    setStatus("Uploading...");
    const result = await uploadDocument(file);
    setStatus(result.message || "Uploaded!");
  };

  return (
    <div>
      <h3>Upload Legal Document</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
      <p>{status}</p>
    </div>
  );
}

export default DocumentUpload;
