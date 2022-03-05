from recommendation_system.model_builder import ModelBuilder
from recommendation_system.simulator import Simulator
from recommendation_types import RecommendationRequest


class Recommendation:
    def __init__(self, algorithm):
        self.__algorithm = algorithm

    def recommend(self, request: RecommendationRequest):
        model_builder = ModelBuilder()
        model = model_builder.fit()
        def set_point(t): 
            pass
        simulator = Simulator(set_point= set_point, pid = request.pid, model= model)
        
    