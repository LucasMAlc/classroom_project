import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin, getMeusDados } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth deve ser usado dentro de AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await getMeusDados();
        setUser(response.data);
      } catch (error) {
        if (error.response?.status === 404) {
          setUser({ username: 'admin', nome: 'Administrador', is_admin: true });
        } else {
          console.error('Erro ao carregar usuário:', error);
          logout();
        }
      }
    }
    setLoading(false);
  };

  const login = async (username, password) => {
    try {
      const response = await apiLogin(username, password);
      localStorage.setItem('token', response.data.access);
      await loadUser();
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Erro ao fazer login',
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const isAdmin = () => {
    return user?.username === 'admin' || user?.is_admin === true;
  };

    return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAdmin }}>
      {children}
    </AuthContext.Provider>
  );
};