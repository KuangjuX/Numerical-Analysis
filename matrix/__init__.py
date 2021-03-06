import numpy as np

class Matrix:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector
        self.m = len(self.matrix)
        self.n = self.m

    def _swap_matrix_row(self, i: int, j: int):
        temp = self.matrix[i].copy()
        self.matrix[i] = self.matrix[j]
        self.matrix[j] = temp

    def _swap_vector_row(self, i: int, j: int):
        temp = self.vector[i].copy()
        self.vector[i] = self.vector[j]
        self.vector[j] = temp

    def random_non_singular_matrix(size):
        random_matrix = np.random.rand(size, size) * 100
        random_vector = np.random.rand(1, size) * 100
        return (random_matrix, random_vector[0])

    # 以列为主元的高斯消元法
    def _gaussian_elimination(self):
        for i in range(0, self.m):
            # 从第 0 行 至最后一行进行消元
            max_element = self.matrix[i][i]
            max_pos = i
            for j in range(i + 1, self.m):
                # 从当前行向后寻找最大的主元
                if self.matrix[j][i] > max_element:
                    max_element = self.matrix[j][i]
                    max_pos = j 
            if max_pos != i:
                # 如果最大的列元素不在当前行，则交换当前行与列元素最大所在行
                self._swap_matrix_row(i, max_pos)
                self._swap_vector_row(i, max_pos)
            
            # 交换行之后进行高斯消元
            for k in range(i + 1, self.m):
                # 计算消元系数
                a_k = self.matrix[k][i] / self.matrix[i][i]
                self.matrix[k] -= a_k * self.matrix[i]
                self.vector[k] -= a_k * self.vector[i]
        
        # 消元后进行回代
        res = []
        for i in range(0, self.m):
            index = self.m - i - 1
            x = self.vector[index]
            for j in range(0, i):
                yindex = self.m - j - 1
                x -= res[j] * self.matrix[index][yindex]
            x = x / self.matrix[index][index]
            res.append(x)
        res = list(reversed(res))
        return res

    def gaussian_slove(self):
        return self._gaussian_elimination()

    # LU 矩阵分解
    def _LU_decomposition(self):
        # 初始化 LU 矩阵
        L = np.array([[0.0 for _ in range(0, self.m)] for _ in range(0, self.m)])
        U = np.array([[0.0 for _ in range(0, self.m)] for _ in range(0, self.m)])

        # 迭代求解 LU 矩阵的系数
        for r in range(0, self.m):
            L[r][r] = 1
            if r == 0:
                U[0] = self.matrix[0]
                for i in range(1, self.m):
                    L[i][0] = self.matrix[i][0] / U[0][0]
            else:
                for i in range(r, self.m):
                    sum = 0
                    for k in range(0, r):
                        sum += L[r][k] * U[k][i]
                    U[r][i] = self.matrix[r][i] - sum
                for i in range(r + 1, self.m):
                    sum = 0
                    for k in range(0, r):
                        sum += L[i][k] * U[k][r]
                    L[i][r] = (self.matrix[i][r] - sum) / U[r][r]
        y = np.linalg.solve(L, self.vector)
        x = np.linalg.solve(U, y)
        return (L, U, x)
                    

    def LU_decomposition_slove(self):
        return self._LU_decomposition()

    # 高斯-塞德尔迭代
    def gauss_seidel(self, x0, delta):
        x = x0  
        count = 0
        while True:  
            count += 1
            max_err = 0.0
            for i in range(self.n):
                old_sum = 0.0
                new_sum = 0.0
                for j in range(0, i):
                    new_sum += self.matrix[i][j] * x[j]
                for j in range(i + 1, self.n):
                    old_sum += self.matrix[i][j] * x[j]
                old_xi = x[i]
                x[i] = (self.vector[i] - old_sum - new_sum)/self.matrix[i][i]
                err = abs(old_xi - x[i])
                max_err = max(max_err, err)
            if max_err < delta:
                break
            max_err = 0
        return (x, count)


    def sor(self, x0, omega, delta):
        x = x0  
        count = 0
        while True:  
            count += 1
            max_err = 0.0
            for i in range(self.n):
                old_sum = 0.0
                new_sum = 0.0
                for j in range(0, i):
                    new_sum += self.matrix[i][j] * x[j]
                for j in range(i, self.n):
                    old_sum += self.matrix[i][j] * x[j]
                old_xi = x[i]
                x[i] = x[i] + omega * (self.vector[i] - old_sum - new_sum)/self.matrix[i][i]
                err = abs(x[i] - old_xi)
                max_err = max(max_err, err)
            if max_err < delta:
                break
            max_err = 0
        return (x, count)

    # 使用 numpy 计算的线性方程组的解，用来和我们计算的比较
    def slove(self):
        return np.linalg.solve(self.matrix, self.vector)





