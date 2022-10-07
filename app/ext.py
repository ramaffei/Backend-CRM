from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow import SchemaOpts


ma = Marshmallow()
migrate = Migrate()

class BaseSchemaOpts(SchemaOpts):

    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)
        self.allow_none = getattr(meta, 'allow_none', ())

class BaseSchema(ma.Schema):

    OPTIONS_CLASS = BaseSchemaOpts

    def on_bind_field(self, field_name, field_obj):
        super().on_bind_field(field_name, field_obj)
        if field_name in self.opts.allow_none:
            field_obj.allow_none = True