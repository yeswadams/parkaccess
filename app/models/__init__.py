from flask_sqlalchemy import SQLAlchemy

# Package-level SQLAlchemy instance for app/models model modules.
db = SQLAlchemy()

from .checkpoint import Checkpoint
from .vehicle import Vehicle
from .users import User
from .checkpoint_logs import CheckpointLog
