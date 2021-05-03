from sbag.language import Entity, Path
from sbag.generators import capitalize_first_letter, first_letter_lower

class EndPoint():

    def __init__(self, method, path, rtype, post_type, rtype_list, parameters):
        """Create instnaces of Endpoint which are used to generate controllers."""
        self.method = method
        self.path = path
        self.rtype = rtype
        self.post_type = post_type
        self.rtype_list = rtype_list
        self.parameters = [param for param in parameters]

    def get_correct_type(self):
        response_type = {
            'int': 'Integer',
            'long': 'Long',
            'double': 'Double',
        }.get(self.rtype.name, self.rtype)
        return response_type if self.rtype_list == '' else 'List<{}>'.format(response_type)

    def function_name(self):
        function_name = ''
        for part in self.path.split('/'):
            function_name = ''.join([function_name, part.replace('{', '').replace('}', '').capitalize()])
        return ''.join([self.method, function_name])


def setup_custom_paths_for_generation(config, model):
    entity_names = [first_letter_lower(ent.name) for ent in model.entities]
    config['new_controllers'] = new_controllers(entity_names, model.paths)
    config['controller_paths'] = new_paths_for_existing_controllers(entity_names, model.paths)
    config['controller_imports'] = generate_imports_for_controllers(config)


def new_controllers(entity_names, paths):
    new_controllers = {}
    for path in paths:
        if path.resource not in entity_names:
            if path not in new_controllers:
                new_controllers[capitalize_first_letter(path.resource)] = []
            new_controllers[capitalize_first_letter(path.resource)].extend(endpoints_from_path(path))
    return new_controllers


def new_paths_for_existing_controllers(entity_names, paths):
    controller_paths = {}
    for path in paths:
        add_paths_to_appropriate_controller(path, entity_names, controller_paths)
    return controller_paths


def add_paths_to_appropriate_controller(path, entity_names, controller_paths):
    if path.resource in entity_names:
        create_controller_if_doesnt_exist(capitalize_first_letter(path.resource), controller_paths)
        controller_paths[capitalize_first_letter(path.resource)].extend(endpoints_from_path(path))

def create_controller_if_doesnt_exist(controller, controller_paths):
    if controller not in controller_paths:
        controller_paths[controller] = []

def generate_imports_for_controllers(config):
    controller_paths = {**config['controller_paths'], **config['new_controllers']}
    controller_imports = {controller:generate_imports_for_controller(controller, controller_paths[controller]) \
                          for controller in controller_paths}
    extend_imports_with_request_object_types(controller_paths, controller_imports)
    return controller_imports

def generate_imports_for_controller(controller, controller_paths):
    controller_imports = []
    for path in controller_paths:
        if isinstance(path.rtype, Entity) and path.rtype.name != controller:
            add_import_to_controller(path.rtype, controller_imports)
    return controller_imports


def add_import_to_controller(entity, controller_imports):
    if import_already_added(entity, controller_imports):
        controller_imports.append(entity)


def import_already_added(entity, controller_imports):
    return entity not in controller_imports


def endpoints_from_path(path, resource='', parameters=None):
    endpoints = []
    if parameters is None: parameters = []
    for content in path.content:
        if isinstance(content, Path):
            handle_subpath_endpoints(content, parameters, endpoints, resource)
        else:
            endpoints.append(
                EndPoint(content.name, resource, content.rtype, content.post_type, content.rtype_list, parameters))

    return endpoints


def handle_subpath_endpoints(content, parameters, endpoints, resource):
    add_parameters_from_path(content, parameters)
    endpoints.extend(endpoints_from_path(content, resource='/'.join([resource, content.resource]),
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


def extend_imports_with_request_object_types(controller_paths, controller_imports):

    for controller in controller_paths:
        add_imports_for_request_objects(controller, controller_paths[controller], controller_imports)




def add_imports_for_request_objects(controller, controller_paths, controller_imports):
    for endpoint in controller_paths:
        if endpoint.post_type != '' and endpoint.post_type is not None:
            add_import_to_controller(endpoint.post_type, controller_imports[controller])
