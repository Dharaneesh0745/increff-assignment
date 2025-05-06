import { useState, useRef, useEffect } from 'react';

export default function HomePage() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Send the user's query to the backend
      const res = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),  // Sending message to backend
      });

      // Check for successful response
      if (!res.ok) {
        throw new Error('Failed to fetch response from the server');
      }

      const data = await res.json();

      // Handle the bot's response
      const botMessage = { sender: 'bot', text: data.reply || 'No response from bot.' };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error contacting server.' }]);
    }

    setInput(''); 
  };

  const reloadChat = () => {
    setMessages([]);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="relative h-screen w-full bg-gray-100 p-4">
      <h1 className="text-4xl font-bold">Welcome to the Home Page</h1>

      {/* Chatbot Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg"
      >
        Chatbot
      </button>

      {/* Chat Popup */}
      {isChatOpen && (
        <div className="fixed bottom-16 right-4 w-80 bg-white border rounded-lg shadow-lg flex flex-col h-96">
          {/* Header with Reload and Close */}
          <div className="bg-blue-600 text-white px-4 py-2 rounded-t-lg flex justify-between items-center">
            <span>Chat with us</span>
            <div className="flex items-center space-x-2">
              {/* Reload Icon */}
              <button
                onClick={reloadChat}
                className="text-white hover:text-gray-200 text-lg font-bold"
                title="Reload"
              >
                &#x21bb;
              </button>
              {/* Close Icon */}
              <button
                onClick={toggleChat}
                className="text-white hover:text-gray-200 text-lg font-bold"
                title="Close"
              >
                &times;
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-2 space-y-2">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`text-sm p-2 rounded max-w-xs break-words whitespace-pre-wrap overflow-hidden ${
                  msg.sender === 'user' ? 'bg-blue-100 self-end' : 'bg-gray-200 self-start'
                }`}
              >
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="flex p-2 border-t">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 border rounded px-2 py-1 mr-2"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-600 text-white px-3 py-1 rounded"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
