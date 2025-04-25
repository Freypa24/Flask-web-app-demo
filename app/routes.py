import datetime

from flask import Blueprint, render_template, make_response, request, redirect, jsonify, flash, url_for
from app.database import db
from app.extensions.user_crud import UserCRUD
from app.models import User, auth_required

from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__, url_prefix="/users")


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        if request.method != "GET":
            return make_response("Malformed Request"), 400

        user = UserCRUD.get_one(db.session, user_id)

        if not user:
            return make_response(f"No such user found")

        return jsonify({
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "date_of_creation": user.date_of_creation.isoformat()
        })

    except Exception as e:
        return make_response(f"Problem during process, error is: {e}"), 400


auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/up', methods=["GET"])
def signup_page():
    return render_template("signup.html")


@auth_bp.route('/in', methods=["GET"])
def signin_page():
    return render_template("signin.html")


@auth_bp.route('/signin', methods=["GET", "POST"])
def login():
    '''
    To be worked on for login logic
    :return:
    '''
    return render_template("signin.html")


@auth_bp.route('/signup', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        error = None

        if not email:
            error = "Username field is required"
        elif not password:
            error = "Password field is required"
        else:
            existing_users = User.query.filter(User.email == email).first()
            if existing_users:
                error = "User already exists"

        if error is None:
            try:
                hashed_pass = generate_password_hash(password)
                new_user = UserCRUD.create(db.session,
                                           {"full_name": full_name,
                                            "email": email,
                                            "password": hashed_pass,
                                            "date_of_creation": datetime.date.today()})
                return redirect(url_for("auth.signin")), 200
            except Exception as e:
                return render_template("signup.html", error=str(e))

        flash(error)

        return render_template("signup.html")


@auth_bp.route('/user/dashboard', methods=["GET"])
@auth_required
def user_dashboard_page():
    return render_template('user_dashboard.html')


template_bp = Blueprint('page', __name__, url_prefix="/")


@template_bp.route("/", methods=["GET"])
def index_page():
    return render_template('index.html')