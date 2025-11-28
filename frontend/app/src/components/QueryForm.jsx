import { useState } from "react";
import { api } from "../api/client"; // Corrected import path

export default function QueryForm({ documentId, setResponse }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalysis = async () => {
    if (!query) {
      setError("Please enter a query.");
      return;
    }
    if (!documentId) {
      setError("Please upload and select a document first.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null); // Clear previous response

    try {
      const res = await api.analyzeDocument(documentId, query);
      setResponse(res.data);
      console.log("Analysis response:", res.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Analysis failed.";
      setError(errorMsg);
      console.error("Analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm mt-4">
      <h2 className="text-lg font-semibold mb-2">Run Analysis</h2>
      <p className="text-sm text-gray-500 mb-4">
        Ask a question about the uploaded document (e.g., "Does this contract comply with GDPR?").
      </p>
      <div className="space-y-3">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your compliance query here..."
          rows={3}
          className="w-full p-2 border rounded-md"
          disabled={loading}
        />
        <button 
          onClick={handleAnalysis} 
          disabled={loading || !query || !documentId}
          className="px-4 py-2 bg-green-500 text-white rounded-md disabled:bg-gray-400"
        >
          {loading ? "Analyzing..." : "Run Analysis"}
        </button>
      </div>
      {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
    </div>
  );
}
