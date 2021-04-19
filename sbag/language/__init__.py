import os
from textx import language, metamodel_from_file
from .builtins import *

current_dir = os.path.dirname(__file__)



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
                             classes=[BaseType, Entity, Config, Property,
                                      OneToOne, OneToMany, ManyToOne, ManyToMany,
                                      Path, Method],
                             builtins=builtin_types,
                             debug=True)

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm
