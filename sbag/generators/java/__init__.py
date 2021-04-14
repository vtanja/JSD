from os import mkdir, getcwd
from os.path import dirname, exists, join

from sbag.language import Config, BaseType, OneToMany, ManyToMany, ManyToOne, OneToOne
from textx import generator
from textxjinja import textx_jinja_generator


def plural(entity: str):
    if entity[-2:] in ['ch', 'sh', 'ss', 'es']:
        entity += 'es'
    elif entity[-1] in ['s', 'x', 'z', 'o']:
        entity += 'es'
    elif entity[-1] == 'y':
        if entity[-2] in ['a', 'e', 'i', 'o', 'u']:
            entity += 's'
        else:
            entity = entity[: -1] + 'ies'
    else:
        entity += 's'
    return entity.capitalize()


def get_type(prop):
    """
    Based on property type returns string saying if its base type, list or entity.
    """
    if isinstance(prop.ptype, BaseType):
        return 'base'
    elif isinstance(prop.atype, OneToMany) or isinstance(prop.atype, ManyToMany):
        return 'list'
    else:
        return 'entity'


def get_association_type(prop):
    """
        Based on property returns string saying if its OneToMany, ManyToMany, OneToOne or ManyToOne association
        """
    if isinstance(prop, OneToMany):
        return 'OneToMany'
    elif isinstance(prop, ManyToMany):
        return 'ManyToMany'
    elif isinstance(prop, OneToOne):
        return 'OneToOne'
    elif isinstance(prop, ManyToOne):
        return 'ManyToOne'

def capitalize_first_letter(prop: str):
    return prop[0].upper() + prop[1:]

def is_base_type(prop):
    if isinstance(prop.type, Entity):
        return False
    else:
        return True

@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}
    check_and_setup_config(model)

    config['config'] = model.config
    config['project'] = model.config.project.capitalize()
    config['app'] = model.config.project.lower()

    # If output path is not specified take the current working directory
    if output_path is None:
        output_path = getcwd()

    # Create folder generated where output will be saved
    output_path = join(output_path, 'generated', '')
    if not exists(output_path):
        mkdir(output_path)

    template_folder = join(this_folder, 'templates')

    filters = {
        'plural': plural,
        'get_type': get_type,
        'get_association_type': get_association_type,
        'capitalize_first_letter': capitalize_first_letter,
        'is_base_type', is_base_type
    }

    # Run Jinja generator
    for entity in model.entities:
        config['entity'] = entity
        config['entity_name'] = entity.name
        textx_jinja_generator(template_folder, output_path, config,
                              overwrite, filters)


def check_and_setup_config(model):
    if model.config is None:
        model.config = Config('demo', 'com.example', 'Describe your project here', model)
    if model.config.project == '':
        model.config.project = 'demo'
    if model.config.group == '':
        model.config.group = 'com.example'
    if model.config.description == '':
        model.config.description = 'Describe your project here'
