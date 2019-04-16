from location import locationApp

@locationApp.shell_context_processor
def make_shell_context():
	return {}