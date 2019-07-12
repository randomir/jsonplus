import jsonplus
from flask import current_app


class JSONEncoder(jsonplus.JSONEncoder):
    """Thin wrapper around :class:`jsonplus.JSONEncoder` that propagates
    :class:`flask.current_app` config options to ``jsonplus`` encoder.
    """

    def __init__(self, **kw):
        kw.setdefault('exact', current_app.config['JSONPLUS_EXACT'])
        super(JSONEncoder, self).__init__(**kw)


class FlaskJSONPlus(object):
    """Flask-JSONPlus extension class."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # if not specified in config, default to jsonplus' exact coding
        app.config.setdefault('JSONPLUS_EXACT', True)

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['jsonplus'] = self

        app.json_encoder = JSONEncoder
        app.json_decoder = jsonplus.JSONDecoder


    # interface to common ``jsonplus`` functions

    def dumps(*pa, **kw):
        return jsonplus.dumps(*pa, **kw)

    def loads(*pa, **kw):
        return jsonplus.loads(*pa, **kw)

    def dump(*pa, **kw):
        return jsonplus.dump(*pa, **kw)

    def load(*pa, **kw):
        return jsonplus.load(*pa, **kw)

    def pretty(obj, **kw):
        return jsonplus.pretty(obj, **kw)
