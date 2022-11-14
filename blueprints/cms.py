from flask import Blueprint, render_template, g, redirect, request, flash, url_for
from models.user import PermissionEnum
from decorators import permission_required
from models.user import UserModel, RoleModel
from models.post import PostModel
from forms.cms import AddStaffForm, EditStaffForm
from exts import db
from utils import restful

bp = Blueprint('cms', __name__, url_prefix='/cms')


# 管理页面的视图函数
@bp.get("")
def index():
    return render_template("cms/index.html")


# 如果当前用户不是员工，则不允许访问
@bp.before_request
def cms_before_request():
    if not hasattr(g, "user") or g.user.is_staff is False:
        return redirect("/")


@bp.context_processor
def cms_context_processor():
    return {"PermissionEnum": PermissionEnum}


@bp.get("/staff/list")
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template("cms/staff_list.html", users=users)


@bp.route("/staff/add", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def add_staff():
    if request.method == "GET":
        roles = RoleModel.query.all()
        return render_template("cms/add_staff.html", roles=roles)
    else:
        form = AddStaffForm(request.form)
        if form.validate():
            email = form.email.data
            role_id = form.role.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("没有此用户")
                return redirect(url_for("cms.add_staff"))
            user.is_staff = True
            user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.staff_list"))


# 编辑员工
@bp.route("/staff/edit/<string:user_id>", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff(user_id):
    user = UserModel.query.get(user_id)
    if request.method == 'GET':
        roles = RoleModel.query.all()
        return render_template("cms/edit_staff.html", user=user, roles=roles)
    else:
        form = EditStaffForm(request.form)
        if form.validate():
            is_staff = form.is_staff.data
            role_id = form.role.data
            user.is_staff = is_staff
            if user.role.id != role_id:
                user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.edit_staff", user_id=user_id))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("cms.edit_staff", user_id=user_id))


@bp.route("/users")
@permission_required(PermissionEnum.FRONT_USER)
def user_list():
    users = UserModel.query.filter_by(is_staff=False).all()
    return render_template("cms/users.html", users=users)


@bp.post("/users/active/<string:user_id>")
@permission_required(PermissionEnum.FRONT_USER)
def active_user(user_id):
    is_active = request.form.get("is_active", type=int)
    if is_active is None:
        return restful.param_error(message="请传入is_active参数")
    user = UserModel.query.filter_by(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()


@bp.get("/posts")
@permission_required(PermissionEnum.POST)
def post_list():
    posts = PostModel.query.all()
    return render_template("cms/posts.html", posts=posts)


@bp.post("/posts/active/<int:post_id>")
def active_post(post_id):
    is_active = request.form.get("is_active", type=int)
    if is_active is None:
        return restful.param_error(message="请输入is_active参数")
    post = PostModel.query.get(post_id)
    post.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()
