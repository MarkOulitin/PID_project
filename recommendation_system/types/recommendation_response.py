from numbers import Number
from typing import List

from recommendation_system.types.recommendation_types import RecommendationResult, SimulationData


class RecommendationResponse:
    def __init__(self, current_p, current_i, current_d, recommended_p, recommended_i, recommended_d, set_point,
                 graph_before, graph_after):
        self.current_p = current_p
        self.current_i = current_i
        self.current_d = current_d
        self.recommended_p = recommended_p
        self.recommended_i = recommended_i
        self.recommended_d = recommended_d
        self.set_point = set_point
        before_min = graph_before[0][0]
        before_max = graph_before[len(graph_before) - 1][0]
        after_min = graph_after[0][0]
        after_max = graph_after[len(graph_after) - 1][0]
        self.graph_before = list(map(lambda entry: (__normalize__(entry[0], before_min, before_max), entry[1]), graph_before))
        self.graph_after = list(map(lambda entry: (__normalize__(entry[0], after_min, after_max), entry[1]), graph_after))

    def __eq__(self, other):
        return self.current_p == other.current_p and self.current_i == other.current_i and \
               self.current_d == other.current_d and self.recommended_p == other.recommended_p and \
               self.recommended_i == other.recommended_i and self.recommended_d == other.recommended_d and \
               self.set_point == other.set_point and self.graph_before == other.graph_before and \
               self.graph_after == other.graph_after


def __normalize__(value, min, max):
    if min == max:
        return 1
    return ((value - min) / (max - min)) * 100


def recommendation_response_from_recommendation_result(rec: RecommendationResult,
                                                       set_point: Number) -> RecommendationResponse:
    current_p, current_i, current_d = rec.old_pid.p, rec.old_pid.i, rec.old_pid.d
    recommended_p, recommended_i, recommended_d = rec.recommended_pid.p, rec.recommended_pid.i, rec.recommended_pid.d
    set_point = set_point
    graph_before = list(zip(rec.old_pid_data_points.time, rec.old_pid_data_points.amplitude))
    graph_after = list(zip(rec.recommended_pid_data_points.time, rec.recommended_pid_data_points.amplitude))
    return RecommendationResponse(
        current_p,
        current_i,
        current_d,
        recommended_p,
        recommended_i,
        recommended_d,
        set_point,
        graph_before,
        graph_after
    )


# Used for default response in-case of tests
def default_recommendation_response(p, i, d, set_point, simulation_data: List[SimulationData]):
    graph_before = list(zip(list(map(lambda entry: entry.timestamp, simulation_data)),
                            list(map(lambda entry: entry.process_value, simulation_data))))
    graph_after = list(zip(list(map(lambda entry: entry.timestamp, simulation_data)),
                           list(map(lambda entry: entry.process_value + 1, simulation_data))))
    return RecommendationResponse(
        p, i, d,
        p + 1, i + 1, d + 1,
        set_point if set_point != "" else "1",
        graph_before,
        graph_after
    )
