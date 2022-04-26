from numbers import Number

from recommendation_system.types.recommendation_types import RecommendationResult


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
        self.graph_before = graph_before
        self.graph_after = graph_after

    def __eq__(self, other):
        return self.current_p == other.current_p and self.current_i == other.current_i and \
               self.current_d == other.current_d and self.recommended_p == other.recommended_p and \
               self.recommended_i == other.recommended_i and self.recommended_d == other.recommended_d and \
               self.set_point == other.set_point and self.graph_before == other.graph_before and \
               self.graph_after == other.graph_after


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
