from app.extensions import ma
from app.models import DNSEntry
from marshmallow import validate

class DNSEntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DNSEntry
        load_instance = True
        sqla_session = ma.SQLAlchemy().session

    domain = ma.String(required=True, validate=validate.Length(min=3, max=253))

dns_entry_schema = DNSEntrySchema()
dns_entries_schema = DNSEntrySchema(many=True)
