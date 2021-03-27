
from textx import generator


@generator('sbag', 'javascript')
def sbag_generate_javascript(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"
    pass


def generator_callback(model, output_file):
    """
    A generator function taht produces output_file from model.
    """
    # TODO: Write here code taht produce generated output
