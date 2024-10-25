from flask import Flask
from flask_migrate import Migrate
import config
from exts import *
# from exts import cache
from blueprints.views import bp
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)
cache.init_app(app)
# 解决跨域请求
CORS(app, supports_credentials=True)
# 挂载
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
