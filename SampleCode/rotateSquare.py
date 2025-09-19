from library.matrix32x16 import Matrix32x16
import math
import utime

# LEDマトリクスの初期化
m = Matrix32x16()
m.show("start")
while True:
    # 二度ずつ回転するため180回繰り返す
    for i in range(180):
        # 画面をクリア
        m.fill(0)
        # 角度iをラジアンに変換
        R = math.radians(i*2)
        # 半径を7に設定
        r = 7
        # 四角形の4つの頂点の座標を計算
        x1 = round(math.cos(R)*r)+16
        y1 = round(math.sin(R)*r)+8
        x2 = round(math.cos(R+math.pi*1/2)*r)+16
        y2 = round(math.sin(R+math.pi*1/2)*r)+8
        x3 = round(math.cos(R+math.pi)*r)+16
        y3 = round(math.sin(R+math.pi)*r)+8
        x4 = round(math.cos(R+math.pi*3/2)*r)+16
        y4 = round(math.sin(R+math.pi*3/2)*r)+8
        # 4つの頂点を結ぶ線を描画
        m.line(x1,y1,x2,y2,1)
        m.line(x2,y2,x3,y3,1)
        m.line(x3,y3,x4,y4,1)
        m.line(x4,y4,x1,y1,1)
        # 画面を更新
        m.show()
        utime.sleep(0.001)

