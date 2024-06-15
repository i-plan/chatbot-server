"""
 优先从instance目录读取配置文件，如果没有再从内存读取
"""
import os


class ProductionConfig:
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    JSONIFY_MIMETYPE = 'application/json'
    # TEMPLATES_AUTO_RELOAD = None
    # MAX_COOKIE_SIZE = 10485760
    # MAX_CONTENT_LENGTH=None
    DB_SERVER = '192.168.19.32'
    MONGO_URI = "mongodb://mongo:p5b67avO9383spNYAXYt@containers-us-west-32.railway.app:5746"

    @property
    def DATABASE_URI(self):  # Note: all caps
        return 'mysql://user@{}/foo'.format(self.DB_SERVER)

    SECRET_KEY = os.environ.get('B_SECRET', 'secret-key')
    WTF_CSRF_ENABLED = False
    AVATAR_PATH = '/avatar/'
    COOKIE_ENABLE = False
