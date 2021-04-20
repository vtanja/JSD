import os
from textx import language, metamodel_from_file, get_location, TextXSyntaxError
from .builtins import *

current_dir = os.path.dirname(__file__)

def method_object_processor(method):
    if method.name not in ['get', 'post', 'head', 'put', 'patch', 'delete']:
        raise TextXSyntaxError('Method name: "{}" not valid.'.format(method.name), **get_location(method))
    if method.name != 'post' and method.post_type is not None:
        raise TextXSyntaxError('Unexpected type after method name.', get_location(method))
    if method.name == 'post' and method.post_type is None:
        raise TextXSyntaxError('Method post missing required request object type.', get_location(method))

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
    obj_processors = {
        'Method': method_object_processor
    }
    mm.register_obj_processors(obj_processors)
    return mm
