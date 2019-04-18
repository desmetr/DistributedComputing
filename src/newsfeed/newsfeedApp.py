from newsfeed import newsfeedApp

@newsfeedApp.shell_context_processor
def make_shell_context():
	return {}