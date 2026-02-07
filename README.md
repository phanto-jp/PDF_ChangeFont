# PDF_ChangeFont
- [動作環境](#-動作環境)
- [ダウンロード](#-ダウンロード)
- [セットアップ](#-セットアップ)
- [使い方](#-使い方)
- [免責事項](#-免責事項)

小説PDFメーカー ( https://shimeken.com/tex ) で作成したPDFのフォントを差し替えます。  
以下のフォントに対応しています。

* **ZENオールド明朝(太字)**
* **しっぽり明朝(太字)**
* **源暎アンチック**
* **夜永オールド明朝(太字)**

## ■ 動作環境

* Windows11
* Python ( 3.10, 3.12 で動作確認 )

## ■ ダウンロード
* **[Ver.1.00](https://github.com/phanto-jp/PDF_ChangeFont/releases/tag/v1.0.0)**  
リンク先の **PDF_ChangeFont_v1.0.0.zip** をダウンロード。

## ■ セットアップ

### Python のインストール
Python が入っていない場合はインストールが必要です。  
動作確認バージョン ( 3.12.10 ) のインストーラはこちら。  
https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe  

インストーラを起動したら **「Add python.exe to PATH」** をチェックして実行します。  
既に Python を入れていて PATH が通っていない方は手動で追加して下さい。

### ライブラリの追加
ダウンロード・解凍したパッケージの setup.bat を実行。  
動作に必要なライブラリが自動的にインストールされます。

### フォントの追加
差し替えたいフォントをインストール。

* **ZENオールド明朝**  
https://fonts.google.com/specimen/Zen+Old+Mincho  
→ ZenOldMincho-Bold.ttf (太字)
* **しっぽり明朝**  
https://fonts.google.com/specimen/Shippori+Mincho  
→ ShipporiMincho-Bold.ttf (太字)
* **源暎アンチック**  
https://okoneya.jp/font/genei-antique.html  
→ GenEiAntiqueNv6-M.ttf
* **夜永オールド明朝**  
https://booth.pm/ja/items/3489185  
→ YonagaOldMincho-Bold.ttf (太字)

## ■ 使い方
バッチファイルに PDF を D&D して実行。  
PDF と同じフォルダに **元の名前_フォント名.pdf** が生成されます。

* **ZENオールド明朝(太字).bat**
* **しっぽり明朝(太字).bat**
* **源暎アンチック.bat**
* **夜永オールド明朝(太字).bat**

テスト用に sample.pdf を同梱しています。  
バッチファイルをダブルクリックするとこのファイルを対象にして実行します。

## ■ 免責事項

本ソフトウェアは無保証で提供されます。  
作者は、本ソフトウェアの使用または使用不能から生じるいかなる損害についても、  
直接的・間接的を問わず、一切の責任を負いません。

本ソフトウェアの使用は、利用者自身の責任において行ってください。  
本ソフトウェアを使用したことにより発生した問題や損害について、  
作者はその責任を負わないものとします。

本ソフトウェアは自由に利用・改変・再配布できますが、  
その結果生じたいかなる問題についても作者は責任を負いません。
