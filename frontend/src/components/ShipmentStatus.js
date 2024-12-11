import React, { useState } from "react";
import axios from "axios";

const ShipmentStatus = () => {
  const [shipmentId, setShipmentId] = useState("");
  const [status, setStatus] = useState("");

  const checkStatus = async () => {
    try {
      const response = await axios.post("http://localhost:5000/api/release_payment", { shipment_id: shipmentId });
      setStatus(response.data.status);
    } catch (err) {
      setStatus("Error fetching status.");
    }
  };

  return (
    <div>
      <h3>Shipment Status</h3>
      <input
        type="text"
        value={shipmentId}
        onChange={(e) => setShipmentId(e.target.value)}
        placeholder="Enter Shipment ID"
      />
      <button onClick={checkStatus}>Check Status</button>
      {status && <p>{status}</p>}
    </div>
  );
};

export default ShipmentStatus;
