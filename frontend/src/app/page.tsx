'use client';

import { useState } from 'react';

interface Message {
  sender: 'user' | 'agent';
  text: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userPrompt = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userPrompt }]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userPrompt }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { sender: 'agent', text: data.response }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: 'agent', text: 'Error connecting to agent backend.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col h-screen max-w-3xl mx-auto p-4 bg-gray-50 text-gray-900">
      <header className="py-4 border-b border-gray-200 mb-4">
        <h1 className="text-2xl font-bold text-gray-800">Local AI Agent Framework</h1>
        <p className="text-sm text-gray-500">Ollama (qwen2.5:3b)</p>
      </header>

      {/* Chat Message Window */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-2">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            Ask a question or request a calculation to trigger tools!
          </div>
        )}
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-md px-4 py-2 rounded-lg ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-200 text-gray-800 shadow-sm'
              }`}
            >
              <span className="block font-semibold text-xs opacity-75 mb-1">
                {msg.sender === 'user' ? 'You' : 'Agent'}
              </span>
              <p className="whitespace-pre-wrap text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 px-4 py-2 rounded-lg shadow-sm text-sm text-gray-500 animate-pulse">
              Agent is thinking & executing tools...
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="What is 15 plus 27, then multiply that result by 3?"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          Send
        </button>
      </form>
    </main>
  );
}