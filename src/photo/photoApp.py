from photo import photoApp, photoDB
from photo.models import Photo

@photoApp.shell_context_processor
def make_shell_context():
	return {'photoDB': photoDB, 'Photo': Photo}