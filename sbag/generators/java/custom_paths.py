from os.path import join
from sbag.language import Entity, Path

def setup_custom_paths_for_generation(config, model):
    entity_names = [ent.name.lower() for ent in model.entities]
    config['new_controllers'] = new_controllers(entity_names, model.paths)
    config['controller_paths'] = new_paths_for_existing_controllers(entity_names, model.paths)
    config['controller_imports'] = new_imports_for_existing_controllers(config['controller_paths'])


def new_controllers(entity_names, paths):
    new_controllers = []
    for path in paths:
        if path.resource not in entity_names:
            new_controllers.append(path)
    return new_controllers

def new_paths_for_existing_controllers(entity_names, paths):
    controller_paths = {}
    for path in paths:
        if path.resource in entity_names:
            if path.resource.capitalize() not in controller_paths:
                controller_paths[path.resource.capitalize()] = []
            controller_paths[path.resource.capitalize()].extend(endpoints_from_path(path))
    return controller_paths

def new_imports_for_existing_controllers(controller_paths):
    from pudb import set_trace; set_trace()
    controller_imports = {}
    for controller in controller_paths:
        controller_imports[controller] = []
        for path in controller_paths[controller]:
            if isinstance(path.rtype, Entity):
                if path.rtype not in controller_imports[controller]:
                    controller_imports[controller].append(path.rtype)
    return controller_imports

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
            if resource_contains_parameter(content.resource):
                parameters.append(content.resource[1:-1])
            endpoints.extend(endpoints_from_path(content, resource=join(resource, content.resource),
                                                 parameters=parameters))
            if resource_contains_parameter(content.resource):
                parameters.remove(content.resource[1:-1])
        else:
            endpoints.append(EndPoint(content.name, resource, content.rtype, content.post_type, content.rtype_list, parameters))

    return endpoints

def resource_contains_parameter(resource):
    return resource[0] == '{' and resource[-1] == '}'
