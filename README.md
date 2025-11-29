# Project Overview - HarveyLex

**HarveyLex** is an advanced multi-agent AI system designed to revolutionize legal document compliance and drafting. Built using Google's Generative AI (Gemini) and a modular agentic architecture, HarveyLex assists legal professionals in analyzing documents, identifying compliance risks against major regulations (GDPR, HIPAA, CCPA), and drafting legally sound clauses.

## Architecture

### Problem Statement
Legal compliance is a high-stakes, labor-intensive process. Lawyers and compliance officers spend countless hours manually reviewing contracts and policies to ensure they adhere to an ever-changing landscape of regulations. This manual process is prone to human error, fatigue, and inconsistency. Furthermore, drafting compliant language that maintains the original business intent requires deep expertise and significant time, creating a bottleneck in legal workflows.

### Solution Statement
HarveyLex automates the compliance review and drafting process through a system of specialized AI agents. It ingests legal documents, understands their semantic meaning, and cross-references them against a knowledge base of regulations. By leveraging vector search and Large Language Models (LLMs), HarveyLex can pinpoint non-compliant clauses, explain *why* they are problematic, and suggest precise, legally robust rewrites. This transforms legal review from a manual line-by-line check into a streamlined, AI-augmented workflow.

### System Architecture
HarveyLex operates as an ecosystem of specialized agents and services, orchestrated by a FastAPI backend and accessible via a modern React frontend.

#### Core Agents
The intelligence of HarveyLex lies in its specialized agents, found in `ai_modules/`:

1.  **Document Inspector (`document_inspector.py`)**:
    *   **Role**: The Analyst.
    *   **Function**: Uses Gemini Pro to parse legal documents, classify clauses into categories (e.g., Liability, Data Protection, Termination), and extract key legal terms. It structures unstructured legal text for downstream analysis.

2.  **Regulation Finder (`regulation_finder.py`)**:
    *   **Role**: The Researcher.
    *   **Function**: Equipped with a Vector Store (FAISS), this agent performs semantic search to find specific regulations (GDPR, HIPAA, etc.) relevant to the analyzed clauses. It combines vector similarity with rule-based matching for high recall.

3.  **Rewrite Agent (`rewrite_agent.py`)**:
    *   **Role**: The Drafter.
    *   **Function**: Acts as an expert legal writer. It takes problematic clauses and their associated compliance issues, then uses Gemini to generate alternative wordings that satisfy regulatory requirements while preserving the original business intent.

#### Backend & Data
*   **FastAPI**: Serves as the central orchestrator, exposing REST endpoints for ingestion, analysis, and drafting.
*   **Vector Store (FAISS)**: Stores embeddings of regulations and document chunks for fast semantic retrieval.
*   **Google Gemini**: Provides the core reasoning and generation capabilities.

#### Frontend
*   **React + Vite**: A responsive, modern web interface for users to upload documents, view analysis results, and interact with the drafting assistant.
*   **Tailwind CSS**: Ensures a clean, professional, and accessible UI.

## Platform Preview

### 1. Intelligent Landing Page
*A modern, clean interface welcoming users to the AI-powered compliance platform.*
![Landing Page](assets/landing_page.png)

### 2. Document Ingestion & Processing
*Real-time feedback as documents are ingested, chunked, and embedded into the vector store.*
![Ingestion Complete](assets/ingestion_complete.png)

### 3. Deep Compliance Analysis
*Detailed risk assessment, identifying specific clauses and their potential legal implications.*
![Analysis View](assets/analysis_view.png)

## Essential Tools and Utilities

*   **Codebase Analysis & Ingestion**: Tools to read, parse, and chunk legal text from various file formats.
*   **Vector Embeddings**: Uses embedding models to convert legal text into mathematical vectors for similarity comparison.
*   **Validation Checkers**: Logic to ensure generated rewrites meet basic legal standards (e.g., checking for specific required phrases like "freely given" for consent).

## Workflow

1.  **Ingest**: The user uploads a legal document (PDF/Text). The system parses the file and splits it into analyzable chunks.
2.  **Analyze**: The **Document Inspector** classifies the clauses. Simultaneously, the **Regulation Finder** scans the vector database for relevant laws.
3.  **Review**: The user is presented with a compliance report, highlighting clauses that may violate specific regulations.
4.  **Refine**: For flagged clauses, the **Rewrite Agent** suggests compliant alternatives.
5.  **Draft**: The user selects the best rewrite or uses the drafting assistant to finalize the document.
6.  **Export**: The final, compliant document is generated for download.

## Installation

This project requires **Python 3.11+** and **Node.js**.

### Prerequisites
1.  **Google Gemini API Key**: You need a valid API key from Google AI Studio.
2.  **Virtual Environment**: Recommended to use `venv` or `uv`.

### Backend Setup
1.  Navigate to the project root.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
4.  Set up environment variables:
    Create a `.env` file and add your API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend/app
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## Running the Application

### 1. Start the Backend
From the root directory:
```bash
python backend/main.py
```
The API will be available at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

### 2. Start the Frontend
From the `frontend/app` directory:
```bash
npm run dev
```
The web application will be accessible at `http://localhost:5173`.

## Project Structure

```
harvey-lex/
├── ai_modules/                 # Core AI Agent Logic
│   ├── document_inspector.py   # Classification & Extraction
│   ├── regulation_finder.py    # Vector Search & Regulation Matching
│   └── rewrite_agent.py        # Generative Drafting
├── backend/                    # FastAPI Backend
│   ├── main.py                 # Entry point
│   ├── api/                    # API Routes
│   └── datastore/              # Data management & Vector Store
├── frontend/                   # React Frontend
│   └── app/                    # Main Application Code
├── legal_compliance_ai/        # Shared AI utilities
└── requirements.txt            # Python Dependencies
```

## Value Statement
HarveyLex significantly reduces the risk of legal non-compliance and accelerates the contract review cycle. By augmenting legal professionals with AI agents that "read" and "know" the law, it allows them to focus on high-level strategy and negotiation rather than routine compliance checking.

**Implementation**
<img width="1442" height="870" alt="image" src="https://github.com/user-attachments/assets/1f4da065-62dc-42ef-9966-9bc53e039906" />
<img width="1470" height="887" alt="image" src="https://github.com/user-attachments/assets/b8434e8c-5145-414f-b946-10cabbb0a1bd" />
<img width="1470" height="887" alt="image" src="https://github.com/user-attachments/assets/ef99858b-d36d-4a18-8fef-7d0e4624fd3b" />



