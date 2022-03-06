from numbers import Number

from recommendation_types import RecommendationResult


class RecommendationResponse:
    def __init__(self, current_p, current_i, current_d, recommended_p, recommended_i, recommeneded_d, set_point,
                 graph_before, graph_after):
        self.current_p = current_p
        self.current_i = current_i
        self.current_d = current_d
        self.recommended_p = recommended_p
        self.recommended_i = recommended_i
        self.recommeneded_d = recommeneded_d
        self.set_point = set_point
        self.graph_before = graph_before
        self.graph_after = graph_after


def recommendation_response_from_recommendation_result(rec: RecommendationResult,
                                                       set_point: Number) -> RecommendationResponse:
    current_p, current_i, current_d = rec.old_pid.p, rec.old_pid.i, rec.old_pid.d
    recommended_p, recommended_i, recommeneded_d = rec.recommended_pid.p, rec.recommended_pid.i, rec.recommended_pid.d
    set_point = set_point
    graph_before = list(zip(rec.old_pid_data_points.time, rec.old_pid_data_points.amplitude))
    graph_after = list(zip(rec.recommended_pid_data_points.time, rec.recommended_pid_data_points.amplitude))
    return RecommendationResponse(
        current_p,
        current_i,
        current_d,
        recommended_p,
        recommended_i,
        recommeneded_d,
        set_point,
        graph_before,
        graph_after
    )
