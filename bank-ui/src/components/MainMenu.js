import axios from "axios";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const MainMenu = () => {
  const [accounts, setAccounts] = useState([]);
  const [amount, setAmount] = useState(0);
  const [selectedAccountId, setSelectedAccountId] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch accounts from the backend
    const fetchAccounts = async () => {
      try {
        const response = await axios.get("http://localhost:5000/accounts");
        setAccounts(response.data);
      } catch (err) {
        console.error("Error fetching accounts:", err);
      }
    };

    fetchAccounts();
  }, []);

  const handleDeposit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/deposit", {
        account_id: selectedAccountId,
        amount: parseFloat(amount),
      });
      setMessage(response.data.message);
      setAccounts((prev) =>
        prev.map((acc) =>
          acc.id === selectedAccountId
            ? { ...acc, balance: acc.balance + parseFloat(amount) }
            : acc
        )
      );
    } catch (err) {
      console.error("Error depositing:", err);
    }
  };

  const handleWithdraw = async () => {
    try {
      const response = await axios.post("http://localhost:5000/withdraw", {
        account_id: selectedAccountId,
        amount: parseFloat(amount),
      });
      setMessage(response.data.message);
      setAccounts((prev) =>
        prev.map((acc) =>
          acc.id === selectedAccountId
            ? { ...acc, balance: acc.balance - parseFloat(amount) }
            : acc
        )
      );
    } catch (err) {
      console.error("Error withdrawing:", err);
    }
  };

  return (
    <div className="container">
      <h2>Main Menu</h2>
      {message && <p className="text-success">{message}</p>}
      <div className="mb-3">
        <label className="form-label">Select Account</label>
        <select
          className="form-select"
          onChange={(e) => setSelectedAccountId(parseInt(e.target.value))}
        >
          <option value="">Select an account</option>
          {accounts.map((account) => (
            <option key={account.id} value={account.id}>
              {account.account_type} - ${account.balance}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-3">
        <label className="form-label">Amount</label>
        <input
          type="number"
          className="form-control"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </div>
      <button className="btn btn-success me-2" onClick={handleDeposit}>
        Deposit
      </button>
      <button className="btn btn-warning" onClick={handleWithdraw}>
        Withdraw
      </button>
      <button
  className="btn btn-info"
  onClick={() => navigate(`/transactions/${selectedAccountId}`)}
  disabled={!selectedAccountId}
>
  View Transactions
</button>

    </div>
  );
};

export default MainMenu;
