#藍圖：當在藍圖裡定義時，處於休眠狀態。直到藍圖被app註冊時，才成為app的一部分。
from flask import Blueprint

#實例化Blueprint類別。
#此類別的建構式必須接收兩個引數：藍圖名稱與藍圖所在的模組或套件。
main = Blueprint('main', __name__)

#匯入app套件的模組，以建立與藍圖的關係 (包含app路由&錯誤頁面處理函式)
# . 代表目前的套件； .. 代表目前套件的父代
from . import views, errors   #相對匯入
