import glob
import os
import PyPDF2
import re
import string
import random
import sys

INPUT_PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'input_pdf')
OUTPUT_PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'output_pdf')
OUTPUT_PASS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'output_pass')

def createPasswd(size=12,isStrongPolicy=True):
  """
  パスワード作成
  """
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  passwd = ''
  if isStrongPolicy:
    isVaildPass = False
    while(not isVaildPass):
      passwd = ''.join(random.choice(chars) for x in range(size))
      if checkPolicy(passwd):
        isVaildPass = True
  else:
    passwd = ''.join(random.choice(chars) for x in range(size))
  return passwd

def checkPolicy(passwd):
  """
  パスワードポリシーチェック
  アルファベット大文字小文字数字が全部含まれているか
  """
  hasUpper = False
  hasLower = False
  hasDigits = False
  for c in passwd:
    if re.match(r'[A-Z]',c):
      hasUpper = True
    elif re.match(r'[a-z]',c):
      hasLower = True
    elif re.match(r'[0-9]',c):
      hasDigits = True
  if hasUpper and hasLower and hasDigits:
    return True
  else:
    return False

def main():
  print('====start process====')
  inputPdfFilePaths = glob.glob(INPUT_PDF_DIR + '/*.pdf')
  print('input file count:' + str(len(inputPdfFilePaths)))

  if len(inputPdfFilePaths) == 0:
    print('input pdf is none.')
    print('please press enter key.')
    input()
    print('bye')
    sys.exit(1)
  
  print('====start passset====')
  for path in inputPdfFilePaths:
    fileName = os.path.basename(path)
    try:
      # pdf読み込み
      srcPdf = PyPDF2.PdfFileReader(path,strict=False)

      # パスワード付与用PDF作成、データコピー
      distPdf = PyPDF2.PdfFileWriter()
      distPdf.cloneReaderDocumentRoot(srcPdf)
      d = {key: srcPdf.documentInfo[key] for key in srcPdf.documentInfo.keys()}
      distPdf.addMetadata(d)

      # パスワード付与
      passwd = createPasswd()
      distPdf.encrypt(passwd)

      # パス付きPDF出力
      with open(OUTPUT_PDF_DIR + '/' + fileName,'wb') as f:
        distPdf.write(f)
      
      # パスワードファイル出力
      with open(OUTPUT_PASS_DIR + '/' + fileName.replace('.pdf','') + '.txt','w',encoding='utf-8') as f:
        f.write(passwd)

      print('Success passset,' + fileName)
    except Exception as e:
      tb = sys.exc_info()[2]
      print("Error passset," + fileName + "," +str(e.with_traceback(tb)))
    
    print('=====end passset=====')
    print('=====end process=====')
    print('please press enter key.')
    input()
    print('bye')
    sys.exit(0)

if __name__ == '__main__':
  main()
