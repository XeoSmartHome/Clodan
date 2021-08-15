import json

from App import app, init_app


app.config.from_file('../config.json', json.load)


init_app()


app.run()
