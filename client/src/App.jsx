// App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import YachtDetails from "./pages/YachtDetails";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Navbar from "./components/Navbar"; // add this
import './App.css';

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/yachts/:id" element={<YachtDetails />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        {/* Add more routes as needed */}
      </Routes>
    </>
  );
}

export default App;
