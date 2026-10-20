class RecordingProvider:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def send(self, recipient, message):
        self.calls += 1
        return self.outcomes.pop(0) if self.outcomes else True
