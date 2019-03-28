from location import locationApp

@locationApp.shell_context_processor
def make_shell_context():
	return {}
	# return {'photoDB': photoDB, 'Photo': Photo}