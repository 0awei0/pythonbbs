import config
import commands
import hooks

from flask import Flask
from exts import db, mail, cache
from blueprints import user_bp, cms_bp, front_bp, media_bp
from flask_migrate import Migrate
from celery_demo import make_celery
from exts import csrf
from models import user, post
from exts import avatars
import filters

app = Flask(__name__)

# 注册头像插件
avatars.init_app(app)
# 添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)
# 添加钩子函数
app.before_request(hooks.bbs_before_request)
# 加载配置文件
app.config.from_object(config.DevelopmentConfig)
# 保护APP
csrf.init_app(app)
# 绑定celery
celery = make_celery(app)
# 将数据库绑定
db.init_app(app)
# 绑定邮箱
mail.init_app(app)
# cache
cache.init_app(app)
# 数据库迁移对象
migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(user_bp)
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)

# 添加命令
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)

# 将处理错误的钩子函数注册到app中
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

if __name__ == '__main__':
    app.run()
