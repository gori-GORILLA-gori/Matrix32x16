<img width="2048" height="1024" alt="image" src="https://github.com/user-attachments/assets/7639870e-2862-4712-b8db-6f124d94cfe7" /># Matrix32x16

秋月電子で販売していた32x16ドットマトリクスLEDのRaspberry Pi Pico用ライブラリです。

## ⚠️ 注意点
- 使用するドットマトリクスLEDは横に接続可能ですが、**このライブラリでは単体での使用のみを想定しています**。

---
## 動作環境
- Raspberry PI Picoシリーズ
## 🔧 使用方法

### 1. ライブラリをRaspberry Pi Picoにアップロードする

1. GitHubの[Code] → [Download ZIP]からZIPをダウンロード
2. ダウンロード後、ZIPを解凍
3. Thonnyで解凍したフォルダに移動し、その中の `library`フォルダを右クリック → `/`にアップロード

### 2. 配線
LEDマトリクス側のピン配列は以下の通りです。  
<img src="https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/MatrixPin.png" width="600">  

### 3. Pythonコードに記述

```python
from library.matrix32x16 import Matrix32x16

# ピン指定を省略した場合はデフォルトのピンが使われます:
# sin1=11, sin2=12, sin3=13, clk=14, latch=15

m = Matrix32x16(sin1=任意のピン, sin2=任意のピン, sin3=任意のピン, clk=任意のピン, latch=任意のピン)
```
## 仕様
- 座標は左上から右下にかけて増えていきます
<img src="https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/matrixVector2.png" width="600">

- すべて`pattern`変数に描画内容を設定し、最後に`show()`で表示します

```Python

use_alphabet_font()
# アルファベットフォントを読み込みます
use_japanese_font()
# 日本語フォントを読み込みます
use_symbol_number_font()
# 記号フォントを読み込みます
use_kanji_font()
# 漢字フォントを読み込みます

pattern_update(List)
# Listに32桁の2進数を16個入れると、その形でパターンを描画します。

binary_image(path)
# バイナリ画像(後述フォーマット)を読み込み、その内容を表示します。

pixel(x, y, c)
# 指定座標(x, y)にc(0: 消灯 / 1: 点灯)を設定します。

line(x1, y1, x2, y2, c)
# (x1, y1)から(x2, y2) に直線を描きます。

fill(c)
# 全画面をc(0または1)で塗りつぶします。
# 0か1か指定しない場合はデフォルトの0になります

draw_circle(cx, cy, r, c)
# 中心(cx, cy)、半径rの円をcで描きます。

rect(x1, y1, x2, y2, c)
# 四角形の枠線を描きます。

fill_rect(x1, y1, x2, y2, c)
# 塗りつぶした四角形を描きます。

text(text, x, y, c)
# 座標(x, y)からテキストを描きます。  
# 通常は8x8フォントですが、一部の記号やアルファベットは4x8になります。

reverse()
# 現在のパターンの 0 と 1 を反転します。

rotate_x(rotate, moveDirection)
# 横方向に rotate 分だけ移動します。
# moveDirection: 0 → 左へ / 1 → 右へ(ループあり)

rotate_y(rotate, moveDirection)
# 縦方向に rotate 分だけ移動します。
# moveDirection: 0 → 上へ / 1 → 下へ(ループあり)

show(runTime)
# 画面表示を開始し、runTime秒後に自動で終了します。

show("start")
# 画面表示を開始します

show("end")
# 開始した画面表示を停止します

show()
# 引数に何も指定しないと画面の状態を更新します

```
## binary_imageについて
binary_image関数を使用する際のバイナリ画像は**32x16の白黒PNG画像**を白を0、黒を1にしてバイナリファイルとして保存した独自の形式を使用します。
この形式の画像を出力するには`Matrix32x16/SampleCode/BinaryImage/`にある`32x16pngToHex.exe`を使用します。
### `32x16pngToHex.exe`の動作環境
- Windows10  
- Windows11
exeファイルですのでMacやLinuxでの動作は想定していません  

### `32x16pngToHex.exe`使用方法  

- 初回起動時は**WindowsによってPCが保護されました**などと出る可能性があります。  
  <img src="https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/Difender.png" width="300">    
  その場合は<ins>`詳細情報`</ins>をクリックして`実行`をクリックすると起動できます。
  
1. 画像ファイルの指定  
   画像ファイルのパスを打ち込むか`参照...`ボタンを押して変換したい画像を選択してください  
   ![アプリ画面](https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/32x16pngToHex_Main.png)

2. 保存先の指定
   開いたウィンドウで保存先を指定してください
   ![save](https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/Save.png)
   
4. 成功というウィンドウが出たら保存完了  
   ![success](https://raw.githubusercontent.com/gori-GORILLA-gori/Matrix32x16/refs/heads/main/Image/success.png)
### `32x16pngToHex.py`について  
`32x16pngToHex.py`は`32x16pngToHex.exe`の元となっているPythonコードです。  
現在は主にWindows上での動作を想定していますが、MacやLinuxの環境でも使用できるように修正することで動作する可能性があります。  

## サンプルコードの使い方
``SampleCode/``フォルダ内には、ライブラリの使い方を理解するためのサンプルがいくつか入っています。  

- ``rotateSquare.py``  
  三角関数を使用して回転する正方形を表示するデモです。図形描画と回転の応用がわかります。
  
- ``testBinaryImage.py``  
  PNG画像を変換して表示するサンプルです。``BinaryImage/test.bin``を読み込み表示します。  
  このサンプルコードを使用するには``BinaryImage/test.bin``をPicoにアップロードしてください。 
  
- ``textTest.py``
  テキスト表示のサンプルです。任意の文字列をLEDに表示する方法を確認できます。
  
### 使い方:
1. ``library``フォルダを``/``にアップロード済みであることを確認します
2. 任意のサンプルコードをThonnyで開き、``F5``キー、もしくは画面右上の実行ボタンで実行
## ファイル構成
```
Matrix32x16/
├── library/
│   ├── matrix32x16.py
│   └── fonts/
│       └── misaki_font.py
├── SampleCode/
│   ├── rotateSquare.py
│   ├── testBinaryImage.py
│   ├── textTest.py
│   └── BinaryImage/
│       ├── 32x16pngToHex.py
│       ├── 32x16pngToHex.exe
│       └── Image.bin
└── README.md
```
## 使用フォント

このプロジェクトでは「美咲フォント(Misaki Font)」を使用しています。  
美咲フォントの著作権は「門真 なむ」様に帰属します。

- フォント名: 美咲フォント
- 著作権者: 門真 なむ
- 配布元: https://littlelimit.net/misaki.htm
- ライセンス: 美咲フォント使用条件に準拠(https://littlelimit.net/font.htm#license)

本フォントは自由に利用・改変・再配布可能ですが、著作権表示およびライセンス条件を保持する必要があります。
### 改変フォントについて
本プロジェクトでは、オリジナルの美咲フォントを以下のように改変しています：

- 一部文字のデータの消去
- フォーマットを変更（Python辞書形式に変換）

改変後も美咲フォントのライセンスに準拠し、著作権表示を保持しています。

- 原著作権者: 門真 なむ
- 改変者: gori-GORILLA-gori

## 製作者コメント
そもそもこのライブラリで使用するドットマトリクスLEDはすでに販売終了しているものです。  
ですが秋月電子の実店舗でたまにアウトレット品として販売されています。見る頻度は結構多いので在庫がけっこうあるのかも。  
実はニコニコ動画で有名な「全力でスイッチをONするとOFFするロボットと戦ってみた」という動画に登場するロボの顔の表示にも使われていたりします。  
販売していたのは2004年ごろらしいです。そういうこともあってかライブラリなどは一切ありませんでした。  
そこで狭いニーズではありますがライブラリを作って開発を楽にしようと考えこのライブラリを制作しました。  
このライブラリを作ってからこのLEDマトリクスを使用しての開発がだいぶ楽になりました。  
ではみなさん、良い電子工作ライフをお送りください。

## License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/mit-license.php) for details.
