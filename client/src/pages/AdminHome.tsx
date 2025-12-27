import React from 'react';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard } from 'lucide-react';

const AdminHome: React.FC = () => {
  const { username } = useAuth();

  return (
    <div className="admin-dashboard-home">
      <div className="welcome-banner">
        <LayoutDashboard size={48} className="banner-icon" />
        <div>
          <h1>Welcome back, {username}!</h1>
          <p>You have full control over your portfolio content from here.</p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Quick Tips</h3>
          <ul>
            <li>Keep your bio updated in the <strong>About</strong> section.</li>
            <li>Add your latest work in <strong>Projects</strong>.</li>
            <li>Check <strong>Messages</strong> for new contact inquiries.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AdminHome;
