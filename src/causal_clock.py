class CausalClock:
    def __init__(self, node_label, all_nodes):
        self.label = node_label
        self.clock = {node: 0 for node in all_nodes}

    def increment_time(self):
        self.clock[self.label] += 1

    def merge(self, other_clock):
        for node, time in other_clock.items():
            self.clock[node] = max(self.clock[node], time)
        self.increment_time()

    def is_valid_event(self, other_clock, sender):
        for node in self.clock:
            if node == sender:
                if other_clock[node] != self.clock[node] + 1:
                    return False
            else:
                if other_clock[node] > self.clock[node]:
                    return False
        return True
