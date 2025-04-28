import datetime

from flask import Blueprint, render_template, make_response, request, redirect, jsonify, flash, url_for, session
from app.database import db
from app.extensions.user_crud import UserCRUD
from app.extensions.class_form import SignupForm
from app.models import auth_required

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
    if 'user_id' in session:
        return redirect(url_for("auth.user_dashboard_page"))
    return render_template("signup.html")


@auth_bp.route('/in', methods=["GET"])
def signin_page():
    if 'user_id' in session:
        return redirect(url_for("auth.user_dashboard_page"))
    return render_template("signin.html")


@auth_bp.route('/signout', methods=["POST"])
@auth_required
def logout():
    if session['user_id']:
        session.pop('user_id', None)
        session.pop('loggedIn', None)
        return redirect(url_for("page.index_page"))


@auth_bp.route('/signin', methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for("auth.user_dashboard_page"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = None
        error = None

        if not email:
            error = "Username field is empty"
        elif not password:
            error = "Password field is empty"
        else:
            try:
                existing_user = UserCRUD.get_by_email(db.session, email)
                if existing_user is None:
                    error = "This account does not exist, kindly signup in"
            except Exception as e:
                print(f"An error occurred during query for the email at login: {e}")
                error = "Internal error during login"

        if error is None:
            try:
                is_valid = check_password_hash(existing_user.password, password)
                if is_valid:
                    session['user_id'] = existing_user.user_id
                    session['loggedIn'] = True
                    return redirect(url_for("auth.user_dashboard_page"))
                else:
                    error = "Incorrect password"
            except Exception as e:
                print(f"Error trying to login account: {e}")
                error = "Internal error during login"

        flash(error)

        return render_template("signin.html")


@auth_bp.route('/signup', methods=["GET", "POST"])
def register():
    if 'user_id' in session:
        return redirect(url_for("auth.user_dashboard_page"))

    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_pass")
        error = None

        if not email:
            error = "Email field is required"
        elif not password:
            error = "Password field is required"
        elif not confirm_pass:
            error = "Confirm your password is required"
        elif password != confirm_pass:
            error = "Passwords do not match"
        else:
            try:
                existing_users = UserCRUD.get_by_email(db.session, email)
                if existing_users:
                    error = "User already exists"
            except Exception as e:
                print(f"error occurred during query for signup: {e}")
                error = "Internal error during login"

        if error is None:
            try:
                hashed_pass = generate_password_hash(password)
                new_user = UserCRUD.create(db.session,
                                           {"full_name": full_name,
                                            "email": email,
                                            "password": hashed_pass,
                                            "date_of_creation": datetime.date.today()})
                return redirect(url_for("auth.signin_page"))
            except Exception as e:
                db.session.rollback()
                error = f"An error occurred during user creation: {str(e)}"

        flash(error)

        return render_template("signup.html")


@auth_bp.route('/user/dashboard', methods=["GET"])
@auth_required
def user_dashboard_page():
    return render_template('user_dashboard.html')


template_bp = Blueprint('page', __name__, url_prefix="/")


@template_bp.route("/", methods=["GET"])
def index_page():
    if 'user_id' in session:
        return redirect(url_for("auth.user_dashboard_page"))
    return render_template('index.html')