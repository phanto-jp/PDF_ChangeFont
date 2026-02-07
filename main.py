import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import statistics
import sys
import os

#----------------------------------------------------------------------------------------
# 各種設定
#----------------------------------------------------------------------------------------

INPUT_PDF = "sample.pdf"
FONT_PATH = "yumindb"
FONT_NAME = 'ReplaceFontName'

# 記号ごとの補正量（offset_x, offset_y, angle, mirror）
ROTATE_OFFSET = {
    "〝": (0.00,  0.20, -55, False), # 開き
    "〟": (0.30,  0.60,   0, True ), # 閉じ
    "ー": (0.86,  0.86,  93, True ),
    "…": (0.86, -0.15,  90, False),
}

SMALL_CHARS = {
    "っ", "ゃ", "ゅ", "ょ", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ",
    "ッ", "ャ", "ュ", "ョ", "ァ", "ィ", "ゥ", "ェ", "ォ",
}
SMALL_OFFSET_X = 0.1   # フォントサイズに対する倍率
SMALL_OFFSET_Y = 0.1

ELLIPSIS_VARIANTS = {
    "\uFE19",  # ︙
    "\u205D",  # ⁝
    "\u22EE",  # ⋮
    "\u22EF",  # ⋯
}

DASH_START = False

#----------------------------------------------------------------------------------------
# 補助関数
#----------------------------------------------------------------------------------------

def get_font_name() :
    return sys.argv[1] if len(sys.argv) >= 2 else FONT_PATH

def get_font_path( name ) :

    # フォント名
    print( 'Font:', name )
    ext = 'ttf'

    # このフォルダ
    filename = '%s.%s' % (name, ext)
    if os.path.exists( filename ) :
        return filename
    
    # システムフォルダ
    path = os.path.join( os.environ['WINDIR'], 'Fonts', filename )
    if os.path.exists( path ) :
        return path

    # ユーザごとのフォルダ    
    path = os.path.join( os.environ["LOCALAPPDATA"], 'Microsoft', 'Windows', 'Fonts', filename)
    if os.path.exists( path ) :
        return path

    # 見つからず
    return None

def set_font_property( name ) :
    global ROTATE_OFFSET
    if 'YonagaOldMincho' in name :
        ROTATE_OFFSET['〝'] = (0.25,  0.95, -90, False)
        ROTATE_OFFSET['〟'] = (0.00,  0.85, -90, False)
    elif 'ShipporiMincho' in name :
        ROTATE_OFFSET['〝'] = (0.00,  0.60, -70, False)
        ROTATE_OFFSET['〟'] = (0.00,  0.80, -70, False)
    elif 'ZenOldMincho' in name :
        ROTATE_OFFSET['〝'] = (0.50,  0.85, -90, False)
        ROTATE_OFFSET['〟'] = (0.00,  0.80, -90, False)
        ROTATE_OFFSET['…'] = (0.55, -0.00,  90, False)

def register_font() :
    name = get_font_name()
    font_path = get_font_path( name )
    if font_path != None :
        print( 'Path:', font_path )
        try :
            pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
            set_font_property( name )
            return True
        except :
            pass
    return False

def normalize_text(text):
    if text in ELLIPSIS_VARIANTS:
        return "…"
    if text == '〞':
        return "〟"
    return text

def draw_text(c, x, y, text, size):

    global DASH_START

    # 出ない文字対策
    text = normalize_text(text)

    # 小字の補正
    if text in SMALL_CHARS:
        x += size * SMALL_OFFSET_X
        y += size * SMALL_OFFSET_Y

    # 縦棒のスキマ補正 ( ホントはフォントによって変えるとよい )
    # ※ ２つセットじゃないとバグる
    DASH_OFFSET = 0.01
    if text == '︱' :
        if DASH_START :
            y -= size * DASH_OFFSET
            DASH_START = False
        else :
            y += size * DASH_OFFSET
            DASH_START = True

    # 回転が必要な記号
    if text in ROTATE_OFFSET :
        offset_x, offset_y, angle, mirror = ROTATE_OFFSET[text]
        offset_x *= size
        offset_y *= size
        c.saveState()
        c.translate(x + offset_x, y + offset_y)
        if angle != 0.0 :
            c.rotate(angle)
        if mirror :
            c.scale(-1, 1)
        c.setFont(FONT_NAME, size)
        c.drawString(0, 0, text)
        c.restoreState()
    else:
        c.setFont(FONT_NAME, size)
        c.drawString(x, y, text)

def get_inputpath() :
    ret = INPUT_PDF
    if len( sys.argv ) >= 3 and os.path.exists( sys.argv[2] ) :
        ret = sys.argv[2]
    print( 'Input:', ret )
    if os.path.exists( ret ) :
        return ret
    return None

def get_outputpath( input ) :
    input_name = input.split('.')[0]
    return '%s_%s.pdf' % (input_name, get_font_name())

#----------------------------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------------------------

def main() :

    # データチェック
    input_pdf = get_inputpath()
    if input_pdf == None :
        print( ' -> Not found.')
        return False
    print( ' -> OK.' )
    if register_font() == False :
        print( ' -> Not found.')
        return False
    print( ' -> OK.' )

    # PDF 作成
    ret = False
    with pdfplumber.open(input_pdf) as pdf:
        first_page = pdf.pages[0]
        width = first_page.width
        height = first_page.height

        output_pdf = get_outputpath(input_pdf)
        c = canvas.Canvas(output_pdf, pagesize=(width, height))

        print('-'*16)
        for i, page in enumerate(pdf.pages):
            print('Page %3d / %d ...' % (i+1, len(pdf.pages)))
            chars = page.chars

            xs = [ch["x0"] for ch in chars]
            spread = max(xs) - min(xs)

            # ★ 2段判定
            is_two_column = spread > 80

            if is_two_column:
                mid = statistics.median(xs)

                right_col = [ch for ch in chars if ch["x0"] > mid]
                left_col  = [ch for ch in chars if ch["x0"] <= mid]

                # ★ y0 昇順（上→下）
                right_sorted = sorted(right_col, key=lambda ch: ch["y0"])
                left_sorted  = sorted(left_col,  key=lambda ch: ch["y0"])

                for ch in right_sorted:
                    draw_text(c, ch["x0"], ch["y0"], ch["text"], ch["size"])

                for ch in left_sorted:
                    draw_text(c, ch["x0"], ch["y0"], ch["text"], ch["size"])

            else:
                # 1段ページ
                one_sorted = sorted(chars, key=lambda ch: ch["y0"])
                for ch in one_sorted:
                    draw_text(c, ch["x0"], ch["y0"], ch["text"], ch["size"])

            c.showPage()

        # セーブ
        print( '-' * 16, '\nSave to:', output_pdf )
        try :
            c.save()
            print( ' -> OK.' )
            ret = True
        except :
            print( ' -> Error, Access denied.')

    # 結果を返す
    return ret

#----------------------------------------------------------------------------------------

# 実行
result = 'OK.' if main() else 'Failed.'
print( '-' * 16, '\nConvert', result )

# end of file.
