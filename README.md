# pdfPassSetter
複数のPDFにランダムパスワードを付けたい時に使えるツール  
パスワードポリシーは現状アルファベット大文字小文字数字12文字  

## 使い方(利用者向け)
1. exec内のdistディレクトリを丸ごとダウンロードしてください
1. パスワードを付けたいpdfをinput_pdfに配備してください
1. passSetter.exeを実行してください
1. output_pdfにパス付きPDFが、ouput_passに各PDFのパスワードが記載されたファイルが作成されます
1. エンターキーを押して終了してください

## 使い方(開発者向け)
1. このリポジトリをcloneしてください
1. pipで以下のモジュールをインストールしてください
   - PyPDF2
   - PyInstaller
1. pipでインストールしたPyPDF2の以下のファイルを修正します(インストールしたままだと出力時に失敗します)  
   - PyPDF2のインストール先ディレクトリを確認
     ```
     pip show PyPDF2
     ```
   - pdf.pyの1631~1632行目をコメントアウト※ログいらないなと思ったので
     ```
     #warnings.warn("Object %d %d not defined."%(indirectReference.idnum,
     #            indirectReference.generation), utils.PdfReadWarning)
     ```
   - 1633行目のコメントアウトを削除し、ifを有効にする
     ```
     if self.strict:
        raise utils.PdfReadError("Could not find object.")
     ```
   - 501行目辺りにtry-exceptを追加する
     ```
     try:
        obj.writeToStream(stream, key)
        stream.write(b_("\nendobj\n"))
     except:
        pass
     ```
1. 以上でpassSetter.pyが実行できる状態になります
1. 実行ファイル化する際は、execディレクトリにて以下のコマンドを実行してください
```
pyinstaller ../passSetter.py --onefile
```
