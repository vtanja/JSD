import os
from textx import language, metamodel_from_file

current_dir = os.path.dirname(__file__)


class BaseType():
    """Class for defining base types eg. string, double and integer..."""

    def __init__(self, parent, name):
        """Constuctor for instatiating base types."""
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


class Entity():
    """Class for defining entities."""

    def __init__(self, name, parent, properties):
        """Constructor for Entities."""
        self.name = name
        self.parent = parent
        self.properties = properties

    def __str__(self):
        return self.name


class Config():
    """Class for defining project configuration."""

    def __init__(self, project, group, description, parent):
        """Create config instance."""
        self.project = project
        self.group = group
        self.description = description
        self.parent = parent


@language('sbag', '*.sbag')
def sbag_language():
    "sbag language"

    builtin_types = {
        'int': BaseType(None, 'int'),
        'string': BaseType(None, 'string'),
        'float': BaseType(None, 'float'),
        'boolean': BaseType(None, 'boolean')
    }
    mm = metamodel_from_file(os.path.join(current_dir, 'sbag.tx'),
                             classes=[BaseType, Entity, Config],
                             builtins=builtin_types,
                             debug=True)

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm
