import { useState } from "react";
import { useAuth } from "../context/AuthContext"; // ✅ use the hook
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { login } = useAuth();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData.username, formData.password);
      navigate("/");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="username" onChange={(e) => setFormData({ ...formData, username: e.target.value })} />
      <input name="password" type="password" onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
