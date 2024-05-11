from flask import Flask
import importlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints dynamically
blueprints = ['auth', 'student', 'lecturer', 'admin', 'projects', 'notifications']
for blueprint_name in blueprints:
    module = importlib.import_module(f'{blueprint_name}')
    blueprint = getattr(module, f'create_{blueprint_name}_blueprint')()
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
