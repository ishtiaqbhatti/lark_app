// This is a new file. Create it with the following content:
import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/authService';

export const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authToken, setAuthToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        setAuthToken(storedToken);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error("Failed to read authToken from localStorage:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const login = async (password) => {
    const response = await apiLogin(password);
    if (response && response.token) {
      try {
        localStorage.setItem('authToken', response.token);
        setAuthToken(response.token);
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Failed to store authToken in localStorage:", error);
        // Even if localStorage fails, keep session in memory for current tab
        setAuthToken(response.token);
        setIsAuthenticated(true);
      }
    } else {
      throw new Error('No token received');
    }
  };

  const logout = async () => {
    try {
      await apiLogout();
      localStorage.removeItem('authToken');
      setAuthToken(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error("Logout failed:", error);
      // Even if API logout fails, clear local state
      localStorage.removeItem('authToken');
      setAuthToken(null);
      setIsAuthenticated(false);
      throw error; // Re-throw to allow component to show error
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, authToken, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
