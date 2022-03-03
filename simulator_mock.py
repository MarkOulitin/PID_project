from simulator_response import SimulatorResponse
from queryrequest import QueryRequest


class Simulator:
    def simulate(self, request: QueryRequest):
        return SimulatorResponse(request.id, request.p, 3, 4, 5, 6, 7, [8, 9])
