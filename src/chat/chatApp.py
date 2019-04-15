from chat import chatApp, chatDB
from chat.models import Chat

@chatApp.shell_context_processor
def make_shell_context():
	return {'chatDB': chatDB, 'Chat': Chat}

if __name__=='__main__':
    chatApp.run(debug=True)