import { useState } from "react";
import { api } from "../api/client"; // Corrected import path

export default function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(""); // Reset message when a new file is selected
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    setUploading(true);
    setProgress(0);
    setMessage("");

    try {
      const response = await api.uploadDocument(file, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percentCompleted);
      });
      
      setMessage(response.data.message || "Upload successful!");
      console.log("Upload response:", response.data);

    } catch (error) {
      const errorMsg = error.response?.data?.detail || "Upload failed. Please try again.";
      setMessage(errorMsg);
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm">
      <h2 className="text-lg font-semibold mb-2">Upload Document</h2>
      <p className="text-sm text-gray-500 mb-4">Upload a PDF or DOCX file for analysis.</p>
      <div className="flex items-center space-x-2">
        <input 
          type="file" 
          onChange={handleFileChange} 
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          accept=".pdf,.docx,.txt"
        />
        <button 
          onClick={handleUpload} 
          disabled={uploading || !file}
          className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:bg-gray-400"
        >
          {uploading ? `Uploading... ${progress}%` : "Upload"}
        </button>
      </div>
      {uploading && (
        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-4">
          <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
        </div>
      )}
      {message && <p className="mt-4 text-sm text-gray-700">{message}</p>}
    </div>
  );
}
