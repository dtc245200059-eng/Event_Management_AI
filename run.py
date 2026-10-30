"""
Entry point for running the Flask Event Management Application.
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = app.config.get('DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
