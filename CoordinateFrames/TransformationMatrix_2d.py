import matplotlib.pyplot as plt
import numpy as np

# 변환 행렬 정의
transform_matrix = np.array([[2, 0],   # x 좌표에 대한 변환
                             [0, 2]])  # y 좌표에 대한 변환

# 변환할 점의 초기 좌표
initial_point = np.array([[2],
                          [3]])

# 좌표 변환 계산
transformed_point = np.dot(transform_matrix, initial_point)

# 좌표 시각화
plt.figure(figsize=(6, 6))

# 변환 전 좌표
plt.plot(initial_point[0], initial_point[1], 'bo', label='Initial Point')

# 변환 후 좌표
plt.plot(transformed_point[0], transformed_point[1], 'ro', label='Transformed Point')

plt.xlim(0, 8)
plt.ylim(0, 8)
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.title('Point Transformation Example')
plt.show()

