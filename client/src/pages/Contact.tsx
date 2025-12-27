import React, { useState } from 'react';
import { portfolioApi } from '../services/api';
import { Send, MapPin, Mail } from 'lucide-react';

const Contact: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [status, setStatus] = useState<{ type: 'success' | 'error' | null, message: string }>({ type: null, message: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await portfolioApi.sendMessage(formData);
      setStatus({ type: 'success', message: 'Message sent successfully!' });
      setFormData({ name: '', email: '', subject: '', message: '' });
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to send message. Please try again.' });
    }
  };

  return (
    <div className="section-modern">
      <div className="container">
        <h2 className="section-title">Get In Touch</h2>
        <p className="section-subtitle">Have a question or want to work together?</p>
        
        <div className="contact-grid">
          <div className="contact-info">
            <div className="contact-item">
              <Mail className="contact-icon" />
              <div>
                <h3>Email</h3>
                <p>contact@example.com</p>
              </div>
            </div>
            <div className="contact-item">
              <MapPin className="contact-icon" />
              <div>
                <h3>Location</h3>
                <p>San Francisco, CA</p>
              </div>
            </div>
          </div>

          <form className="contact-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <input 
                type="text" 
                placeholder="Name" 
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required 
              />
            </div>
            <div className="form-group">
              <input 
                type="email" 
                placeholder="Email" 
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required 
              />
            </div>
            <div className="form-group">
              <input 
                type="text" 
                placeholder="Subject" 
                value={formData.subject}
                onChange={(e) => setFormData({...formData, subject: e.target.value})}
                required 
              />
            </div>
            <div className="form-group">
              <textarea 
                placeholder="Message" 
                rows={5}
                value={formData.message}
                onChange={(e) => setFormData({...formData, message: e.target.value})}
                required
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary">
              Send Message <Send size={20} />
            </button>
            {status.type && (
              <div className={`status-message ${status.type}`}>
                {status.message}
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default Contact;
