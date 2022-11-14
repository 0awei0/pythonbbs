from enum import Enum
from exts import db
from datetime import datetime
from shortuuid import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))

    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('RoleModel', backref='users')

    # 直接传password自动完成加密
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        ans = check_password_hash(self.password, raw_password)
        return ans

    # 用来快速判断当前用户是否具有某个权限
    def has_permission(self, permission):
        return permission in [permission.name for permission in self.role.permissions]


class PermissionEnum(Enum):
    """
        存放权限类型的枚举
    """
    BOARD = '板块'
    POST = '帖子'
    COMMENT = '评论'
    FRONT_USER = '前台用户'
    CMS_USER = '后台用户'


class PermissionModel(db.Model):
    """
        用户权限表，权限的类型从PermissionEnum中获取,不是直接和用户关联，而是先跟角色关联再跟用户关联
    """
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)


#
role_permission_table = db.Table(
    "role_permission_table",
    db.Column("role_id", db.Integer, db.ForeignKey('role.id')),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)


class RoleModel(db.Model):
    """
        主键id， 角色描述desc， 创建时间，关系属性permissions与PermissionModel进行关联
        RoleModel和PermissionModel属于多对多的关系
        通过PermissionModel对象的roles属性即可访问到权限下所有与其关联的角色
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 角色名称
    name = db.Column(db.String(50), nullable=False)
    # 角色描述
    desc = db.Column(db.String(200), nullable=True)
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 拥有权限
    permissions = db.relationship('PermissionModel', secondary=role_permission_table, backref="roles")
