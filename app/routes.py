import datetime

from flask import Blueprint, render_template, make_response, request, redirect, jsonify, flash, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.database import db
from app.extensions.user_crud import UserCRUD
from app.extensions.workforce_crud import WorkforceCRUD
from app.extensions.class_form import SignupForm, SigninForm, RemoveEmployeeForm, AddEmployeeForm
from app.extensions.checker import validate_password
from app.models import auth_required, admin_required, employee_required

from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def apply_rate_limit(app):
    """Apply rate limiting and check for exhaustion (failed login attempts)."""
    limiter.init_app(app)

    @app.before_request
    def log_rate_limit():
        # Print or log the current rate limit status for debugging
        print(f"Rate Limit: {request.remote_addr}")

@admin_bp.route("/<int:id>", methods=["GET"])
@admin_required
def get_workforce(id):
    try:
        if request.method != "GET":
            return make_response("Malformed Request"), 400

        workforce = WorkforceCRUD.get_one(db.session, id)

        if not workforce:
            return make_response(f"No workforce found with id")

        return jsonify({
            "workforce_id": workforce.id,
            "workforce_name": workforce.name,
            "admin": workforce.admin[0],
            "employees": [
                {
                    "user_id": employee.id,
                    "full_name": employee.full_name,
                    "email": employee.email,
                    "date_of_creation": employee.date_of_creation
                } for employee in workforce.employees
            ]
        })

    except Exception as e:
        return make_response(f"Problem during process, error is: {e}"), 400


@admin_bp.route("/remove", methods=["POST"])
@admin_required
def remove_employee():
    try:
        if request.method != "POST":
            return make_response("Malformed Request"), 400

        form = RemoveEmployeeForm()

        if form.validate_on_submit():
            employee = UserCRUD.get_one(db.session, form.employee_id.data)
            if employee:
                UserCRUD.update(db.session, employee, {"workforce_id": None})

                return redirect(url_for("auth.admin_dashboard_page"))
        return redirect(url_for("auth.admin_dashboard_page"))
    except Exception as e:
        print(f"Error trying to remove employee from workforce. {e}")
        return make_response("Internal server error", 500)


@admin_bp.route("/add", methods=["POST"])
@admin_required
def add_employee():
    try:
        if request.method != "POST":
            return make_response("Malformed Request"), 400

        unassigned = UserCRUD.get_all(db.session, filters={
            'workforce_id': None,
            'role': 'employee'
        }) or []

        form = AddEmployeeForm()
        form.employee_id.choices = [
            (emp.id, f"{emp.full_name} - {emp.role} - {emp.email}") for emp in unassigned
        ]

        if form.validate_on_submit():

            employee = UserCRUD.get_one(db.session, form.employee_id.data)
            if employee:
                admin_id = session.get('user_id')
                admin = UserCRUD.get_one(db.session, admin_id)

                UserCRUD.update(db.session, employee, {"workforce_id": admin.administered_workforces[0].id})

                return redirect(url_for("auth.admin_dashboard_page"))
        return redirect(url_for("auth.admin_dashboard_page"))
    except Exception as e:
        print(f"Error trying to add employee to workforce. {e}")
        return make_response(f"Internal server error {e}", 500)

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/signout', methods=["POST"])
@auth_required
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('loggedIn', None)
        session.pop('role', None)
        return redirect(url_for("page.index_page"))


@auth_bp.route('/signin', methods=["GET", "POST"])
@limiter.limit("10 per 3 minutes")
def login():
    if 'user_id' in session and session.get('role') == "employee":
        return redirect(url_for("auth.user_dashboard_page"))
    elif 'user_id' in session and session.get('role') == "admin":
        return redirect(url_for("auth.admin_dashboard_page"))

    form = SigninForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        existing_user = None
        error = None

        try:
            existing_user = UserCRUD.get_by_email(db.session, email)
            if existing_user is None:
                error = "This account does not exist, kindly signup."
        except Exception as e:
            print(f"An error occurred during query for the email at login: {e}")
            error = "Internal error during login"

        if error is None:
            try:
                is_valid = check_password_hash(existing_user.password, password)
                if is_valid:
                    session['user_id'] = existing_user.id
                    session['loggedIn'] = True
                    session['role'] = existing_user.role
                    if session['role'] is "admin":
                        return redirect(url_for("auth.admin_dashboard_page"))
                    else:
                        return redirect(url_for("auth.user_dashboard_page"))
                else:
                    error = "Incorrect password"
            except Exception as e:
                print(f"Error trying to login account: {e}")
                error = f"Internal error during login {e}"

        flash(error, "danger")

    return render_template("signin.html", form=form)


@auth_bp.route('/signup', methods=["GET", "POST"])
@limiter.limit("10 per 3 minutes")
def register():
    if 'user_id' in session and session.get('role') == "employee":
        return redirect(url_for("auth.user_dashboard_page"))
    elif 'user_id' in session and session.get('role') == "admin":
        return redirect(url_for("auth.admin_dashboard_page"))

    form = SignupForm()
    error = None

    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        confirm_pass = form.confirm_password.data

        if password != confirm_pass:
            error = "Passwords do not match"
        elif not validate_password(password):
            error = "Password is not strong enough"
        else:
            try:
                existing_users = UserCRUD.get_by_email(db.session, email)
                if existing_users:
                    error = "User already exists"
            except Exception as e:
                print(f"error occurred during query for signup: {e}")
                error = f"Internal error during login {e}"

        if error is None:
            try:
                hashed_pass = generate_password_hash(password)
                new_user = UserCRUD.create(db.session,
                                           {"full_name": full_name,
                                            "email": email,
                                            "password": hashed_pass,
                                            "date_of_creation": datetime.date.today()})
                flash("Account successfully created. Please log in.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                db.session.rollback()
                error = f"An error occurred during user creation: {str(e)}"

        flash(error, "danger")

    elif request.method == 'POST':
        for field_errors in form.errors.values():
            for field_error in field_errors:
                flash(field_error, "danger")
                break

    return render_template("signup.html", form=form)


@auth_bp.route('/user/dashboard', methods=["GET"])
@auth_required
@employee_required
@limiter.exempt
def user_dashboard_page():
    user = UserCRUD.get_one(db.session, session['user_id'])
    return render_template('user_dashboard.html', user=user)


@auth_bp.route('/admin/dashboard', methods=["GET"])
@admin_required
@limiter.exempt
def admin_dashboard_page():
    admin = UserCRUD.get_one(db.session, session['user_id'])

    # Check if an admin handles a workforce
    if admin.administered_workforces:
        workforce = admin.administered_workforces[0]
        workforce_id = workforce.id
    else:
        workforce_id = None

    employees = UserCRUD.get_all(db.session,
                                 filters={
                                     'workforce_id': workforce_id,
                                     'role': 'employee'
                                 })
    unassigned = UserCRUD.get_all(db.session,
                                    filters={
                                        'workforce_id': None,
                                        'role': 'employee'
                                    }) or []

    employee_choices = [(emp.id, f"{emp.full_name} - {emp.role} - {emp.email}") for emp in unassigned]
    add_form = AddEmployeeForm()
    add_form.employee_id.choices = employee_choices

    remove_forms = {emp.id: RemoveEmployeeForm(employee_id=emp.id) for emp in employees}

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        employees=employees,
        unassigned=unassigned,
        add_form=add_form,
        remove_forms=remove_forms
    )


template_bp = Blueprint('page', __name__, url_prefix="/")


@template_bp.route("/", methods=["GET"])
@limiter.exempt
def index_page():
    if 'user_id' in session and session.get('role') == "employee":
        return redirect(url_for("auth.user_dashboard_page"))
    elif 'user_id' in session and session.get('role') == "admin":
        return redirect(url_for("auth.admin_dashboard_page"))

    return render_template('index.html')