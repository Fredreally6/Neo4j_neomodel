from neomodel import db,config, StructuredNode, StringProperty

class Rootnode(StructuredNode):
    name = StringProperty(required = True)

class Normalnode(StructuredNode):
    name = StringProperty(required = True)