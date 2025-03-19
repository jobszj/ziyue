from applications.api.imageApi import api_bp

def init_api_bps(app):
    app.register_blueprint(api_bp)