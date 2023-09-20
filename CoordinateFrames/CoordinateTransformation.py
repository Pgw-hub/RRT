import numpy as np
import matplotlib.pyplot as plt

# 경로를 정의. 예를 들어, 간단한 경로를 생성
t = np.linspace(0, 10, 100)  # 시간 또는 위치에 대한 벡터
x = t  # 경로 x 좌표
y = np.sin(t)  # 경로 y 좌표

# 객체(object) 개수를 정의
num_objects = 5

# 객체(object)의 초기 위치를 무작위로 생성
object_x = np.random.uniform(0, 10, num_objects)
object_y = np.random.uniform(-1, 1, num_objects)

# 경로 시각화
plt.figure(figsize=(12, 6))

# 원래 경로 플롯
plt.subplot(1, 2, 1)
plt.plot(x, y, label='Path', color='blue')
plt.scatter(object_x, object_y, color='red', label='Objects (Original)')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.title('Original Path and Objects')
plt.gca().set_aspect('equal', adjustable='box')

# Frenet Frame 정보 계산
point_index = len(t) // 2
x_point = x[point_index]
y_point = y[point_index]
slope = np.gradient(y, x)[point_index]

# Frenet Frame 정보
tangent_vector = np.array([1, slope])  # 접선 벡터 (Tangent Vector)
normal_vector = np.array([-slope, 1])  # 법선 벡터 (Normal Vector)

# 객체(object)들을 Frenet Frame으로 변환하여 저장
object_frenet_x = np.zeros(num_objects)
object_frenet_y = np.zeros(num_objects)

for i in range(num_objects):
    object_relative_x = object_x[i] - x_point
    object_relative_y = object_y[i] - y_point
    object_frenet_x[i] = np.dot([object_relative_x, object_relative_y], tangent_vector)
    object_frenet_y[i] = np.dot([object_relative_x, object_relative_y], normal_vector)

# 변환된 객체(object) 시각화
plt.subplot(1, 2, 2)
plt.plot(object_frenet_x, object_frenet_y, 'go', label='Objects (Frenet Frame)')
plt.xlabel('X (Frenet Frame)')
plt.ylabel('Y (Frenet Frame)')
plt.legend()
plt.grid(True)
plt.title('Transformed Objects in Frenet Frame')
plt.gca().set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.show()
