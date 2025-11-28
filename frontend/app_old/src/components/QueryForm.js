import React, { useState } from "react";
import { askQuestion } from "../api";

function QueryForm({ onAnswerUpdate }) {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");

  const submit = async () => {
    if (!query.trim()) return;
    setStatus("Thinking...");
    const result = await askQuestion(query);
    setStatus("");
    onAnswerUpdate(result.answer || "No response");
  };

  return (
    <div>
      <h3>Ask a Legal Question</h3>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
      />
      <button onClick={submit}>Ask</button>
      <p>{status}</p>
    </div>
  );
}

export default QueryForm;
