import { useState, useEffect } from "react";
import API from "../api/api";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editedBooking, setEditedBooking] = useState({});

  useEffect(() => {
    API.get("/bookings/my").then((res) => setBookings(res.data));
  }, []);

  const handleDelete = async (id) => {
    if (confirm("Are you sure you want to cancel this booking?")) {
      await API.delete(`/bookings/${id}`);
      setBookings((prev) => prev.filter((b) => b.id !== id));
    }
  };

  const handleEdit = (booking) => {
    setEditingId(booking.id);
    setEditedBooking({
      start_date: booking.start_date,
      end_date: booking.end_date,
      addon_ids: booking.addons.map((a) => a.id),
    });
  };

  const handleUpdate = async () => {
    const res = await API.put(`/bookings/${editingId}`, {
      ...editedBooking,
      total_price: 999, // Recalculate total price on backend or here
      special_request: "Updated",
    });

    setBookings((prev) =>
      prev.map((b) => (b.id === res.data.id ? res.data : b))
    );
    setEditingId(null);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>My Bookings</h2>
      {bookings.map((b) => (
        <div key={b.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
          <p><strong>Yacht:</strong> {b.yacht.name}</p>
          {editingId === b.id ? (
            <>
              <input
                type="date"
                value={editedBooking.start_date}
                onChange={(e) =>
                  setEditedBooking({ ...editedBooking, start_date: e.target.value })
                }
              />
              <input
                type="date"
                value={editedBooking.end_date}
                onChange={(e) =>
                  setEditedBooking({ ...editedBooking, end_date: e.target.value })
                }
              />
              {/* TODO: Add checkboxes for addon_ids here */}
              <button onClick={handleUpdate}>Save</button>
              <button onClick={() => setEditingId(null)}>Cancel</button>
            </>
          ) : (
            <>
              <p><strong>From:</strong> {b.start_date}</p>
              <p><strong>To:</strong> {b.end_date}</p>
              <p><strong>Total:</strong> ${b.total_price}</p>
              <button onClick={() => handleEdit(b)}>✏️ Edit</button>
              <button onClick={() => handleDelete(b.id)}>🗑️ Cancel</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default MyBookings;
