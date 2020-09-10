from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from application import app, db
from controllers.admin import admin_route
from controllers.home import home_route

app.register_blueprint(admin_route, url_prefix='/admin')
app.register_blueprint(home_route, url_prefix='/')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
