// src/context/AuthContext.jsx

import { createContext, useContext, useState, useEffect } from "react";
import API from "../api/api"; // using your configured axios instance

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Check session on mount
  useEffect(() => {
    API.get("/auth/check_session")
      .then((res) => setUser(res.data))
      .catch(() => setUser(null));
  }, []);

  // Login function
  const login = async (username, password) => {
    const res = await API.post("/auth/login", { username, password });
    setUser(res.data);
  };

  // Logout function
  const logout = async () => {
    await API.delete("/auth/logout");
    setUser(null);
  };

  // Signup function
  const signup = async (username, email, password) => {
    const res = await API.post("/auth/signup", { username, email, password });
    setUser(res.data);
  };
  

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
