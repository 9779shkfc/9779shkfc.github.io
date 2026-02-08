from flask import Flask, render_template
from blueprints.kao import kao_bp
from blueprints.jane import jane_bp
from blueprints.love_design import love_design_bp
from blueprints.media import media_bp
app = Flask(__name__, template_folder='templates', static_folder='static')

def create_app():
    
    # Register blueprints
    app.register_blueprint(kao_bp, url_prefix='/kao')
    app.register_blueprint(jane_bp, url_prefix='/jane')
    app.register_blueprint(love_design_bp, url_prefix='/love-design')
    app.register_blueprint(media_bp, url_prefix='/media')

    # Root route renders homepage
    @app.route('/')
    def index():
        return render_template('index.html', title='Home')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
