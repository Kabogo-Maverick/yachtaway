import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const { signup } = useAuth();
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(formData.username, formData.email, formData.password);
      navigate("/");
    } catch (err) {
      alert("Signup failed: " + (err.response?.data?.error || "Unknown error"));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create an Account</h2>
      <input placeholder="Username" onChange={(e) => setFormData({ ...formData, username: e.target.value })} />
      <input placeholder="Email" onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
      <input placeholder="Password" type="password" onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default Signup;
