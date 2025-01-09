import numpy as np
import math
import matplotlib.pyplot as plt
import random
import time
import cv2  # OpenCVをインポート

class Camera:
    # Camera class remains unchanged...
    # ...

class RobotSim:
    # RobotSim class remains unchanged...
    # ...

class ParticleFilter:
    # ParticleFilter class remains unchanged...
    # ...

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

    # 動画作成の設定
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # コーデック設定
    out = cv2.VideoWriter('simulation_video.avi', fourcc, 20.0, (640, 480))  # 動画ファイルの設定

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

        # 描画を画像として保存し、動画に追加
        plt.draw()
        img = np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        out.write(img)

    plt.ioff()
    plt.show()

    # 動画ファイルの保存を終了
    out.release()

if __name__ == "__main__":
    main()

