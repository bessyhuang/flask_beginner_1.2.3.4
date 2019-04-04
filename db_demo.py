### mariadb 連接 db_demo.py 與 webform.html ###
# 主腳本 #
import os

from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate #用Flask-Migrate進行資料庫遷移

#建立一個App，從環境變數或預設來取得組態設置。
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

##初始化Flask-Migrate
migrate = Migrate(app, db) #用Flask-Migrate進行資料庫遷移

##Python殼層的自訂context
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

### test "單元測試"啟動命令 ###
@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')  # tests 資料夾
    unittest.TextTestRunner(verbosity=2).run(tests)
