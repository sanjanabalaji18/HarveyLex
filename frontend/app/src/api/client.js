
import axios from 'axios';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: '/api', // The base URL for all API requests
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * API client for interacting with the backend.
 */
export const api = {
  /**
   * Uploads a document for ingestion.
   * @param {File} file - The file to upload.
   * @param {Function} onUploadProgress - Callback for upload progress.
   * @returns {Promise<any>} The response from the server.
   */
  uploadDocument: (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    return apiClient.post('/ingest/upload-document/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
  },

  /**
   * Analyzes a document.
   * @param {string} documentId - The ID of the document to analyze.
   * @param {string} query - The user's query for the analysis.
   * @returns {Promise<any>} The analysis results.
   */
  analyzeDocument: (documentId, query) => {
    return apiClient.post('/analyse', {
      file_id: documentId,
      query: query,
      session_id: "session-" + Date.now()
    });
  },

  /**
   * Rewrites a clause.
   * @param {string} clause - The clause to rewrite.
   * @param {string} issue - The issue with the clause.
   * @param {string} context - The context of the clause.
   * @returns {Promise<any>} The rewritten suggestions.
   */
  rewriteClause: (clause, issue, context) => {
    return apiClient.post('/drafting/rewrite-clause/', {
      clause,
      issue,
      context,
    });
  },
};

export default apiClient;
