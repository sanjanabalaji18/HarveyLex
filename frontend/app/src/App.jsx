import React, { useState, useEffect, useRef } from 'react';
import {
  Scale,
  ShieldCheck,
  Upload,
  FileText,
  Search,
  Bot,
  Zap,
  ChevronRight,
  Menu,
  X,
  Send,
  Loader2,
  CheckCircle2,
  FileCheck,
  AlertCircle,
  Gavel,
  Eye,
  Maximize2,
  Minimize2,
  Cpu,
  Database,
  ScanLine
} from 'lucide-react';
import apiClient, { api } from './api/client';

// --- Mock Data & Constants ---

const MOCK_SUGGESTIONS = [
  "Does this NDA have a non-solicitation clause?",
  "Analyze the liability cap in the attached MSA.",
  "Check for GDPR compliance regarding data processing.",
  "Summarize the termination conditions."
];

const AGENT_STEPS = [
  { id: 'extract', label: 'Extraction Agent', action: 'Isolating legal clauses...' },
  { id: 'vector', label: 'Vector Agent', action: 'Generating semantic embeddings...' },
  { id: 'analysis', label: 'Legal Analyst', action: 'Cross-referencing regulations...' },
  { id: 'draft', label: 'Drafter', action: 'Formulating compliance insight...' },
];

const INGESTION_STEPS = [
  { id: 'upload', label: 'Upload Complete', icon: Upload },
  { id: 'ocr', label: 'OCR & Text Extraction', icon: ScanLine },
  { id: 'chunk', label: 'Semantic Chunking', icon: FileText },
  { id: 'embed', label: 'Vector Embedding', icon: Cpu },
  { id: 'store', label: 'Indexing in VectorDB', icon: Database },
];

// --- Components ---

const Header = ({ onViewChange, currentView }) => (
  <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
    <div className="container mx-auto flex h-16 items-center justify-between px-4">
      <div
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => onViewChange('landing')}
      >
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white">
          <Scale size={20} strokeWidth={2.5} />
        </div>
        <span className="text-xl font-bold tracking-tight text-slate-900">HarveyLex</span>
      </div>

      <nav className="hidden md:flex items-center gap-6">
        <button className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Platform</button>
        <button className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Security</button>
        <button className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Compliance</button>
      </nav>

      <div className="flex items-center gap-3">
        {currentView === 'landing' ? (
          <button
            onClick={() => onViewChange('app')}
            className="rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white transition-all hover:bg-slate-800 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
          >
            Launch Workspace
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline-block text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full border border-emerald-100">
              ● System Operational
            </span>
            <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold border border-indigo-200">
              JD
            </div>
          </div>
        )}
      </div>
    </div>
  </header>
);

const Hero = ({ onStart }) => (
  <div className="relative overflow-hidden bg-white pt-16 pb-32">
    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-indigo-50/50 rounded-full blur-3xl -z-10" />

    <div className="container mx-auto px-4 text-center">
      <div className="inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-600 mb-8 animate-fade-in-up">
        <Zap size={14} fill="currentColor" />
        <span>Powered by Multi-Agent Architecture</span>
      </div>

      <h1 className="mx-auto max-w-4xl text-5xl font-extrabold tracking-tight text-slate-900 sm:text-6xl mb-6 leading-tight">
        Legal compliance at the speed of <span className="text-indigo-600">AI reasoning.</span>
      </h1>

      <p className="mx-auto max-w-2xl text-lg text-slate-600 mb-10 leading-relaxed">
        HarveyLex ingests complex legal documents, analyzes regulations, and delivers
        instant compliance insights using a secure, multi-agent backend.
      </p>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
        <button
          onClick={onStart}
          className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-xl transition-all hover:bg-indigo-700 hover:translate-y-[-2px]"
        >
          Start Analysis <ChevronRight size={18} />
        </button>
        <button className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-8 py-3.5 text-base font-semibold text-slate-700 hover:bg-slate-50 transition-all">
          View Documentation
        </button>
      </div>

      <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto text-left">
        {[
          { icon: FileText, title: "Smart Ingestion", desc: "Instantly chunk, clean, and embed PDFs & DOCX files." },
          { icon: Bot, title: "Agent Reasoning", desc: "Specialized agents for retrieval, analysis, and drafting." },
          { icon: ShieldCheck, title: "Compliance Check", desc: "Verify contracts against GDPR, CCPA, and custom rules." }
        ].map((feature, idx) => (
          <div key={idx} className="group p-6 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="h-12 w-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600 mb-4 group-hover:scale-110 transition-transform">
              <feature.icon size={24} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">{feature.title}</h3>
            <p className="text-slate-500 leading-relaxed">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

const DocumentSidebar = ({ documents, onUpload, activeDocId, onSelectDoc, isOpen, onClose }) => (
  <div className={`
    fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 text-slate-300 transform transition-transform duration-300 ease-in-out
    ${isOpen ? 'translate-x-0' : '-translate-x-full'} lg:relative lg:translate-x-0 border-r border-slate-800 flex flex-col
  `}>
    <div className="p-4 border-b border-slate-800 flex items-center justify-between">
      <span className="font-semibold text-white flex items-center gap-2">
        <FileCheck size={18} className="text-indigo-400" />
        Case Files
      </span>
      <button onClick={onClose} className="lg:hidden p-1 hover:bg-slate-800 rounded">
        <X size={20} />
      </button>
    </div>

    <div className="p-4">
      <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-slate-700 rounded-xl cursor-pointer hover:bg-slate-800/50 hover:border-indigo-500 transition-all group relative overflow-hidden">
        <div className="flex flex-col items-center justify-center pt-5 pb-6 z-10">
          <Upload className="w-8 h-8 mb-2 text-slate-500 group-hover:text-indigo-400" />
          <p className="text-xs text-slate-400 font-medium">Click to upload PDF</p>
        </div>
        <input type="file" className="hidden" onChange={onUpload} accept=".pdf,.docx,.doc" />
      </label>
    </div>

    <div className="flex-1 overflow-y-auto px-2">
      <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-2 mt-2">Analyzed Docs</div>
      {documents.length === 0 ? (
        <div className="px-4 py-8 text-center text-sm text-slate-600">
          No documents uploaded yet.
        </div>
      ) : (
        <ul className="space-y-1">
          {documents.map((doc) => (
            <li
              key={doc.id}
              onClick={() => onSelectDoc(doc)}
              className={`
                flex items-start gap-3 p-3 rounded-lg transition-colors cursor-pointer group
                ${activeDocId === doc.id ? 'bg-indigo-900/50 border border-indigo-500/30' : 'hover:bg-slate-800 border border-transparent'}
              `}
            >
              <div className="mt-1">
                {doc.status === 'processing' ? (
                  <Loader2 size={16} className="text-indigo-400 animate-spin" />
                ) : (
                  <FileText size={16} className={activeDocId === doc.id ? "text-indigo-300" : "text-slate-500"} />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className={`text-sm font-medium truncate ${activeDocId === doc.id ? 'text-white' : 'text-slate-200'}`}>
                  {doc.name}
                </p>
                <p className="text-xs text-slate-500 flex items-center gap-1">
                  {doc.status === 'processing' ? 'Ingesting...' : 'Ready for query'}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  </div>
);

const IngestionOverlay = ({ currentStepIndex, filename }) => (
  <div className="absolute inset-0 bg-white/95 backdrop-blur-sm z-10 flex flex-col items-center justify-center p-8 animate-fade-in">
    <div className="w-full max-w-md">
      <h3 className="text-xl font-bold text-slate-900 mb-6 text-center">Ingesting Document</h3>
      <p className="text-center text-slate-500 mb-8 font-medium">{filename}</p>

      <div className="space-y-6">
        {INGESTION_STEPS.map((step, idx) => {
          const isComplete = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <div key={step.id} className={`flex items-center gap-4 transition-all duration-300 ${isCurrent ? 'scale-105' : 'opacity-60'}`}>
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center shrink-0 border-2
                ${isComplete ? 'bg-green-100 border-green-500 text-green-600' :
                  isCurrent ? 'bg-indigo-50 border-indigo-600 text-indigo-600 animate-pulse' :
                    'bg-slate-50 border-slate-200 text-slate-300'}
              `}>
                {isComplete ? <CheckCircle2 size={20} /> : <step.icon size={20} />}
              </div>
              <div className="flex-1">
                <p className={`text-sm font-semibold ${isCurrent ? 'text-slate-900' : 'text-slate-500'}`}>{step.label}</p>
                {isCurrent && <div className="h-1 w-24 bg-slate-100 rounded-full mt-2 overflow-hidden">
                  <div className="h-full bg-indigo-600 animate-progress-bar"></div>
                </div>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  </div>
);

const PDFPreview = ({ docUrl, isIngesting, ingestionStep, filename }) => (
  <div className="h-full w-full bg-slate-100 border-l border-slate-200 flex flex-col relative overflow-hidden">
    <div className="h-12 bg-white border-b border-slate-200 flex items-center justify-between px-4 shrink-0">
      <span className="text-sm font-semibold text-slate-700 flex items-center gap-2">
        <FileText size={16} className="text-indigo-600" />
        Document Preview
      </span>
      <div className="flex gap-2">
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-500"><Minimize2 size={16} /></button>
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-500"><Maximize2 size={16} /></button>
      </div>
    </div>

    <div className="flex-1 relative bg-slate-500/10">
      {isIngesting ? (
        <IngestionOverlay currentStepIndex={ingestionStep} filename={filename} />
      ) : docUrl ? (
        <iframe
          src={docUrl}
          className="w-full h-full border-none"
          title="Document Preview"
        />
      ) : (
        <div className="absolute inset-0 flex items-center justify-center text-slate-400">
          <div className="text-center">
            <Eye size={48} className="mx-auto mb-2 opacity-20" />
            <p>Select a document to preview</p>
          </div>
        </div>
      )}
    </div>
  </div>
);

const ChatInterface = ({ messages, isProcessing, agentStep, onSend, onSuggestionClick, chatContainerRef, hasDocs }) => {
  return (
    <div className="flex-1 flex flex-col h-full bg-white relative">
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 scroll-smooth" ref={chatContainerRef}>
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center opacity-0 animate-fade-in text-center px-4">
            <div className="h-14 w-14 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6">
              <Bot size={28} className="text-indigo-600" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 mb-2">Ready to Analyze</h2>
            <p className="text-slate-500 max-w-sm mb-8 text-sm">
              I have context on the uploaded documents. Ask me about clauses, risks, or summaries.
            </p>
            {hasDocs && (
              <div className="grid grid-cols-1 gap-2 w-full max-w-md">
                {MOCK_SUGGESTIONS.map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => onSuggestionClick(suggestion)}
                    className="text-left px-4 py-3 rounded-lg bg-slate-50 border border-slate-100 text-sm text-slate-600 hover:bg-white hover:border-indigo-200 hover:shadow-sm transition-all"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 max-w-3xl ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
          >
            <div className={`
              w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm
              ${msg.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-indigo-600 border border-slate-200'}
            `}>
              {msg.sender === 'user' ? 'JD' : <Bot size={16} />}
            </div>

            <div className={`flex flex-col gap-1 min-w-0 max-w-[85%]`}>
              <div className={`
                p-3.5 rounded-2xl text-sm leading-relaxed shadow-sm
                ${msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-none'
                  : 'bg-slate-50 border border-slate-100 text-slate-800 rounded-tl-none'}
              `}>
                {msg.text.split('\n').map((line, i) => (
                  <p key={i} className={`min-h-[1rem] ${i > 0 ? 'mt-2' : ''} ${line.startsWith('•') ? 'pl-4' : ''}`}>
                    {line}
                  </p>
                ))}
              </div>

              {msg.sender === 'bot' && msg.citations && (
                <div className="flex gap-2 mt-1">
                  {msg.citations.map((cit, idx) => (
                    <span key={idx} className="inline-flex items-center gap-1 px-2 py-1 rounded bg-orange-50 border border-orange-100 text-[10px] font-medium text-orange-700 hover:bg-orange-100 cursor-pointer transition-colors">
                      <Search size={10} /> Page {cit}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isProcessing && (
          <div className="flex gap-4 max-w-3xl mr-auto animate-pulse">
            <div className="w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center shrink-0">
              <Bot size={16} className="text-slate-400" />
            </div>
            <div className="flex flex-col gap-2">
              <div className="bg-white border border-slate-200 p-3 rounded-2xl rounded-tl-none w-64 shadow-sm">
                <div className="flex items-center gap-3">
                  <Loader2 size={16} className="text-indigo-600 animate-spin" />
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                      {agentStep ? AGENT_STEPS.find(s => s.id === agentStep)?.label : 'System'}
                    </span>
                    <span className="text-xs text-slate-500">
                      {agentStep ? AGENT_STEPS.find(s => s.id === agentStep)?.action : 'Thinking...'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-white border-t border-slate-200">
        <div className="max-w-4xl mx-auto relative">
          <input
            type="text"
            placeholder={hasDocs ? "Ask a question about the document..." : "Upload a document to start..."}
            className="w-full pl-4 pr-12 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm"
            onKeyDown={(e) => e.key === 'Enter' && onSend(e.target.value)}
            disabled={!hasDocs}
            id="chat-input"
          />
          <button
            onClick={() => {
              const input = document.getElementById('chat-input');
              if (input.value) onSend(input.value);
            }}
            disabled={!hasDocs}
            className="absolute right-2 top-2 p-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm disabled:bg-slate-300"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

// --- Main App Component ---

export default function HarveyLexApp() {
  const [view, setView] = useState('landing');
  const [documents, setDocuments] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);
  const [activeDocUrl, setActiveDocUrl] = useState(null);

  // Ingestion State
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestionStepIndex, setIngestionStepIndex] = useState(0);

  // Chat State
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [agentStep, setAgentStep] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [messages, isProcessing, agentStep]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Create a Blob URL for the PDF preview
    const objectUrl = URL.createObjectURL(file);
    setActiveDocUrl(objectUrl);

    const tempId = Date.now();
    const newDoc = {
      id: tempId,
      name: file.name,
      status: 'processing'
    };

    setDocuments(prev => [newDoc, ...prev]);
    setActiveDoc(newDoc);
    setIsIngesting(true);
    setIngestionStepIndex(0);

    try {
      // Simulate steps for UI feedback while uploading
      const interval = setInterval(() => {
        setIngestionStepIndex(prev => Math.min(prev + 1, 4));
      }, 500);

      const response = await api.uploadDocument(file);
      clearInterval(interval);

      // Update doc with real ID from backend
      setDocuments(prev => prev.map(d => d.id === tempId ? { ...d, id: response.data.document_id, status: 'ready' } : d));
      setActiveDoc(prev => prev.id === tempId ? { ...prev, id: response.data.document_id, status: 'ready' } : prev);

      setIsIngesting(false);
      setIngestionStepIndex(5); // Complete

      const systemMsg = {
        id: Date.now(),
        sender: 'bot',
        text: `**Analysis Complete**: ${file.name}\n\nI have successfully extracted text, chunked the content, and updated the vector database. You can now audit this document.`
      };
      setMessages(prev => [...prev, systemMsg]);

    } catch (error) {
      console.error("Upload failed:", error);
      setIsIngesting(false);
      setDocuments(prev => prev.map(d => d.id === tempId ? { ...d, status: 'error' } : d));
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        text: `Error uploading document: ${error.message}`
      }]);
    }
  };

  const handleSend = async (text) => {
    const input = document.getElementById('chat-input');
    if (input) input.value = '';

    const userMsgId = Date.now();
    setMessages(prev => [...prev, { id: userMsgId, sender: 'user', text }]);
    setIsProcessing(true);

    // Simulate agent steps for UI
    const steps = ['extract', 'vector', 'analysis', 'draft'];
    let stepIdx = 0;
    const stepInterval = setInterval(() => {
      if (stepIdx < steps.length) {
        setAgentStep(steps[stepIdx]);
        stepIdx++;
      }
    }, 800);

    try {
      // Determine which endpoint to use based on context
      // For now, we use the new /analyse endpoint if a document is active
      let response;
      if (activeDoc && activeDoc.status === 'ready') {
        // Use the new advanced analysis endpoint
        response = await apiClient.post('/api/analyse', {
          query: text,
          session_id: "session-" + Date.now(), // Simple session ID
          file_id: activeDoc.id
        });
      } else {
        // Fallback to general analysis
        response = await apiClient.post('/api/analyze', {
          query: text,
          session_id: "session-" + Date.now()
        });
      }

      clearInterval(stepInterval);
      setAgentStep(null);
      setIsProcessing(false);

      const data = response.data;
      let botText = data.answer || data.summary || "Analysis complete.";

      // Format the response if it's from the new endpoint
      if (data.message) {
        botText = `**${data.message}**\n\n${data.summary}`;
      }

      // Extract citations/sources
      let citations = [];
      if (data.sources) {
        citations = data.sources.map((s, i) => i + 1); // Simple index based citations for now
      } else if (data.regulations) {
        citations = data.regulations.map((r, i) => i + 1);
      }

      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        text: botText,
        citations: citations
      }]);

    } catch (error) {
      clearInterval(stepInterval);
      setAgentStep(null);
      setIsProcessing(false);
      console.error("Analysis failed:", error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        sender: 'bot',
        text: `Error analyzing query: ${error.message}. Please ensure the backend is running and the document is fully processed.`
      }]);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900">
      <Header onViewChange={setView} currentView={view} />

      {view === 'landing' ? (
        <Hero onStart={() => setView('app')} />
      ) : (
        <div className="flex h-[calc(100vh-64px)] overflow-hidden">
          {/* Sidebar */}
          <DocumentSidebar
            documents={documents}
            activeDocId={activeDoc?.id}
            onSelectDoc={(doc) => setActiveDoc(doc)}
            onUpload={handleFileUpload}
            isOpen={isSidebarOpen}
            onClose={() => setIsSidebarOpen(false)}
          />

          {/* Main Area: Split Screen */}
          <main className="flex-1 flex w-full relative">
            {/* Left: Chat */}
            <div className={`flex-1 flex flex-col min-w-0 transition-all ${activeDoc ? 'w-1/2 border-r border-slate-200' : 'w-full'}`}>
              <button
                className="lg:hidden absolute top-4 right-4 z-50 p-2 bg-slate-900 text-white rounded-full shadow-lg"
                onClick={() => setIsSidebarOpen(true)}
              >
                <Menu size={20} />
              </button>

              <ChatInterface
                messages={messages}
                isProcessing={isProcessing}
                agentStep={agentStep}
                onSend={handleSend}
                onSuggestionClick={handleSend}
                chatContainerRef={chatContainerRef}
                hasDocs={documents.length > 0}
              />
            </div>

            {/* Right: PDF Preview (Only visible if doc active) */}
            {activeDoc && (
              <div className="hidden lg:block w-1/2 h-full bg-slate-100">
                <PDFPreview
                  docUrl={activeDocUrl}
                  isIngesting={isIngesting}
                  ingestionStep={ingestionStepIndex}
                  filename={activeDoc?.name}
                />
              </div>
            )}
          </main>
        </div>
      )}
    </div>
  );
}