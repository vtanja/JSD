import re; 

def capitalize_first_letter(prop: str):
    return prop[0].upper() + prop[1:]

def first_letter_lower(string: str):
    return string[0].lower() + string[1:]

def format_file_name(entity_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', entity_name)
    ret = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    return ret

def plural(entity: str):
    if entity[-2:] in ['ch', 'sh', 'ss', 'es']:
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
    return capitalize_first_letter(entity)