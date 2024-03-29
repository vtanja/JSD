"""Base module for generating javascript Angular application."""
import datetime
import re
from textx import generator
from textxjinja import textx_jinja_generator
from os import mkdir, getcwd
from os.path import dirname, exists, join
from sbag.language import Entity, BaseType
from sbag.generators.java import get_type as get_property_type
from sbag.generators.java import has_associations, get_unique_properties, get_template_name_from_path, create_imports_for_models, \
    setup_custom_paths_for_generation
from sbag.generators.filters import capitalize_first_letter, first_letter_lower, format_file_name, plural


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


def get_correct_type_custom_paths(endpoint):
    """
    Returns correct type if endpoint type is BaseType or returns correct entity DTO.
    """
    if isinstance(endpoint.post_type, Entity):
        return 'I{}'.format(endpoint.post_type.name.capitalize())
    else:
        return {
            'int': 'number',
            'float': 'number',
            'String': 'string',
            'Long': 'number'
        }.get(endpoint.post_type.name, endpoint.post_type.name)


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
    if '{' in endpoint.path and '}' in endpoint.path:
        for param in endpoint.parameters:
            ret = ret + ' + ' + param + ' + ' + "'/'"
    return ret


def get_custom_path_imports(path):
    ret = set()
    for endpoint in path:
        if isinstance(endpoint.post_type, Entity):
            ret.add(endpoint.post_type)
    return ret


@generator('sbag', 'javascript')
def sbag_generate_javascript(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating javascript Angular project from sbag descriptions"
    this_folder = dirname(__file__)

    config = {}
    config['config'] = model.config

    config['entities'] = model.entities
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
        'get_correct_type_custom_paths': get_correct_type_custom_paths,
        'format_file_name': format_file_name,
        'get_path_for_methods': get_path_for_methods,
        'get_path_parameters': get_path_parameters,
        'get_custom_path_imports': get_custom_path_imports,
    }

    config['model_imports'] = create_imports_for_models(config, model)

    generate_base_angular_projct(template_folder, output_path, config)

    generate_src_folder(template_folder, output_path, config, overwrite, filters)

    generate_components(template_folder, output_path, model, config, overwrite, filters)

    generate_custom_path_services(template_folder, output_path, overwrite, filters, config)


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

def generate_custom_path_services(template_folder, output_path, overwrite, filters, config):
    custom_paths_folder = join(template_folder, 'custom_path')
    custom_paths_output= join(output_path, 'app', 'src', 'app', 'shared', 'service', '')
    for path in config['new_controllers']:
        config['path_name'] = path[0].lower() + path[1:]
        textx_jinja_generator(custom_paths_folder, custom_paths_output, config,
                              overwrite, filters)
