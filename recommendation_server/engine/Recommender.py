import numpy as np
import pandas as pd
from cvxopt import matrix, solvers
# from statsmodels.stats.correlation_tools import cov_nearest

RAW_FILE_LOCATION = 'output/stock_raw_data/'

class Recommender:

    def __init__(self, df, forecast_length):
        self.df = df
        self.e = df['e'].tolist()
        self.sigma = df['sigma'].tolist()
        self.n = len(self.df)
        self.cov = self.__create_cov__(forecast_length)

    @staticmethod
    def __get_return_data__(symbol, n):
        df = pd.read_csv(RAW_FILE_LOCATION + symbol + '.csv')
        return np.array(df['Adj Return'][-n:])

    def __create_cov__(self, n):
        symbols = self.df.index
        data = [self.__get_return_data__(symbol, n) for symbol in symbols]
        # Make all the data the same length
        data_length = min([len(i) for i in data])
        data = [i[-data_length:] for i in data]
        return matrix(np.cov(data))

    # def __create_matrix_A__(self):
    #     A = []
    #     for i in xrange(self.n):
    #         zeros = [0] * self.n
    #         zeros[i] = -1
    #         function = [-1 * self.e[i], 1] + zeros
    #         A.append(function)
    #     return matrix(A)
    #
    # def __create_matrix_b__(self, expectation):
    #     zeros = [0] * self.n
    #     all_functions = [-1 * expectation, 1] + zeros
    #     b = matrix(all_functions)
    #     return b
    #
    # def __create_matrix_c__(self):
    #     c = matrix(self.sigma)
    #     return c

    def __create_matrix_q__(self):
        q = matrix(np.zeros((self.n, 1)))
        return q

    def __create_matrix_G__(self):
        G = matrix(np.concatenate((-np.transpose(matrix(self.e)),
                                   -np.identity(self.n)), 0))
        return G

    def __create_matrix_h__(self, expectation):
        h = matrix(np.concatenate((-np.ones((1, 1)) * expectation,
                                   np.zeros((self.n, 1))), 0))
        return h

    def optimize(self, expectation):
        P = self.cov
        q = self.__create_matrix_q__()
        G = self.__create_matrix_G__()
        h = self.__create_matrix_h__(expectation)
        A = matrix(1.0, (1, self.n))
        b = matrix(1.0)
        sol = solvers.qp(P, q, G, h, A, b)
        return sol

if __name__ == '__main__':

    df = pd.DataFrame({'e': [0.2, 0.3, 0.4], 'sigma': [0.15, 0.2, 0.3]}, index=['AAPL', 'GOOG', 'BABA'])
    rec = Recommender(df, 760)
    rec.__create_cov__(760)
    sol = rec.optimize(0.31)
    import ipdb; ipdb.set_trace()





