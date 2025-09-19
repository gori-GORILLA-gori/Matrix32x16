from machine import Pin,Timer
import utime



half_chars = set("!\"#$%&'()*+,-./"
                "0123456789"
                ":;<=>?@"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "[\\]^_`"
                "abcdefghijklmnopqrstuvwxyz"
                "{|}~"
                "ｧｱｨｲｩｳｪｴｫｵｶｷｸｹｺｻｼｽｾｿﾀﾁｯﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝﾞﾟ")
class Matrix32x16:
    def __init__(self, sin1=11, sin2=12, sin3=13, clk=14, latch=15):
        self.SIN1 = Pin(sin1, Pin.OUT)
        self.SIN2 = Pin(sin2, Pin.OUT)
        self.SIN3 = Pin(sin3, Pin.OUT)
        self.CLOCK = Pin(clk, Pin.OUT)
        self.LATCH = Pin(latch, Pin.OUT)
        #辞書を統合
        self.font_data = dict()

        # 初期化
        for pin in [self.SIN1, self.SIN2, self.SIN3, self.CLOCK, self.LATCH]:
            pin.value(0)
        
        self.pattern = [
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000
        ]
        self.show_pattern = [
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000,
            0b00000000000000000000000000000000
        ]
            
    def send_bit(self, s1, s2, s3):
        self.SIN1.value(s1)
        self.SIN2.value(s2)
        self.SIN3.value(s3)
        utime.sleep_us(1)
        self.CLOCK.high()
        utime.sleep_us(1)
        self.CLOCK.low()

    def send_data(self, row_data, led1_data, led2_data):
        for i in range(16):
            b1 = (row_data >> (i)) & 1
            b2 = (led1_data >> (i)) & 1
            b3 = (led2_data >> (i)) & 1
            self.send_bit(b1, b2, b3)
        self.LATCH.low()
        utime.sleep_us(1)
        self.LATCH.high()

    def pattern_update(self,list):
        self.pattern = list
    def binary_image(self,path):
        data_list = []
        with open(path, "rb") as f:
            for _ in range(16):
                data = f.read(4)
                if len(data) < 4:
                    break
                value = int.from_bytes(data, "big")  #位置引数にする

                data_list.append(value)
        self.pattern = data_list
    def use_alphabet_font(self):
        from library.fonts.misaki_font import alphabet_font
        self.font_data.update(alphabet_font)
    def use_japanese_font(self):
        from library.fonts.misaki_font import japanese_font
        self.font_data.update(japanese_font)
    def use_symbol_number_font(self):
        from library.fonts.misaki_font import symbol_number_font
        self.font_data.update(symbol_number_font)
    def use_kanji_font(self):
        from library.fonts.misaki_font import kanji_font
        self.font_data.update(kanji_font)
    
    def pixel(self,x,y,c):
        self.pattern[y] = setBit(self.pattern[y],c,31-x)
    
    def line(self, x1, y1, x2, y2, c):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.pixel(x1, y1, c)  # 点を描画

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def fill(self,c = 0):
        if c:
            self.pattern = [
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF
            ]
        else:
            self.pattern = [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]
    def draw_circle(self, cx, cy, r, color):
        x = 0
        y = r
        d = 1 - r

        def plot8(xc, yc, x, y):
            self.pixel(xc + x, yc + y, color)
            self.pixel(xc - x, yc + y, color)
            self.pixel(xc + x, yc - y, color)
            self.pixel(xc - x, yc - y, color)
            self.pixel(xc + y, yc + x, color)
            self.pixel(xc - y, yc + x, color)
            self.pixel(xc + y, yc - x, color)
            self.pixel(xc - y, yc - x, color)

        plot8(cx, cy, x, y)
        while x < y:
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1
            plot8(cx, cy, x, y)
            
    def rect(self,x1,y1,x2,y2,c):
        self.line(x1,y1,x1,y2,c)
        self.line(x2,y1,x2,y2,c)
        self.line(x1,y1,x2,y1,c)
        self.line(x1,y2,x2,y2,c)
    def fill_rect(self, x1, y1, x2, y2, c):
        x3 = min(x1, x2)
        x4 = max(x1, x2)
        y3 = min(y1, y2)
        y4 = max(y1, y2)

        mask = 0
        for x in range(x3, x4 + 1):
            if 0 <= x < 32:
                mask |= (1 << (31 - x))

        for y in range(y3, y4 + 1):
            if 0 <= y < len(self.pattern):
                if c == 1:
                    self.pattern[y] |= mask
                else:
                    self.pattern[y] &= ~mask
    def text(self,text,x,y,c):
        xSet = 0
        for i, char in enumerate(text):
            code = str(ord(char))
            if code not in self.font_data:
                code = str(ord("?"))  # フォントに含まれてない文字

            glyph = self.font_data[code]
            is_half = char in half_chars
            glyph_width = 4 if is_half else 8
            
            for row, bits in enumerate(glyph):
                mask = 0
                for col in range(glyph_width):
                    if (bits >> (7 - col)) & 1:
                        mask |= (1 << (31 - (col + x + xSet)))  # MSB基準（左からx）
                if c:
                    self.pattern[row+y] |= mask
                else:
                    self.pattern[row+y] &= ~mask
            xSet += glyph_width
    def reverse(self):
        for i in range(16):
            self.pattern[i] = ~self.pattern[i]
    def rotate_x(self,rotate,moveDirection):
        if moveDirection:
            for i in range(16):
                self.pattern[i] = rotate_right(self.pattern[i],rotate,32)
        else:
            for i in range(16):
                self.pattern[i] = rotate_left(self.pattern[i],rotate,32)
    def rotate_y(self,rotate,moveDirection):
        if moveDirection:
            self.pattern = rotate_down(self.pattern,rotate)
        else:
            self.pattern = rotate_up(self.pattern,rotate)
    def show(self, runTime=None):
        self.show_pattern = self.pattern

        def timer_callback(timer):
            self.show_data(timer)
            # runTime が数値なら自動停止チェック
            if isinstance(runTime, (int, float)):
                now = utime.ticks_ms()
                if utime.ticks_diff(now, self._show_start) >= runTime * 1000:
                    self.t.deinit()

        # タイマーを作る（既にあれば再利用）
        if not hasattr(self, "t"):
            self.t = Timer()

        if runTime is None:
            # 更新だけ
            return
        elif runTime == "start":
            self._show_start = utime.ticks_ms()
            self.t.init(freq=50, mode=Timer.PERIODIC, callback=timer_callback)
        elif runTime == "end":
            self.t.deinit()
        else:  # 数値
            self._show_start = utime.ticks_ms()
            self.t.init(freq=50, mode=Timer.PERIODIC, callback=timer_callback)


    def show_data(self, timer):
        for row in range(16):
            row_mask = 1 << row
            self.send_data(
                row_mask,
                upper_mask(self.show_pattern[row]),
                lower_mask(self.show_pattern[row])
            )
            utime.sleep_us(50)

def upper_mask(x):
    # 上位16ビットを取り出す
    return (x >> 16) & 0xFFFF

def lower_mask(x):
    # 下位16ビットを取り出す
    return x & 0xFFFF
def setBit(value,bit,pos):
    if bit:
        return value | (1 << pos)
    else:
        return value & ~(1 << pos)
def rotate_right(value, shift_bits, bit_length):
    # 左にシフトして飛び出したビットを保存
    shifted_out = (value & ((1 << shift_bits) - 1))  # 右シフトして飛び出したビットを取り出す
    # 右シフト
    value = (value >> shift_bits)  # 左にシフト
    # シフトアウトしたビットを元の位置に戻す
    value = value | (shifted_out << (bit_length - shift_bits))  # シフトしたビットを最上位に戻す
    return value

def rotate_left(value, shift_bits, bit_length):
    # 右にシフトして飛び出したビットを保存
    shifted_out = (value >> (bit_length - shift_bits)) & ((1 << shift_bits) - 1)
    # 左シフト
    value = (value << shift_bits) & ((1 << bit_length) - 1)  # ビット長を超えないようにする
    # シフトアウトしたビットを元の位置に戻す
    value = value | shifted_out
    return value
def rotate_up(value, shift):
    newValue = value[shift:] + value[:shift]
    return newValue
def rotate_down(value, shift):
    newValue = value[-shift:] + value[:-shift]
    return newValue



