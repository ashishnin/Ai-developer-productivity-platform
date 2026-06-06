import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api';

  const AuthContext = createContext(null);

  export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const token = localStorage.getItem('token');
      if (token) {
        authAPI.getMe()
          .then((res) => setUser(res.data))
          .catch(() => localStorage.removeItem('token'))
          .finally(() => setLoading(false));
      } else {
        setLoading(false);
      }
    }, []);

    const login = async (email, password) => {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await authAPI.login(formData);

      console.log("LOGIN RESPONSE:", res.data);

      localStorage.setItem('token', res.data.access_token);

      console.log("TOKEN SAVED:", res.data.access_token);

      const userRes = await authAPI.getMe();
      setUser(userRes.data);

      return userRes.data;
    };

    const register = async (data) => {
      const res = await authAPI.register(data);
      return res.data;
    };

    const logout = () => {
      localStorage.removeItem('token');
      setUser(null);
    };

    return (
      <AuthContext.Provider value={{ user, login, register, logout, loading }}>
        {children}
      </AuthContext.Provider>
    );
  };

  export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
      throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
  };
 