import numpy as np
import math
import matplotlib.pyplot as plt
import random
import time


class Camera:
    def __init__(self, landmarks, max_range, sense_noise):
        self.landmarks = landmarks  # ランドマークの位置
        self.max_range = max_range  # 観測可能な最大距離
        self.sense_noise = sense_noise  # 観測ノイズ

    def sense(self, x):
        """ランドマークとの距離を観測（ノイズを追加）"""
        z = []
        for landmark in self.landmarks:
            distance = abs(x - landmark[0])  # 距離
            if distance <= self.max_range:  # 観測可能な範囲
                noisy_distance = distance + random.gauss(0.0, self.sense_noise)
                z.append((noisy_distance, landmark))  # (観測距離, ランドマーク位置)
        return z


class RobotSim:
    def __init__(self, landmarks, world_size, max_range, sense_noise):
        self.landmarks = landmarks  # ランドマークの位置 [(x1, y1), (x2, y2), ...]
        self.world_size = world_size  # 世界の大きさ
        self.camera = Camera(landmarks, max_range, sense_noise)  # カメラ機能を統合

        # ロボットの初期位置
        self.x = 0.0  
        self.y = 0.0  

        # 動作ノイズ
        self.forward_noise = 0.0

    def set_noise(self, forward_noise):
        """動作ノイズを設定"""
        self.forward_noise = forward_noise

    def move(self, forward):
        """ロボットを移動"""
        self.x += forward + random.gauss(0.0, self.forward_noise)
        self.x %= self.world_size  # 世界の端でループ
        return self.x

    def sense(self):
        """カメラを使用してランドマークを観測"""
        return self.camera.sense(self.x)


class ParticleFilter:
    def __init__(self, num_particles, world_size, landmarks):
        self.num_particles = num_particles
        self.world_size = world_size
        self.landmarks = landmarks

        # パーティクルの初期化
        self.particles = [self.create_random_particle() for _ in range(num_particles)]

    def create_random_particle(self):
        """ランダムなパーティクルを生成"""
        x = random.uniform(0, 0)
        return {'x': x, 'orientation': 1.0, 'weight': 1.0}

    def motion_update(self, forward, motion_noise):
        """パーティクルを移動"""
        for particle in self.particles:
            dist = forward + random.gauss(0.0, motion_noise)
            particle['x'] += dist
            particle['x'] %= self.world_size
            particle['orientation'] = forward  # 矢印の方向を進行方向に設定

    def observation_update(self, measurements, sense_noise):
        """観測に基づいてパーティクルの重みを更新"""
        for particle in self.particles:
            particle['weight'] = 1.0
            for dist, landmark in measurements:  # タプル (距離, ランドマーク)
                particle_dist = abs(particle['x'] - landmark[0])  # ランドマークのx座標
                particle['weight'] *= self.gaussian(particle_dist, sense_noise, dist)

    def resample_particles(self):
        """重みに基づいてパーティクルをリサンプリング"""
        weights = [particle['weight'] for particle in self.particles]
        new_particles = random.choices(self.particles, weights=weights, k=self.num_particles)
        self.particles = [{'x': p['x'], 'orientation': p['orientation'], 'weight': 1.0} for p in new_particles]

    @staticmethod
    def gaussian(mu, sigma, x):
        """ガウス分布"""
        return math.exp(-((mu - x) ** 2) / (2 * sigma ** 2)) / math.sqrt(2 * math.pi * sigma ** 2)

    def get_particle_positions(self):
        """パーティクルの位置と方向を取得"""
        return [{'x': p['x'], 'orientation': p['orientation']} for p in self.particles]


def main():
    # 世界の設定
    world_size = 100.0
    landmarks = [(80.0, 0.0)]  # ランドマークを複数配置
    num_particles = 100
    robot_speed = 1.0  # ロボットの速度を1に固定
    max_range = 20.0  # 観測可能な最大距離
    sense_noise = 2.0  # 観測ノイズ

    # ロボットの初期化
    robot = RobotSim(landmarks, world_size, max_range, sense_noise)
    robot.set_noise(forward_noise=0.5)  # 動作ノイズを調整

    # パーティクルフィルタの初期化
    pf = ParticleFilter(num_particles, world_size, landmarks)

    # シミュレーション
    plt.ion()
    start_time = time.time()  # シミュレーション開始時間

    while robot.x < world_size - robot_speed:
        plt.clf()

        # 経過時間を計算
        elapsed_time = time.time() - start_time

        # ロボットの移動と観測
        robot_position = robot.move(robot_speed)  # 右方向に移動
        measurements = robot.sense()

        # パーティクルフィルタの更新
        pf.motion_update(robot_speed, motion_noise=0.5)  # 動作ノイズを調整
        pf.observation_update(measurements, sense_noise=sense_noise)
        pf.resample_particles()

        # 描画
        particles = pf.get_particle_positions()
        particle_x = [p['x'] for p in particles]
        particle_dx = [p['orientation'] for p in particles]  # 矢印の長さ（方向）
        plt.quiver(particle_x, [0] * len(particles), particle_dx, [0] * len(particles),
                   angles='xy', scale_units='xy', scale=1, color="blue", label='Particles')

        # ロボットとランドマークを描画
        plt.scatter(robot_position, 0, s=100, c='red', label='Robot')
        for lm in landmarks:
            color = 'blue' if lm in [landmark for _, landmark in measurements] else 'yellow'
            plt.scatter(lm[0], lm[1], s=200, c=color, marker='*', label='Landmark')

        plt.title(f"Time Elapsed: {elapsed_time:.1f} seconds")
        plt.xlim(0, world_size)
        plt.ylim(-1, 1)  # より狭い範囲で表示
        plt.legend(loc='upper right')
        plt.pause(0.1)  # 0.1秒ごとに更新

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()

