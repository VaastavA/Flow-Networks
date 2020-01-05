class FlowEdge:
    def __init__(self, capacity: int):
        assert capacity >=0 , "Capacity cannot be negative"
        self.capacity = capacity
        self.conjugate = None

    def connect(self, pair: 'FlowEdge'):
        assert pair is not None, "Conjugate Edge cannot be null"
        self.conjugate = pair

    def get_capacity(self):
        return self.capacity

    def send_flow(self, flow: int):

        assert flow > 0, "Flow cannot be negative"
        self.capacity -= flow
        self.conjugate.capacity += flow
        assert self.capacity >= 0, "Incorrect Flow change"
        assert self.conjugate.capacity >= 0, "Incorrect Flow change"
