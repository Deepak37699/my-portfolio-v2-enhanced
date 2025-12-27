import React, { createContext, useContext, useState, useEffect } from 'react';
import { adminApi } from '../services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  username: string | null;
  login: (credentials: any) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    const storedUsername = localStorage.getItem('admin_username');
    if (token && storedUsername) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
    }
    setLoading(false);
  }, []);

  const login = async (credentials: any) => {
    const data = await adminApi.login(credentials);
    localStorage.setItem('admin_token', data.token);
    localStorage.setItem('admin_username', data.username);
    setIsAuthenticated(true);
    setUsername(data.username);
  };

  const logout = () => {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_username');
    setIsAuthenticated(false);
    setUsername(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, username, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
