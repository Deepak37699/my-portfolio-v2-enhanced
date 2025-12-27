import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  FolderKanban, 
  Trophy, 
  MessageSquare, 
  UserCircle, 
  LogOut,
  ChevronLeft
} from 'lucide-react';

const AdminLayout: React.FC = () => {
  const { logout, username } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/admin', icon: LayoutDashboard, end: true },
    { name: 'Projects', path: '/admin/projects', icon: FolderKanban },
    { name: 'Skills', path: '/admin/skills', icon: Trophy },
    { name: 'Messages', path: '/admin/messages', icon: MessageSquare },
    { name: 'About', path: '/admin/about', icon: UserCircle },
  ];

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <NavLink to="/" className="back-link">
            <ChevronLeft size={20} /> Site
          </NavLink>
          <div className="admin-user">
            <div className="user-avatar">AD</div>
            <span>{username}</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.end}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            >
              <item.icon size={20} />
              {item.name}
            </NavLink>
          ))}
        </nav>

        <button onClick={handleLogout} className="logout-btn">
          <LogOut size={20} /> Logout
        </button>
      </aside>

      <main className="admin-main">
        <header className="admin-topbar">
          <h2>Admin Management</h2>
        </header>
        <div className="admin-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AdminLayout;
