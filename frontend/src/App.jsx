import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState(null);

  const API_URL = "/api"; // ← Cambiar esto (sin window.location.origin)

  const handleUpload = async () => {
    if (!files) return;

    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append("files", file));

    try {
      setLoading(true);
      await axios.post(`${API_URL}/upload`, formData);
      alert("Archivos subidos correctamente");
      setFiles(null);
    } catch (error) {
      alert("Error al subir archivos: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: input,
      });

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error al procesar la consulta: " + error.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Sistema RAG - RRHH</h1>

        <div className="upload-section">
          <input
            type="file"
            multiple
            onChange={(e) => setFiles(e.target.files)}
          />
          <button onClick={handleUpload} disabled={loading || !files}>
            Subir Archivos
          </button>
        </div>

        <div className="chat-container">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
              {msg.sources && (
                <div className="sources">
                  <small>
                    Fuentes: {msg.sources.map((s) => s.filename).join(", ")}
                  </small>
                </div>
              )}
            </div>
          ))}
          {loading && <div className="message assistant">Pensando...</div>}
        </div>

        <div className="input-section">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="Escribe tu pregunta..."
            disabled={loading}
          />
          <button onClick={handleSend} disabled={loading || !input.trim()}>
            Enviar
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
