from applications.route.imageApi import api_bp

def init_api_bps(app):
    app.register_blueprint(api_bp)