# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image
from resizeimage import resizeimage
im = Image.open( "/home/grendy/Downloads/Telegram Desktop/Crawling/tokped611673.png" )
imB = im.resize((200,22))
imB.save('/home/grendy/Downloads/Telegram Desktop/Crawling/coy.png')
varnum= pytesseract.image_to_string(Image.open('/home/grendy/Downloads/Telegram Desktop/Crawling/coy.png'))
varnum = str(varnum)
nomor = varnum.replace('«FE-2','0')
print nomor

#buat picture = 320,69 == buat email
#buat picture = 200,22 == buat phone