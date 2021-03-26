import os
from functools import partial
from textx import generator, gen_file, get_output_filename


@generator('sbag', 'java')
def sbag_generate_java(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating java from sbag descriptions"

    output_file = get_output_filename(model.file_name, output_path, '*.sbag')
    gen_file(model.file_name, output_file,
             partial(generator_callback, model, output_file),
             overwrite,
             success_message="""To start Spring Boot application you need maven installed
             Run mvn clean install
             Following with java -jar target/<name_of_the_app>.0.0.1.SNAPSHOT.jar""")


def generator_callback(model, output_file):
    """
    A generator function taht produces output_file from model.
    """
    # TODO: Write here code taht produce generated output
