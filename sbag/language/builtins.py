class BaseType():
    """
    Class for defining base types eg. string, double and integer.
    """

    def __init__(self, parent, name):
        """Constuctor for instatiating base types."""
        self.parent = parent
        self.name = name

    def __str__(self):
        """Returns basetype's name as it's string representation."""
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
        """Create entity and put id in it's properties."""
        self.name = name
        self.parent = parent
        self.properties = [Property(self, 'id', BaseType(None, 'Long'))]
        self.properties.extend(properties)

    def __str__(self):
        """Returns entity's name as it's string representation."""
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


class OneToOne():

    def __init__(self, parent, option):
        """One to one entity association type."""
        self.parent = parent
        self.option = option


class OneToMany():

    def __init__(self, parent, owner):
        """One to many entity association type."""
        self.parent = parent
        self.owner = owner


class ManyToOne():

    def __init__(self, parent, option):
        """Many to one entity association type."""
        self.parent = parent
        self.option = option


class ManyToMany:

    def __init__(self, parent, owner):
        """Many to many entity association type."""
        self.parent = parent
        self.owner = owner
