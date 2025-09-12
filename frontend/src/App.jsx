import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        query: query,
        top_k: 5,
        embed_model: "all-MiniLM-L6-v2",
      });

      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("❌ Error: Could not fetch response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h1>JioPay Assistant</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask me something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Ask"}
        </button>
      </form>
      <div style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
        {answer && (
          <>
            <h3>Answer:</h3>
            <p>{answer}</p>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
