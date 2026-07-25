from flask_sqlalchemy import SQLAlchemy

# Package-level SQLAlchemy instance for app/models model modules.
db = SQLAlchemy()

from .Checkpoint import Checkpoint
from .Registration import Registration
from .Vehicle import Vehicle
