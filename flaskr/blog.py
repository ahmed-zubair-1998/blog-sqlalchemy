from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_session
from .post import Post
from .user import User
from .comment import Comment
from .flagged_comments import FlaggedComment

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_session()
    posts = db.query(Post, User)\
        .join(User)\
        .all()
    comments = db.query(Comment, User)\
    .join(User)\
    .all()
    return render_template('blog/index.html', posts=posts, comments=comments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_session()
            post = Post(title, body, g.user.id)
            db.add(post)
            db.commit()
            db.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_session().query(Post).join(User).filter(Post.id==id).first()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_session()
            post = db.query(Post).filter(Post.id==id).first()
            post.title = title
            post.body = body
            db.commit()
            db.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_session()
    post = db.query(Post).filter(Post.id==id).first()
    db.delete(post)
    db.commit()
    db.close()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/comment', methods=('GET', 'POST'))
@login_required
def comment(id):
    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_session()
            comment = Comment(body, g.user.id, id)
            db.add(comment)
            db.commit()
            db.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/comment.html')

@bp.route('/<int:id>/', methods=('GET', ))
@login_required
def flag_comment(id):
    user_id = g.user.id
    db = get_session()
    if db.query(FlaggedComment).filter(FlaggedComment.user_id == user_id)\
        .filter(FlaggedComment.comment_id == id).first() is None :

        comment = db.query(Comment).filter(Comment.id == id).first()
        comment.flags += 1
        flagged_comment = FlaggedComment(user_id, id)
        db.add(flagged_comment)
        db.commit()
        db.close()
    return redirect(url_for('blog.index'))
