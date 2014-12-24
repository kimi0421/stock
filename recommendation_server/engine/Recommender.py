import pandas as pd
from cvxopt import matrix, solvers


class Recommender:

    def __init__(self, df):
        self.df = df
        self.e = df['e'].tolist()
        self.sigma = df['sigma'].tolist()
        self.n = len(self.df)

    def __create_matrix_A__(self):
        A = []
        for i in xrange(self.n):
            zeros = [0] * self.n
            zeros[i] = -1
            function = [-1 * self.e[i], 1] + zeros
            A.append(function)
        return matrix(A)

    def __create_matrix_b__(self, expectation):
        zeros = [0] * self.n
        all_functions = [-1 * expectation, 1] + zeros
        b = matrix(all_functions)
        return b

    def __create_matrix_c__(self):
        c = matrix(self.sigma)
        return c

    def optimize(self, expectation):
        A = self.__create_matrix_A__()
        b = self.__create_matrix_b__(expectation)
        c = self.__create_matrix_c__()
        sol = solvers.lp(c, A, b)
        return sol


if __name__ == '__main__':

    df = pd.DataFrame({'e':[0.2, 0.3, 0.4], 'sigma':[0.15, 0.2, 0.3]}, index=[0, 1, 2])
    rec = Recommender(df)
    sol = rec.optimize(0.35)
    import ipdb; ipdb.set_trace()





