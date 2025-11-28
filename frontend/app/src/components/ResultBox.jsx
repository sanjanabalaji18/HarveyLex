
export default function ResultBox({ response }) {
  // Helper function to render a part of the response
  const renderSection = (title, content) => {
    if (!content) return null;

    const renderContent = () => {
      if (typeof content === 'object' && content !== null) {
        return (
          <pre className="bg-gray-100 p-2 rounded text-xs whitespace-pre-wrap">
            {JSON.stringify(content, null, 2)}
          </pre>
        );
      }
      return <p className="text-gray-700">{String(content)}</p>;
    };

    return (
      <div className="mb-4">
        <h3 className="font-semibold text-md mb-1">{title}</h3>
        {renderContent()}
      </div>
    );
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm mt-4 bg-white">
      <h2 className="text-lg font-bold mb-4">Analysis Results</h2>
      {!response ? (
        <div className="text-center text-gray-500">
          <p>Your analysis results will appear here...</p>
        </div>
      ) : (
        <div>
          {renderSection("Risk Score", response.risk_score)}
          {renderSection("Query", response.query)}
          {renderSection("Compliance Results", response.compliance_results)}
          {renderSection("Retrieved Regulations", response.retrieved_regulations)}
          {renderSection("Reasoning Chain", response.reasoning_chain)}
          {renderSection("Document ID", response.document_id)}
        </div>
      )}
    </div>
  );
}
