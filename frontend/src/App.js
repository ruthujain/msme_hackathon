import React, { useState } from "react";
import HSNClassification from "./components/HSNClassification";
import DepositForm from "./components/DepositForm";
import ShipmentStatus from "./components/ShipmentStatus";

const App = () => {
  return (
    <div>
      <h1>MSME Trade Finance Platform</h1>
      <HSNClassification />
      <DepositForm />
      <ShipmentStatus />
    </div>
  );
};

export default App;
