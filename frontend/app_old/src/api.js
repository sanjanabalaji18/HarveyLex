const API_BASE = "http://127.0.0.1:8000";

export async function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: form
  });

  return res.json();
}

export async function askQuestion(query) {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });

  return res.json();
}
