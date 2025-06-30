// App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import YachtDetails from "./pages/YachtDetails";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import BookingForm from "./pages/BookingForm"; // ✅ Import it
import Navbar from "./components/Navbar";
import './App.css';
import MyBookings from "./pages/MyBookings";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/yachts/:id" element={<YachtDetails />} />
        <Route path="/yachts/:id/book" element={<BookingForm />} /> {/* ✅ New route */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/my-bookings" element={<MyBookings />} /> {/* ✅ New route */}
        {/* Add /my-bookings later */}
      </Routes>
    </>
  );
}

export default App;
