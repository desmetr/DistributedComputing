# import loginApp, loginDB
from login import loginApp, loginDB
# from models import User
from login.models import User, Friendship

@loginApp.shell_context_processor
def make_shell_context():
	return {'loginDB': loginDB, 'User': User, "Friendship": Friendship}