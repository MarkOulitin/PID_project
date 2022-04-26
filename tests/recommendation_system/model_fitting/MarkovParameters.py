from control import tf
from pandas import read_excel
from recommendation_system.model_builder import ModelBuilder

def main():
    data_file_path = '../data/simulationData.xlsx'
    data = read_excel(data_file_path)
    print(data)
    # tf_nominator = [1]
    # tf_denominator = [1, 20, 100]
    # model = tf(tf_nominator, tf_denominator)
    # model_builder = ModelBuilder()
    # infered_model = model_builder.fit()
    # print('initial model')
    # print(model)
    # print('infered model')
    # print(infered_model)
if __name__ == "__main__":
    main()
