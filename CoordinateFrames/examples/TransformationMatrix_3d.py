import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 3x3 변환 행렬 정의 (단위 행렬이 아닌 변환 행렬)
transform_matrix = np.array([[1, 0, 0],   # x 좌표에 대한 변환 (x 방향으로 변화 없음)
                             [0, 2, 0],   # y 좌표에 대한 변환 (y 방향으로 2배 확대)
                             [0, 0, 0.5]])  # z 좌표에 대한 변환 (z 방향으로 0.5배 축소)

# 초기 좌표 정의
initial_point = np.array([[1, 2, 3]])  # 3차원 좌표

# 좌표 변환 계산
transformed_point = np.dot(initial_point, transform_matrix)

# 변환 전 좌표와 변환 후 좌표
x_initial, y_initial, z_initial = initial_point[0, 0], initial_point[0, 1], initial_point[0, 2]
x_transformed, y_transformed, z_transformed = transformed_point[0, 0], transformed_point[0, 1], transformed_point[0, 2]

# 3D 좌표 시각화
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# 변환 전 좌표
ax.scatter(x_initial, y_initial, z_initial, c='blue', label='Initial Point')

# 변환 후 좌표
ax.scatter(x_transformed, y_transformed, z_transformed, c='red', label='Transformed Point')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.title('3D Point Transformation Example')
plt.show()
