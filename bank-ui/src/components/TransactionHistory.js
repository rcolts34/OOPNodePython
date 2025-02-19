import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const TransactionHistory = () => {
  const { accountId } = useParams();
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/transactions?account_id=${accountId}`
        );
        setTransactions(response.data);
      } catch (err) {
        console.error("Error fetching transactions:", err);
      }
    };

    if (accountId) fetchTransactions();
  }, [accountId]);

  return (
    <div className="container">
      <h2>Transaction History</h2>
      {transactions.length === 0 ? (
        <p>No transactions available.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Amount</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((txn) => (
              <tr key={txn.id}>
                <td>{txn.transaction_type}</td>
                <td>${txn.amount}</td>
                <td>{txn.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TransactionHistory;
