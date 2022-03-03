import json


class SimulatorResponse:
    def __init__(self, current_p, current_i, current_d, recommended_p, recommended_i, recommeneded_d, set_point,
                 points):
        self.current_p = current_p
        self.current_i = current_i
        self.current_d = current_d
        self.recommended_p = recommended_p
        self.recommended_i = recommended_i
        self.recommeneded_d = recommeneded_d
        self.set_point = set_point
        self.points = points

