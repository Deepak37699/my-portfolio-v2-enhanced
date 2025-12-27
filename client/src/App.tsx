import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AnimatePresence, motion } from 'framer-motion';
import Navbar from './components/Navbar';
import AdminLayout from './components/AdminLayout';
import Home from './pages/Home';
import About from './pages/About';
import Projects from './pages/Projects';
import Skills from './pages/Skills';
import Contact from './pages/Contact';
import Login from './pages/Login';
import AdminHome from './pages/AdminHome';
import ProjectManager from './pages/ProjectManager';
import SkillManager from './pages/SkillManager';
import MessageManager from './pages/MessageManager';
import AboutManager from './pages/AboutManager';

const PageWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
};

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" />;
  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  const location = useLocation();
  
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        {/* Public Routes */}
        <Route path="/" element={<><Navbar /><PageWrapper><Home /></PageWrapper></>} />
        <Route path="/about" element={<><Navbar /><PageWrapper><About /></PageWrapper></>} />
        <Route path="/projects" element={<><Navbar /><PageWrapper><Projects /></PageWrapper></>} />
        <Route path="/skills" element={<><Navbar /><PageWrapper><Skills /></PageWrapper></>} />
        <Route path="/contact" element={<><Navbar /><PageWrapper><Contact /></PageWrapper></>} />
        <Route path="/login" element={<PageWrapper><Login /></PageWrapper>} />

        {/* Admin Routes */}
        <Route path="/admin" element={
          <ProtectedRoute>
            <AdminLayout />
          </ProtectedRoute>
        }>
          <Route index element={<PageWrapper><AdminHome /></PageWrapper>} />
          <Route path="projects" element={<PageWrapper><ProjectManager /></PageWrapper>} />
          <Route path="skills" element={<PageWrapper><SkillManager /></PageWrapper>} />
          <Route path="messages" element={<PageWrapper><MessageManager /></PageWrapper>} />
          <Route path="about" element={<PageWrapper><AboutManager /></PageWrapper>} />
        </Route>
      </Routes>
    </AnimatePresence>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <AppRoutes />
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
