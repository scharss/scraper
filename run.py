from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables and admin user."""
    db.create_all()
    Role.insert_roles()
    admin_email = "admin@agrocopilot.xyz"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin = User(email=admin_email, username='admin')
        admin.set_password('Hholaadmin256@')
        admin.role = Role.query.filter_by(name='Administrator').first()
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.") 