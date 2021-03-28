from os import mkdir
from os.path import dirname, exists, join

from textx import generator
from textxjinja import textx_jinja_generator


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}

    if output_path is None:
        output_path = join(this_folder, 'gen', '')
        if not exists(output_path):
            mkdir(output_path)

    template_folder = join(this_folder, 'templates')

    # Run Jinja generator
    for entity in model.entities:
        config['entity'] = entity
        config['entity_name'] = entity.name
        entity_path = join(output_path, entity.name, '')
        if not exists(entity_path):
            mkdir(entity_path)
        textx_jinja_generator(template_folder, entity_path, config,
                              overwrite)
