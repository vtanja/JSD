from os import mkdir, getcwd
from os.path import dirname, exists, join
from sbag.generators.java.custom_paths import new_paths_for_existing_controllers, generate_imports_for_controllers, \
    new_controllers
from sbag.language import Entity, BaseType
from sbag.generators.java import get_type as get_property_type
from sbag.generators.java import plural, first_letter_lower, has_associations, capitalize_first_letter, \
    get_unique_properties, get_template_name_from_path, format_file_name
from textx import generator
from textxjinja import textx_jinja_generator
import re
import datetime


def get_correct_type(prop):
    """
    Returns correct java type if prop type is BaseType or returns correct entity DTO.
    """
    if isinstance(prop.ptype, Entity):
        return 'I{}'.format(prop.ptype.name)
    else:
        return {
            'int': 'number',
            'float': 'number',
            'String': 'string',
            'Long': 'number'
        }.get(prop.ptype.name, prop.ptype.name)


def format_property(prop: str):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", prop)


def get_form_input_type(prop):
    """
    Returns correct form input type for given property type
    """
    if isinstance(prop.ptype, BaseType):
        return {
            'int': 'number',
            'float': 'number',
            'string': 'text',
            'boolean': 'checkbox'
        }.get(prop.ptype.name, prop.ptype.name)


def get_path_for_methods(endpoint):
    paths = endpoint.path.split('/')
    ret = ''
    for p in paths:
        if '{' not in p:
            ret = ret + p + '/'

    return ret


def get_path_parameters(endpoint):
    ret = ''
    for param in endpoint.parameters:
        ret = ret + ' + ' + param + ' + ' + "'/'"

    return ret


@generator('sbag', 'javascript')
def sbag_generate_javascript(metamodel, model, output_path, overwrite, debug, **custom_args):
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

    filters = {
        'get_correct_type': get_correct_type,
        'plural': plural,
        'format_property': format_property,
        'first_letter_lower': first_letter_lower,
        'get_property_type': get_property_type,
        'get_form_input_type': get_form_input_type,
        'has_associations': has_associations,
        'capitalize_first_letter': capitalize_first_letter,
        'get_unique_properties': get_unique_properties,
        'get_template_name_from_path': get_template_name_from_path,
        'format_file_name': format_file_name
        'get_path_for_methods': get_path_for_methods,
        'get_path_parameters': get_path_parameters,
    }

    config['entities'] = model.entities
    entity_names = [ent.name.lower() for ent in model.entities]
    config['new_controllers'] = new_controllers(entity_names, model.paths)
    config['controller_paths'] = new_paths_for_existing_controllers(entity_names, model.paths)
    config['controller_imports'] = generate_imports_for_controllers(config)
    config['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    generate_base_angular_projct(template_folder, output_path, config)

    generate_src_folder(template_folder, output_path, config, overwrite, filters)

    generate_components(template_folder, output_path, model, config, overwrite, filters)


def generate_base_angular_projct(template_folder, output_path, config):
    base_project_template = join(template_folder, 'app', '')
    base_output_path = join(output_path, 'app', '')
    textx_jinja_generator(base_project_template, base_output_path, config)


def generate_src_folder(template_folder, output_path, config, overwrite, filters):
    src_template = join(template_folder, 'src', '')
    src_output_path = join(output_path, 'app', 'src', '')
    textx_jinja_generator(src_template, src_output_path, config, overwrite, filters)


def generate_components(template_folder, output_path, model, config, overwrite, filters):
    entities_folder = join(template_folder, 'entities', '')
    output_path = join(output_path, 'app', 'src', 'app', '')

    for entity in model.entities:
        config['properties'] = entity.properties
        config['entity'] = entity
        config['entity_name'] = format_file_name(entity.name)
        if model.config.project != None:
            config['app_name'] = model.config.project
        textx_jinja_generator(entities_folder, output_path, config, overwrite,
                              filters)
