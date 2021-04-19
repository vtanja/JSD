from os.path import join
from sbag.language import Entity, Path

def setup_custom_paths_for_generation(config, model):
    entity_names = [ent.name.lower() for ent in model.entities]
    config['new_controllers'] = new_controllers(entity_names, model.paths)
    config['controller_paths'] = new_paths_for_existing_controllers(entity_names, model.paths)
    config['controller_imports'] = new_imports_for_existing_controllers(config['controller_paths'])
    extend_imports_with_post_object_types(config)

def new_controllers(entity_names, paths):
    new_controllers = []
    for path in paths:
        if path.resource not in entity_names:
            new_controllers.append(path)
    return new_controllers

def new_paths_for_existing_controllers(entity_names, paths):
    controller_paths = {}
    for path in paths:
        add_paths_to_appropriate_controller(path, entity_names, controller_paths)
    return controller_paths

def add_paths_to_appropriate_controller(path, entity_names, controller_paths):
    if path.resource in entity_names:
        create_controller_if_doesnt_exist(path, controller_paths)
        controller_paths[path.resource.capitalize()].extend(endpoints_from_path(path))

def create_controller_if_doesnt_exist(path, controller_paths):
    if path.resource.capitalize() not in controller_paths:
        controller_paths[path.resource.capitalize()] = []

def new_imports_for_existing_controllers(controller_paths):
    controller_imports = {controller:generate_imports_for_controller(controller_paths[controller]) \
                          for controller in controller_paths}
    return controller_imports

def generate_imports_for_controller(controller_paths):
    controller_imports = []
    for path in controller_paths:
        if isinstance(path.rtype, Entity):
            add_import_to_controller(path.rtype, controller_imports)
    return controller_imports

def add_import_to_controller(entity, controller_imports):
    if import_already_added(entity, controller_imports):
       controller_imports.append(entity)

def import_already_added(entity, controller_imports):
    return entity not in controller_imports

class EndPoint():

    def __init__(self, method, path, rtype, post_type, rtype_list, parameters):
        self.method = method
        self.path = path
        self.rtype = rtype
        self.post_type = post_type
        self.rtype_list = rtype_list
        self.parameters = [param for param in parameters]

    def get_correct_type(self):
        return self.rtype if self.rtype_list == '' else 'List<{}>'.format(str(self.rtype))

    def function_name(self):
        function_name = ''
        for part in self.path.split('/'):
            function_name = ''.join([function_name, part.replace('{', '').replace('}', '').capitalize()])
        return ''.join([self.method, function_name])

def endpoints_from_path(path, resource='', parameters=[]):
    endpoints = []
    for content in path.content:
        if isinstance(content, Path):
            handle_subpath_endpoints(content, parameters, endpoints, resource)
        else:
            endpoints.append(EndPoint(content.name, resource, content.rtype, content.post_type, content.rtype_list, parameters))

    return endpoints

def handle_subpath_endpoints(content, parameters, endpoints, resource):
    add_parameters_from_path(content, parameters)
    endpoints.extend(endpoints_from_path(content, resource=join(resource, content.resource),
                                         parameters=parameters))
    remove_added_parameters_from_path(content, parameters)

def add_parameters_from_path(content, parameters):
    if resource_contains_parameter(content.resource):
        parameters.append(content.resource[1:-1])

def remove_added_parameters_from_path(content, parameters):
    """Remove parameters to avoid backwards propagation. We only want to propagate parameters forwards."""
    if resource_contains_parameter(content.resource):
        parameters.remove(content.resource[1:-1])

def resource_contains_parameter(resource):
    return resource[0] == '{' and resource[-1] == '}'

def extend_imports_with_post_object_types(config):
    for controller in config['controller_paths']:
        add_import_for_post_methods(controller, config)

def add_import_for_post_methods(controller, config):
    for endpoint in config['controller_paths'][controller]:
        if endpoint.method == 'post':
            add_import_to_controller(endpoint.post_type, config['controller_imports'][controller])
