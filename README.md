# 🕰️ Vector Clock Causal KV Store - Distributed Systems Assignment

This repository contains the implementation of a **Causally Consistent Distributed Key-Value Store** using **Vector Clocks**. Built entirely in **Python** and containerized with **Docker** and **Docker Compose**, this project was developed as part of the *Fundamentals of Distributed Systems* course at IIT Jodhpur.

---

## 📌 Problem Statement

The goal is to move beyond simple event ordering (like Lamport timestamps) and accurately capture **causal relationships** between events in a distributed system. Using **Vector Clocks**, we ensure that if **event B is causally dependent on event A**, all nodes will process **A before B**.

---

## 🛠️ Tech Stack

- 🐍 Python (Flask, requests)
- 🐳 Docker & Docker Compose
- ⏱️ Vector Clock-based causal consistency
- 🔁 Simulated 3-node network

---

## 📁 Folder Structure

vector-clock-kv-store/
├── src/
│ ├── service_node.py # Flask API node logic with buffering & vector clock
│ ├── causal_clock.py # VectorClock class and causal rules
│ └── test_client.py # Scenario-based client to test causal consistency
├── Dockerfile # Builds a node container
├── compose-run.yml # Defines 3-node Docker Compose network
├── project_report.pdf # Detailed report with screenshots & architecture
└── README.md # This file


---

## 🚀 How to Run the Project

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/vector-clock-kv-store.git
cd vector-clock-kv-store


2️⃣ Build & Launch the Nodes

docker-compose -f compose-run.yml up --build

This will spin up 3 nodes: X, Y, and Z, on ports 6000, 6001, and 6002.

3️⃣ Run the Test Client

In a separate terminal:
cd src
python test_client.py

This will simulate writes across nodes and demonstrate delayed/buffered writes when causal dependencies are not yet met.


🧪 Sample Output Highlights

    ✅ Writes are delayed if causal dependencies aren’t satisfied

    📦 Buffered messages are eventually applied when dependencies resolve

    ✅ Final key-values across nodes show causal order is preserved


📚 Project Report

The full report is included in project_report.pdf, detailing:

    System architecture

    Vector Clock algorithm and logic

    Docker containerization and setup

    Screenshots proving causal consistency

    Final system behavior analysis


🙋‍♂️ Author

Mohamed Bin Badhusha E B
M.Tech Data Engineering, IIT Jodhpur

