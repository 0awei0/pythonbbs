import os

from flask import Blueprint, request, render_template, jsonify, current_app, url_for, send_from_directory, g, flash, \
    redirect
from werkzeug.utils import secure_filename
from models.post import BoardModel, PostModel, CommentModel
from exts import csrf, db
from decorators import login_required
from forms.post import PublicPostForm
from utils import restful
from flask_paginate import Pagination

bp = Blueprint('front', __name__, url_prefix='')


# 发布帖子的视图
@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.title.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.param_error(message=message)


# 主页视图
@bp.route("/")
def index():
    boards = BoardModel.query.all()
    # 获取页码参数
    page = request.args.get("page", type=int, default=1)
    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 当前page的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)

    # 总共有多少帖子
    total = query_obj.count()
    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)
    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }

    return render_template("front/index.html", **context)


@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()
    return render_template("front/post_detail.html", post=post)


# 把帖子id通过url参数传过来，然后通过表单获取评论内容
@bp.route("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
    form = PublicPostForm(request.form)
    if form.validate():
        content = form.content.data
        comment = CommentModel(content=content, post_id=post_id, author=g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    return redirect(url_for("front.post_detail", post_id=post_id))


# 上传图片的视图函数
@bp.route("/upload/image")
@csrf.exempt
@login_required
def upload_image():
    f = request.files.get('image')
    extension = f.filename.split(".")[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return jsonify({
            'errno': 400,
            "data": []
        })
    filename = secure_filename(f.filename)
    # 保存图片到默认路径
    f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename))
    url = url_for('media.media_file', filename=filename)
    return jsonify({
        'errno': 0,
        "data": [{
            "url": url,
            "alt": "",
            "href": ""
        }]
    })
