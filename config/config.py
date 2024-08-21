import os
from dotenv import load_dotenv
import sys

class BotConfig:
    def __init__(self, envpath) -> None:
        self.envpath = envpath
        self.SetDotEnv()
        self.GetBotEnv()
        self.GetDatabaseEnv()
        self.PaymentConf()
        self.ChannelConf()

    def SetDotEnv(self):
        try:
            load_dotenv(dotenv_path=self.envpath)
        except Exception as ex:
            print(".env not found.")

    def GetBotEnv(self):
        self.token = os.getenv("BOT_TOKEN", "defaultbottoken")
        self.admin_tg_id = os.getenv("ADMIN_TG_ID", "").split(",")
        self.default_photo=os.getenv("DEFAULT_PHOTO", "https://minio.itechacademy.uz/product/no%20photo.png")
        self.default_video=os.getenv("DEFAULT_VIDEO", "Dilkash-start_compressed.mp4")
    
    def GetDatabaseEnv(self):
        self.db_user= os.getenv("DB_USER", "default_user")
        self.db_password = os.getenv("DB_PASSWORD", "default_password")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "dilkash_bot")

    def PaymentConf(self):
        self.payme_token = os.getenv("PAYME_TOKEN", "")
        self.click_token = os.getenv("CLICK_TOKEN", "")

    def ChannelConf(self):
        self.idea_canal_id = os.getenv("IDEA_CANAL_ID", "")
        self.bron_canal_id = os.getenv("BRON_CANAL_ID", "")
        self.order_canal_id = os.getenv("ORDER_CANAL_ID", "")

