import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AdminControls from "./components/AdminControls";
import LoginPage from "./components/LoginPage";
import MainMenu from "./components/MainMenu";
import SignupPage from "./components/SignupPage";
import TransactionHistory from "./components/TransactionHistory";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/menu" element={<MainMenu />} />
        <Route path="/transactions/:accountId" element={<TransactionHistory />} />
        <Route path="/admin" element={<AdminControls />} />
      </Routes>
    </Router>
  );
}

export default App;
