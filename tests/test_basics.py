import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    #在每次測試之前執行，幫測試程式建立一個類似運行中App的環境
    def setUp(self):
        #建立一個testing組態的App，並啟動context
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  #為測試程式建立全新的資料庫
        
    #在每次測試之後執行
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 開頭為"test_"的方法，是我們要執行的測試 #
    
    #確認App實例的存在
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    #確認App在測試組態下運行
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
