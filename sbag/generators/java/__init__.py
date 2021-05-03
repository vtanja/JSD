"""Base module for generating java Spring boot application."""
import datetime
import os
from os import mkdir, getcwd
from os.path import dirname, exists, join
from textx import generator
from textxjinja import textx_jinja_generator
from sbag.language import Config, BaseType, Entity, OneToMany, ManyToMany, ManyToOne, OneToOne
from .custom_paths import add_import_to_controller, create_controller_if_doesnt_exist, setup_custom_paths_for_generation
from sbag.generators.filters import capitalize_first_letter, first_letter_lower, format_file_name, plural

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
    if isinstance(prop.atype, OneToMany):
        return 'OneToMany'
    elif isinstance(prop.atype, ManyToMany):
        return 'ManyToMany'
    elif isinstance(prop.atype, OneToOne):
        return 'OneToOne'
    elif isinstance(prop.atype, ManyToOne):
        return 'ManyToOne'


def has_associations(entity: Entity):
    """
    Returns true if entity has any associations as properties
    """
    for prop in entity.properties:
        if hasattr(prop, "atype"):
            return True
    return False


def get_unique_properties(entity):
    ret = set()
    for prop in entity.properties:
        if hasattr(prop, "atype"):
            ret.add(prop.ptype.name)
    return ret


def get_template_name_from_path(path: str):
    tail = os.path.split(path)[-1]
    return tail


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java Spring Boot project from sbag descriptions"

    this_folder = dirname(__file__)

    config = {}
    check_and_setup_config(model)

    config['config'] = model.config
    config['project'] = model.config.project.capitalize()
    config['app'] = model.config.project.lower()
    config['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    setup_custom_paths_for_generation(config, model)

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
        'first_letter_lower': first_letter_lower,
        'has_associations': has_associations,
        'get_unique_properties': get_unique_properties,
        'get_template_name_from_path': get_template_name_from_path,
        'format_file_name': format_file_name
    }

    # Run Jinja generator
    generate_base_project_structure(template_folder, output_path, config,
                                    overwrite, filters)

    generate_entity_based_files(template_folder, output_path, config, model,
                                overwrite, filters)

    generate_custom_path_files(config, template_folder, output_path,
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


def generate_base_project_structure(template_folder, output_path, config, overwrite, filters):
    project_template = join(template_folder, '__project__', '')
    project_output = join(output_path, '__project__', '')
    textx_jinja_generator(project_template, project_output, config,
                          overwrite, filters)


def generate_entity_based_files(template_folder, output_path, config, model,
                                overwrite, filters):
    entities_template = join(template_folder, 'app', '')
    entities_output = join(output_path, '__project__', 'src', 'main', 'java',
                           'com', 'example', '__app__', '')
    for entity in model.entities:
        config['entity'] = entity
        config['entity_name'] = entity.name
        textx_jinja_generator(entities_template, entities_output, config,
                              overwrite, filters)


def generate_custom_path_files(config, template_folder, output_path,
                               overwrite, filters):
    custom_paths_folder = join(template_folder, 'custom_paths')
    custom_paths_output = join(output_path, '__project__', 'src', 'main', 'java', 'com', 'example', '__app__', '')
    for path in config['new_controllers']:
        config['path_name'] = capitalize_first_letter(path)
        textx_jinja_generator(custom_paths_folder, custom_paths_output, config,
                              overwrite, filters)

def create_imports_for_models(config, model):
    imports_dictionary = config['controller_imports']
    for ent in model.entities:
        create_controller_if_doesnt_exist(ent.name, imports_dictionary)
        add_imports_for_entity_properties(ent, imports_dictionary)
    return imports_dictionary

def add_imports_for_entity_properties(entity, imports_dictionary):
    for prop in entity.properties:
        if not isinstance(prop.ptype, BaseType) and prop.ptype.name != entity.name:
            add_import_to_controller(prop.ptype, imports_dictionary[entity.name])
