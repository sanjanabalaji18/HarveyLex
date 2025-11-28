import React from "react";

function ResultBox({ text }) {
  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Answer:</h3>
      <div
        style={{
          background: "#efefef",
          padding: "15px",
          borderRadius: "8px",
          minHeight: "100px",
        }}
      >
        {text}
      </div>
    </div>
  );
}

export default ResultBox;
