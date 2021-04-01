from os import mkdir, getcwd
from os.path import dirname, exists, join

from sbag.language import Entity
from textx import generator
from textxjinja import textx_jinja_generator


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}
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

    def get_correct_type(property):
        """
        Returns correct java type if property type is BaseType or
        returns correct entity DTO.
        """
        if isinstance(property.type, Entity):
            return '{}DTO'.format(property.name.capitalize())
        else:
            return {
                'string': 'String'
            }.get(property.type.name, property.type)

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
        
    def get_correct_type_for_model(property):
        """
        Returns correct java type if property type is BaseType or
        returns correct entity DTO.
        """
        if isinstance(property.type, Entity):
            return property.name.capitalize()
        else:
            return {
                'string': 'String'
            }.get(property.type.name, property.type)

    filters = {
        'get_correct_type': get_correct_type,
        'get_correct_type_for_model': get_correct_type_for_model,
        'plural': plural
    }

    # Run Jinja generator
    for entity in model.entities:
        config['entity'] = entity
        config['entity_name'] = entity.name
        textx_jinja_generator(template_folder, output_path, config,
                              overwrite, filters)
