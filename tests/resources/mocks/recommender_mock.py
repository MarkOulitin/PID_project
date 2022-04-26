from recommendation_system.algorithm_impl.mock import MockAlgorithm
from recommendation_system.recommendation import Recommendation
from recommendation_system.types.recommendation_types import RecommendationRequest, RecommendationResult, PID, PidDataPoints


class RecommenderMock(Recommendation):
    def __init__(self):
        super().__init__(MockAlgorithm())
        self.request = None
        self.ret_value: RecommendationResult = RecommendationResult(PID(0, 0, 0),
                                                                    PidDataPoints(0, 0),
                                                                    PID(0, 0, 0),
                                                                    PidDataPoints(0, 0))

    def recommend(self, request: RecommendationRequest):
        assert self.request == request
        return self.ret_value

    def set_expected_values(self, request: RecommendationRequest, ret_value: RecommendationResult):
        self.request = request
        self.ret_value = ret_value
