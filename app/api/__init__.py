from .checkpoints import bp as checkpoints_bp
from .checkpoint_logs import bp as checkpoint_logs_bp
from .users import bp as users_bp
from .vehicles import bp as vehicles_bp


def register_blueprints(app):
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(checkpoints_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(checkpoint_logs_bp)
