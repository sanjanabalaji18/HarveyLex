from typing import List, Dict, Any
from datastore.vector_store.vector_store import VectorStore
from backend.datastore.embedding_utils import EmbeddingService



class RegulationFinder:
    """
    Finds relevant regulations and legal references for given clauses.
    Uses vector similarity search against a knowledge base of regulations.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.embedder = EmbeddingService()
        self.regulations_db = self._load_regulations()

    def _load_regulations(self) -> List[Dict[str, Any]]:
        """
        Load predefined regulations into memory.
        In production, this would load from a database or file.
        """
        return [
            {
                "id": "gdpr_5_1_e",
                "text": "Personal data must not be retained longer than necessary.",
                "document": "GDPR",
                "article": "5(1)(e)",
                "scope": "retention"
            },
            {
                "id": "gdpr_6_1",
                "text": "Processing requires consent or clear legal basis.",
                "document": "GDPR",
                "article": "6(1)",
                "scope": "lawful_basis"
            },
            {
                "id": "gdpr_7_1",
                "text": "Consent must be freely given, specific, informed and unambiguous.",
                "document": "GDPR",
                "article": "7(1)",
                "scope": "consent"
            },
            {
                "id": "hipaa_164_308",
                "text": "Organizations must prevent, detect, and correct security violations.",
                "document": "HIPAA",
                "article": "164.308",
                "scope": "security"
            },
            {
                "id": "ccpa_1798_100",
                "text": "Consumers have the right to know what personal information is collected.",
                "document": "CCPA",
                "article": "1798.100",
                "scope": "transparency"
            }
        ]

    def find_matches(self, clauses: List[str]) -> List[Dict[str, Any]]:
        """
        Find relevant regulations for each clause.
        Returns a list of matches with similarity scores.
        """
        results = []

        for i, clause in enumerate(clauses):
            clause_embedding = self.embedder.embed_text(clause)
            matches = self.vector_store.search(clause_embedding, top_k=3)

            # If no matches in vector store, use rule-based matching
            if not matches:
                matches = self._rule_based_match(clause)

            results.append({
                "clause_index": i,
                "clause_text": clause,
                "matches": matches
            })

        return results

    def _rule_based_match(self, clause: str) -> List[Dict[str, Any]]:
        """
        Fallback rule-based matching when vector search fails.
        """
        matches = []
        clause_lower = clause.lower()

        for reg in self.regulations_db:
            score = 0
            reg_text_lower = reg["text"].lower()

            # Simple keyword matching
            keywords = reg_text_lower.split()
            for keyword in keywords:
                if keyword in clause_lower:
                    score += 1

            if score > 0:
                matches.append({
                    "regulation": reg,
                    "similarity": min(score / len(keywords), 1.0)
                })

        return sorted(matches, key=lambda x: x["similarity"], reverse=True)[:3]

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Direct search for regulations by text query.
        """
        query_embedding = self.embedder.embed_text(query)
        return self.vector_store.search(query_embedding, top_k=top_k)
