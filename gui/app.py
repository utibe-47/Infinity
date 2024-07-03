import os
from gui.user_interface import create_app


app = create_app(os.getenv('GUI_ENV') or 'prod')
