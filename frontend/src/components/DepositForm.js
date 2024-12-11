import React, { useState } from "react";
import axios from "axios";

const DepositForm = () => {
  const [amount, setAmount] = useState("");

  const handleDeposit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/api/deposit_funds", { amount });
      console.log("Deposit successful:", response.data);
    } catch (err) {
      console.log("Error depositing funds:", err);
    }
  };

  return (
    <div>
      <h3>Deposit Funds</h3>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Enter amount"
      />
      <button onClick={handleDeposit}>Deposit</button>
    </div>
  );
};

export default DepositForm;
