from os import mkdir, getcwd
from os.path import dirname, exists, join

from sbag.language import Entity, Config, BaseType, OneToMany, ManyToMany
from textx import generator
from textxjinja import textx_jinja_generator


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}
    check_and_setup_config(model)

    config['config'] = model.config
    config['project'] = model.config.project.capitalize()
    config['app'] = model.config.project.lower()
    config['type'] = type

    # If output path is not specified take the current working directory
    if output_path is None:
        output_path = getcwd()

    # Create folder generated where output will be saved
    output_path = join(output_path, 'generated', '')
    if not exists(output_path):
        mkdir(output_path)

    template_folder = join(this_folder, 'templates')

    def plural(entity: str):
        if entity[-2 :] in ['ch', 'sh', 'ss', 'es']:
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
#        from pudb import set_trace; set_trace()
        if isinstance(prop.type, BaseType):
            return 'base'
        elif isinstance(prop, OneToMany) or isinstance(prop, ManyToMany):
            return 'list'
        else:
            return 'entity'

    filters = {
        'plural': plural,
        'get_type': get_type
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
