import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';
import { Mail, Calendar, MessageSquare } from 'lucide-react';

const MessageManager: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const data = await adminApi.getMessages();
      setMessages(data);
    } catch (error) {
      console.error('Failed to fetch messages');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="manager-container">
      <div className="manager-header">
        <h2>Inbox</h2>
      </div>

      <div className="messages-list">
        {messages.length === 0 ? (
          <div className="no-items">
            <MessageSquare size={48} />
            <p>No messages yet.</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className="message-card">
              <div className="message-header">
                <div className="sender-info">
                  <div className="sender-avatar">{msg.name[0]}</div>
                  <div>
                    <h4>{msg.name}</h4>
                    <p><Mail size={14} /> {msg.email}</p>
                  </div>
                </div>
                <div className="message-meta">
                  <Calendar size={14} /> {new Date(msg.created_date).toLocaleDateString()}
                </div>
              </div>
              <div className="message-body">
                <h5>Subject: {msg.subject}</h5>
                <p>{msg.message}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default MessageManager;
