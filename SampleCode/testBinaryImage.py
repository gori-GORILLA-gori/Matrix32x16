from library.matrix32x16 import Matrix32x16

# LEDマトリクスの初期化
m = Matrix32x16()
# 画面をクリア
m.fill()
# 画像を読み込む
m.binary_image("Image.bin")
# 画面を更新
m.show(1000)