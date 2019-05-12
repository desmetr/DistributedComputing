from advertising import advApp, advDB
from advertising.models import Advertisement

@advApp.shell_context_processor
def make_shell_context():
	return {'advDB': advDB, 'Advertisement': Advertisement}

if __name__=='__main__':
    advApp.run(debug=True)