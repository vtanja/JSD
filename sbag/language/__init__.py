import os
from textx import language, metamodel_from_file

current_dir = os.path.dirname(__file__)


class BaseType():
    """
    Class for defining base types eg. string, double and integer...
    """

    def __init__(self, parent, name):
        """Constuctor for instatiating base types."""
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


class Property():
    """
    Defines both base properties and associations.
    """

    def __init__(self, parent, name, ptype):
        """Constructor for BaseTypes and Associations properties."""
        self.parent = parent
        self.name = name
        self.ptype = ptype


class Entity():
    """
    Class for defining entities.
    """

    def __init__(self, name, parent, properties):
        """Constructor for Entities."""
        self.name = name
        self.parent = parent
        self.properties = [Property(self, 'id', BaseType(None, 'Long'))]
        self.properties.extend(properties)

    def __str__(self):
        return self.name


class Config():
    """
    Class for defining project configuration.
    """

    def __init__(self, project, group, description, parent):
        """Create config instance."""
        self.project = project
        self.group = group
        self.description = description
        self.parent = parent


class OneToMany():

    def __init__(self, parent, name, owner, ptype):
        """Instantiate one to many associations."""
        self.parent = parent
        self.name = name
        self.owner = owner
        self.pype = ptype


class ManyToMany():

    def __init__(self, parent, name, owner, ptype):
        """Instantiate many to many associations."""
        self.parent = parent
        self.name = name
        self.owner = owner
        self.ptype = ptype


@language('sbag', '*.sbag')
def sbag_language():
    "sbag language"

    builtin_types = {
        'int': BaseType(None, 'int'),
        'String': BaseType(None, 'String'),
        'float': BaseType(None, 'float'),
        'boolean': BaseType(None, 'boolean'),
        'Long': BaseType(None, 'Long')
    }
    mm = metamodel_from_file(os.path.join(current_dir, 'sbag.tx'),
                             classes=[BaseType, Entity, Config, Property, OneToMany, ManyToMany],
                             builtins=builtin_types,
                             debug=True)

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm
