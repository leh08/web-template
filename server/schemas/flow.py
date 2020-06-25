from schema import BaseSchema
from models.flow import FlowModel


class FlowSchema(BaseSchema):   
    class Meta(BaseSchema.Meta):
        model = FlowModel