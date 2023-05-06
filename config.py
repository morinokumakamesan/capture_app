from dotenv import load_dotenv
import os

load_dotenv()

# 環境変数を参照
LINE_CHANNEL_ACCESS_TOKEN_1 = os.getenv('LINE_CHANNEL_ACCESS_TOKEN_1')
LINE_CHANNEL_SECRET_1 = os.getenv('LINE_CHANNEL_SECRET_1')