from neomodel import StructuredNode, StringProperty

class Rootnode(StructuredNode):
    name = StringProperty(required = True)

class Normalnode(StructuredNode):
    name = StringProperty(required = True)