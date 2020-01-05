class FlowEdge:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.conjugate = None

    def connect(self, pair: 'FlowEdge'):
        self.conjugate = pair

    def get_capacity(self):
        return self.capacity

    def send_flow(self, flow: int):
        self.capacity -= flow
        self.conjugate.capacity += flow
