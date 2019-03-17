from login import loginApp, loginDB
from login.models import User

@loginApp.shell_context_processor
def make_shell_context():
	return {'loginDB': loginDB, 'User': User}