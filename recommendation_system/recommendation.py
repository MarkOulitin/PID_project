from recommendation_system.model_builder import ModelBuilder
from recommendation_system.simulator import Simulator
from recommendation_types import PidDataPoints, RecommendationRequest, RecommendationResult


class Recommendation:
    def __init__(self, algorithm):
        self.__algorithm = algorithm

    def recommend(self, request: RecommendationRequest):
        model_builder = ModelBuilder()
        model = model_builder.fit()
        # constant function for all t >= 0
        def set_point(t): 
            if t >= 0:
                return request.set_point
            else:
                return 0
        
        simulator_old_pid = Simulator(set_point= set_point, pid = request.pid, model= model, initial_signal= request.current_sensor_value)
        time_old_pid, amplitude_old_pid = simulator_old_pid.simulate(t_limit= request.convergence_time)
        
        new_pid = self.__algorithm.recomend()
        simulator_new_pid = Simulator(set_point= set_point, pid = new_pid, model= model, initial_signal= request.current_sensor_value)
        time_new_pid, amplitude_new_pid = simulator_new_pid.simulate(t_limit= request.convergence_time)
        
        return RecommendationResult(
            old_pid= request.pid,
            old_pid_data_points= PidDataPoints(
                time = time_old_pid,
                amplitude = amplitude_old_pid
            ),
            recommended_pid= new_pid,
            recommended_pid_data_points = PidDataPoints(
                time = time_new_pid,
                amplitude= amplitude_new_pid
            )
        )
    
    