from os import mkdir, getcwd
from os.path import dirname, exists, join

from textx import generator
from textxjinja import textx_jinja_generator


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}
    config['config'] = model.config

    # If output path is not specified take the current working directory
    if output_path is None:
        output_path = getcwd()

    # Create folder generated where output will be saved
    output_path = join(output_path, 'generated', '')
    if not exists(output_path):
        mkdir(output_path)

    template_folder = join(this_folder, 'templates')

    # Run Jinja generator
    for entity in model.entities:
        config['entity'] = entity
        config['entity_name'] = entity.name
        textx_jinja_generator(template_folder, output_path, config,
                              overwrite)
