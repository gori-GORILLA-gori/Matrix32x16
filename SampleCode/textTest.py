from library.matrix32x16 import Matrix32x16

# LEDマトリクスの初期化
m = Matrix32x16()
# 画面をクリア
m.fill()
# テキストを表示
m.text("TEST",8,4,1)
# 画面を更新
m.show(1000)
