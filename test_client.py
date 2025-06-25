import requests
import time

# Endpoints of running nodes
nodes = {
    'X': 'http://localhost:6000',
    'Y': 'http://localhost:6001',
    'Z': 'http://localhost:6002'
}

def post_with_log(node_label, path, payload):
    print(f"\n🔁 Sending to Node {node_label} at {nodes[node_label]}{path}")
    try:
        response = requests.post(nodes[node_label] + path, json=payload, timeout=5)
        print(f"✅ Node {node_label} says:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"❌ Node {node_label} request failed:", str(e))
    except Exception:
        print(f"❌ Node {node_label} raw response:", response.text)

def get_with_log(node_label, key):
    try:
        result = requests.get(nodes[node_label] + "/retrieve", params={"key": key}, timeout=5)
        print(f"📦 Node {node_label} →", result.json())
    except requests.exceptions.RequestException as e:
        print(f"❌ Node {node_label} retrieve failed:", str(e))
    except Exception:
        print(f"❌ Node {node_label} raw response:", result.text)

# Step 1: Node X performs first write
clock_X = {'X': 1, 'Y': 0, 'Z': 0}
print("🟢 Writing x=100 from Node X")
post_with_log('X', '/store', {
    "key": "x",
    "value": "100",
    "clock": clock_X,
    "origin": "X"
})

# Wait to simulate network delay and allow local processing
time.sleep(1)

# Manual sync: Send Node X's write to Node Y to avoid causality conflict
print("\n🔁 Syncing Node X's write to Node Y")
post_with_log('Y', '/store', {
    "key": "x",
    "value": "100",
    "clock": clock_X,
    "origin": "X"
})

# Wait a moment before next write
time.sleep(1)

# Step 2: Node Y performs write that depends on Node X's write
clock_Y = {'X': 1, 'Y': 2, 'Z': 0}
print("\n🟠 Writing x=200 from Node Y (causally dependent)")
post_with_log('Y', '/store', {
    "key": "x",
    "value": "200",
    "clock": clock_Y,
    "origin": "Y"
})

# Wait for async clock processing
time.sleep(2)

# Step 3: Read values from all nodes
print("\n🔵 Final key state from all nodes:")
for label in nodes:
    get_with_log(label, "x")
