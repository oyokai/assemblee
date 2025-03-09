# routes/__init__.py

from routes.accueil import accueil_bp
from routes.programme import programme_bp

def init_app(app):
    app.register_blueprint(accueil_bp)
    app.register_blueprint(programme_bp)