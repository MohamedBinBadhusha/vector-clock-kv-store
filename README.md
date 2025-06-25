# 🕒 Vector Clock Based Causally Consistent Key-Value Store

This project implements a **distributed key-value store** using **Vector Clocks** to maintain **causal consistency** across multiple nodes.  
Built with **Python (Flask)** and containerized using **Docker + Docker Compose**, this system simulates a real-world causally consistent database.

---

## 📌 Features

- 🧠 Vector Clock implementation for event tracking
- 🕸️ Multi-node communication with causal message ordering
- ⏳ Buffering of writes until causal dependencies are satisfied
- 📦 Local key-value storage at each node
- 🔁 Verification via a custom client script

---

## 📂 Project Structure

