import { useState, useEffect } from "react";
import API from "../api/api";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editedBooking, setEditedBooking] = useState({});
  const [addons, setAddons] = useState([]);

  useEffect(() => {
    API.get("/bookings/my").then((res) => setBookings(res.data));
    API.get("/addons").then((res) => setAddons(res.data));
  }, []);

  const handleDelete = async (id) => {
    if (confirm("Cancel booking?")) {
      await API.delete(`/bookings/${id}`);
      setBookings((prev) => prev.filter((b) => b.id !== id));
    }
  };

  const handleEdit = (booking) => {
    setEditingId(booking.id);
    setEditedBooking({
      yacht_id: booking.yacht.id,
      yacht_price: booking.yacht.price, // ✅ Save yacht daily price
      start_date: booking.start_date,
      end_date: booking.end_date,
      addon_ids: booking.addons.map((a) => a.id || a.addon?.id),
      total_price: booking.total_price,
      special_request: booking.special_request || "",
    });
  };

  const handleCheckboxChange = (id) => {
    const selected = editedBooking.addon_ids || [];
    const updated = selected.includes(id)
      ? selected.filter((a) => a !== id)
      : [...selected, id];
    setEditedBooking({ ...editedBooking, addon_ids: updated });
  };

  const handleUpdate = async () => {
    const validAddonIds = addons.map((a) => a.id);
    const filteredAddons = (editedBooking.addon_ids || []).filter((id) =>
      validAddonIds.includes(id)
    );

    const selectedAddons = addons.filter((a) =>
      filteredAddons.includes(a.id)
    );
    const addonCost = selectedAddons.reduce((sum, a) => sum + a.price, 0);

    // ✅ Calculate number of days
    const startDate = new Date(editedBooking.start_date);
    const endDate = new Date(editedBooking.end_date);
    const diffDays = Math.ceil(
      (endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (diffDays <= 0) {
      alert("End date must be after start date.");
      return;
    }

    const yachtDailyPrice = editedBooking.yacht_price || 0;
    const yachtCost = yachtDailyPrice * diffDays;

    const total = yachtCost + addonCost;

    const payload = {
      ...editedBooking,
      addon_ids: filteredAddons,
      total_price: total,
    };

    console.log("📤 Final payload:", payload);

    try {
      await API.put(`/bookings/${editingId}`, payload, {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });

      const res = await API.get("/bookings/my");
      setBookings(res.data);
      setEditingId(null);
    } catch (err) {
      console.error("❌ Update failed:", err.response?.data || err.message);
      alert("Update failed.");
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>My Bookings</h2>
      {bookings.map((b) => (
        <div
          key={b.id}
          style={{ border: "1px solid #ccc", marginBottom: 10, padding: 10 }}
        >
          <p>
            <strong>Yacht:</strong> {b.yacht.name}
          </p>
          {editingId === b.id ? (
            <>
              <input
                type="date"
                value={editedBooking.start_date}
                onChange={(e) =>
                  setEditedBooking({
                    ...editedBooking,
                    start_date: e.target.value,
                  })
                }
              />
              <input
                type="date"
                value={editedBooking.end_date}
                onChange={(e) =>
                  setEditedBooking({
                    ...editedBooking,
                    end_date: e.target.value,
                  })
                }
              />

              <div>
                <strong>Add-ons:</strong>
                {addons.map((a) => (
                  <div key={a.id}>
                    <label>
                      <input
                        type="checkbox"
                        checked={
                          editedBooking.addon_ids?.includes(a.id) || false
                        }
                        onChange={() => handleCheckboxChange(a.id)}
                      />
                      {a.name} (${a.price})
                    </label>
                  </div>
                ))}
              </div>

              <button onClick={handleUpdate}>💾 Save</button>
              <button onClick={() => setEditingId(null)}>Cancel</button>
            </>
          ) : (
            <>
              <p>
                <strong>From:</strong> {b.start_date}
              </p>
              <p>
                <strong>To:</strong> {b.end_date}
              </p>
              <p>
                <strong>Add-ons:</strong>{" "}
                {b.addons.length > 0
                  ? b.addons
                      .map((a) => a.name || a.addon?.name)
                      .filter(Boolean)
                      .join(", ")
                  : "None"}
              </p>
              <p>
                <strong>Total:</strong> ${b.total_price}
              </p>
              <button onClick={() => handleEdit(b)}>✏️ Edit</button>
              <button onClick={() => handleDelete(b.id)}>🗑️ Delete</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default MyBookings;
