from os import mkdir, getcwd
from os.path import dirname, exists, join

from sbag.language import Entity
from textx import generator
from textxjinja import textx_jinja_generator
import re


@generator('sbag', 'javascript')
def sbag_generate_javascript(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"
    this_folder = dirname(__file__)

    config = {}
    config['config'] = model.config
    config['get_type'] = type

    # If output path is not specified take the current working directory
    if output_path is None:
        output_path = getcwd()

    # Create folder generated where output will be saved
    output_path = join(output_path, 'generated', '')
    if not exists(output_path):
        mkdir(output_path)

    template_folder = join(this_folder, 'templates')

    def get_correct_type(prop):
        """
        Returns correct java type if prop type is BaseType or returns correct entity DTO.
        """
        if isinstance(prop.type, Entity):
            return 'I{}'.format(prop.name.capitalize())
        else:
            return {
                'int': 'number',
                'float': 'number'
            }.get(prop.type.name, prop.type.name)

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

    def format_property(prop: str):
        return re.sub(r"(\w)([A-Z])", r"\1 \2", prop)

    def first_letter_lower(string: str):
        return string[0].lower() + string[1:]

    filters = {
        'get_correct_type': get_correct_type,
        'plural': plural,
        'format_property': format_property,
        'first_letter_lower': first_letter_lower,
    }

    config['entities'] = model.entities

    for entity in model.entities:
        config['properties'] = entity.properties
        config['entity'] = entity
        config['entity_name'] = entity.name.lower()
        textx_jinja_generator(template_folder, output_path, config, overwrite,
                              filters)
