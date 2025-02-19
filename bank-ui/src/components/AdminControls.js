import axios from "axios";
import React, { useEffect, useState } from "react";

const AdminControls = () => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get("http://localhost:5000/users");
        setUsers(response.data);
      } catch (err) {
        console.error("Error fetching users:", err);
      }
    };

    fetchUsers();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await axios.get(
        `http://localhost:5000/accounts?user_id=${selectedUserId}`
      );
      setAccounts(response.data);
    } catch (err) {
      console.error("Error fetching accounts:", err);
    }
  };

  const deleteAccount = async (accountId) => {
    try {
      const response = await axios.delete("http://localhost:5000/delete_account", {
        data: { account_id: accountId },
      });
      alert(response.data.message);
      fetchAccounts();
    } catch (err) {
      console.error("Error deleting account:", err);
    }
  };

  return (
    <div className="container">
      <h2>Admin Controls</h2>
      <div className="mb-3">
        <label className="form-label">Select User</label>
        <select
          className="form-select"
          onChange={(e) => setSelectedUserId(e.target.value)}
        >
          <option value="">Select a user</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </select>
        <button className="btn btn-primary mt-2" onClick={fetchAccounts}>
          Fetch Accounts
        </button>
      </div>
      {accounts.length > 0 && (
        <table className="table">
          <thead>
            <tr>
              <th>Account Type</th>
              <th>Balance</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((account) => (
              <tr key={account.id}>
                <td>{account.account_type}</td>
                <td>${account.balance}</td>
                <td>
                  <button
                    className="btn btn-danger"
                    onClick={() => deleteAccount(account.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdminControls;
