"""
Alias entry point for running the Flask Event Management Application.
Allows running via either `python run.py` or `python app.py`.
"""
import os
from run import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = app.config.get('DEBUG', False)
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
