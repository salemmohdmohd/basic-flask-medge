"""
Flask extensions initialization module.

This module contains the initialization of Flask extensions used throughout
the application. Following the Flask app factory pattern, extensions are
created here and initialized in the main app file.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
