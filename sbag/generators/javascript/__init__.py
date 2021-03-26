import os
from functools import partial
from textx import generator, gen_file, get_output_filename


@generator('sbag', 'javascript')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    output_file = get_output_filename(model.file_name, output_path, '*.sbag')
    gen_file(model.file_name, output_file,
             partial(generator_callback, model, output_file),
             overwrite,
             success_message='To start this angular application run: ng serve')


def generator_callback(model, output_file):
    """
    A generator function taht produces output_file from model.
    """
    # TODO: Write here code taht produce generated output
