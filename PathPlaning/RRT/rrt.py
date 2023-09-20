import numpy as np
import matplotlib.pyplot as plt
import time

class Node(object):
    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.parent = None
    
    def set_parent(self, parent) : # 각 노드마다 부모를 정의함.
        self.parent = parent

class RRT(object) :
    def __init__(self, start, goal, space, obstacle_list, success_dist_thres = 1.0):
        self.start_node = Node(start[0], start[1])
        self.goal_node = Node(goal[0],goal[1])
        self.space = space
        self.obstacle_list = obstacle_list
        self.node_list = []

        #options
        self.max_iter = 500000
        self.goal_sample_rate = 0.1
        self.min_u = 1.0
        self.max_u = 3.0
        self.success_dist_thres = success_dist_thres
        self.collision_check_step = 0.2
        self.stepsize = 0.5

    def plan(self):
        self.node_list = [self.start_node]
        for i in range(self.max_iter) :
            #Get random node
            rand_node = self.get_random_node()
            #Find_neareast node
            nearest_node = self.find_nearest_node(self.node_list, rand_node)
            #Create new node
            u = self.stepsize*self.get_random_input(self.min_u, self.max_u)
            new_node = self.create_child_node(nearest_node, rand_node, u)
            #Collision check(Node, Path)
            node_collide = self.is_collide(new_node, self.obstacle_list)
            if node_collide :
                continue
            collide = self.is_path_collide(nearest_node, new_node, self.obstacle_list, self.collision_check_step)
            if collide :
                continue
            #Add to tree
            new_node.set_parent(nearest_node)
            self.node_list.append(new_node)
            #Goal check
            goal_reached = self.check_goal(
                new_node, self.success_dist_thres)
            if goal_reached:
                print("[-] GOAL REACHED!!")
                return self.backtrace_path(new_node)
        return None
        

    @staticmethod #이렇게하면 그냥 클래스이름으로 호출할 수 있음. 
    def is_same_node(node1, node2):
        if(node1.x == node2.x) and (node1.y == node2.y):
            return True
        else:
            return False
    
    def backtrace_path(self, node):
        current_node = node
        path = [current_node]
        reached_start_node = self.is_same_node(current_node, self.start_node)
        while not reached_start_node:
            current_node = current_node.parent
            path.append(current_node)
            reached_start_node = self.is_same_node(current_node, self.start_node)
        return path[::-1]
        
    def get_random_node(self):
        min_x, max_x, min_y, max_y = self.space
        if np.random.rand() > self.goal_sample_rate:
            rand_x = np.random.uniform(min_x, max_x)
            rand_y = np.random.uniform(min_y, max_y)
            rand_node = Node(rand_x, rand_y)
            return rand_node
        else:
            return self.goal_node
        
    def check_goal(self, node, success_dist_thres) :
        dx = node.x - self.goal_node.x
        dy = node.y - self.goal_node.y
        dist = np.sqrt(dx*dx + dy*dy)

        if (dist < success_dist_thres):
            return True
        else :
            return False
        
    @staticmethod
    def create_child_node(nearest_node, rand_node, u):
        dx = rand_node.x - nearest_node.x
        dy = rand_node.y - nearest_node.y
        mag = np.sqrt(dx*dx + dy*dy)

        direction_x = dx/mag
        direction_y = dy/mag

        new_x = nearest_node.x + u * direction_x
        new_y = nearest_node.y + u * direction_y
        new_node = Node(new_x, new_y)
        return new_node
    
    @staticmethod
    def get_random_input(min_u, max_u) :
        return np.random.uniform(min_u, max_u)
    
    @staticmethod
    def find_nearest_node(node_list, rand_node):
        min_index = 0
        min_dist = 1e9
        for i in range(len(node_list)):
            node = node_list[i]
            dx = rand_node.x - node.x
            dy = rand_node.y - node.y
            dist = np.sqrt(dx*dx + dy*dy)

            if dist < min_dist:
                min_dist = dist
                min_index = i
        
        return node_list[min_index]
    
    @staticmethod
    def is_collide(node, obstacle_list):
        for obstacle in obstacle_list:
            obs_x, obs_y, r = obstacle

            dx = node.x - obs_x
            dy = node.y - obs_y
            dist = np.sqrt(dx*dx+dy*dy)
            if (dist < r):
                return True

        return False

    @staticmethod
    def is_path_collide(node_from, node_to, obstacle_list, check_step=0.2):
        dx = node_to.x - node_from.x
        dy = node_to.y - node_from.y
        length = np.sqrt(dx*dx + dy*dy)

        direction_x = dx/length
        direction_y = dy/length

        nodes_to_check = [node_from, node_to]

        if length >=check_step:
            n_add = int(np.floor(length / check_step))
            for i in range(n_add):
                step_node_x = node_from.x + check_step * direction_x * (i+1.0)
                step_node_y = node_from.y + check_step * direction_y * (i+1.0)
                nodes_to_check.append(Node(step_node_x,step_node_y))

        for node in nodes_to_check:
            for obstacle in obstacle_list:
                obs_x, obs_y, r = obstacle
                
                dx = node.x - obs_x
                dy = node.y - obs_y
                dist = np.sqrt(dx*dx+dy*dy)

                if(dist <= r):
                    return True
        return False

        
if __name__ == "__main__":
    # 시작 지점과 목표 지점 설정
    start_point = (0, 0)
    goal_point = (10, 10)

    # 작업 영역 (min_x, max_x, min_y, max_y) 설정
    space = (-20, 20, -20, 20)

    # 장애물 리스트 (각각의 장애물은 (x, y, 반지름) 형태로 설정)
    # 장애물 갯수
    num_obstacles = 50

    # 장애물 리스트 (각각의 장애물은 (x, y, 반지름) 형태로 설정)
    obstacle_list = []

    for _ in range(num_obstacles):
        obs_x = np.random.uniform(space[0], space[1])
        obs_y = np.random.uniform(space[2], space[3])
        obs_radius = np.random.uniform(0.5, 3.0)  # 장애물 크기를 0.5 ~ 3.0 사이의 랜덤 값으로 설정
        obstacle_list.append((obs_x, obs_y, obs_radius))


    # RRT 객체 생성
    rrt_planner = RRT(start_point, goal_point, space, obstacle_list)

    # 경로 계획
    path = rrt_planner.plan()

    if path:
        # 경로 출력
        print("Found path:")
        for node in path:
            print(f"({node.x}, {node.y})")

        # 시각화
        plt.figure(figsize=(8, 8))
        plt.axis([space[0], space[1], space[2], space[3]])
        plt.plot(start_point[0], start_point[1], 'go', markersize=10)
        plt.plot(goal_point[0], goal_point[1], 'ro', markersize=10)
        for obstacle in obstacle_list:
            circle = plt.Circle((obstacle[0], obstacle[1]), obstacle[2], color='gray')
            plt.gca().add_patch(circle)

        # 경로를 점으로 표시
        x_vals = [node.x for node in path]
        y_vals = [node.y for node in path]
        plt.scatter(x_vals, y_vals, c='lightgray', marker='o', s=30, label='Path')
        
        # 경로를 선으로 연결 (선은 투명도를 줌)
        plt.plot(x_vals, y_vals, 'b-', linewidth=2, alpha=0.7, label='Path Line')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("RRT Path Planning with Obstacles")
        plt.grid(True)
        plt.legend()
        plt.show()
    else:
        print("Failed to find a path.")




















































































































































































































































