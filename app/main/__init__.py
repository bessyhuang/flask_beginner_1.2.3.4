#藍圖：當在藍圖裡定義時，處於休眠狀態。直到藍圖被app註冊時，才成為app的一部分。
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors