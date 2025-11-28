import React, { useState } from "react";
import DocumentUpload from "./components/DocumentUpload";
import QueryForm from "./components/QueryForm";
import ResultBox from "./components/ResultBox";
import "./App.css";

function App() {
  const [finalAnswer, setFinalAnswer] = useState("");

  return (
    <div className="container">
      <h1>Legal Compliance AI</h1>

      <DocumentUpload />

      <QueryForm onAnswerUpdate={setFinalAnswer} />

      <ResultBox text={finalAnswer} />
    </div>
  );
}

export default App;
