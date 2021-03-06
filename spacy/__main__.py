# coding: utf8
from __future__ import print_function
# NB! This breaks in plac on Python 2!!
#from __future__ import unicode_literals

import plac
from spacy.cli import download as cli_download
from spacy.cli import link as cli_link
from spacy.cli import info as cli_info
from spacy.cli import package as cli_package
from spacy.cli import train as cli_train


class CLI(object):
    """Command-line interface for spaCy"""

    commands = ('download', 'link', 'info', 'package', 'train')

    @plac.annotations(
        model=("model to download (shortcut or model name)", "positional", None, str),
        direct=("force direct download. Needs model name with version and won't "
                "perform compatibility check", "flag", "d", bool)
    )
    def download(self, model=None, direct=False):
        """
        Download compatible model from default download path using pip. Model
        can be shortcut, model name or, if --direct flag is set, full model name
        with version.
        """

        cli_download(model, direct)


    @plac.annotations(
        origin=("package name or local path to model", "positional", None, str),
        link_name=("name of shortuct link to create", "positional", None, str),
        force=("force overwriting of existing link", "flag", "f", bool)
    )
    def link(self, origin, link_name, force=False):
        """
        Create a symlink for models within the spacy/data directory. Accepts
        either the name of a pip package, or the local path to the model data
        directory. Linking models allows loading them via spacy.load(link_name).
        """

        cli_link(origin, link_name, force)


    @plac.annotations(
        model=("optional: shortcut link of model", "positional", None, str),
        markdown=("generate Markdown for GitHub issues", "flag", "md", str)
    )
    def info(self, model=None, markdown=False):
        """
        Print info about spaCy installation. If a model shortcut link is
        speficied as an argument, print model information. Flag --markdown
        prints details in Markdown for easy copy-pasting to GitHub issues.
        """

        cli_info(model, markdown)


    @plac.annotations(
        input_dir=("directory with model data", "positional", None, str),
        output_dir=("output parent directory", "positional", None, str),
        force=("force overwriting of existing folder in output directory", "flag", "f", bool)
    )
    def package(self, input_dir, output_dir, force=False):
        """
        Generate Python package for model data, including meta and required
        installation files. A new directory will be created in the specified
        output directory, and model data will be copied over.
        """

        cli_package(input_dir, output_dir, force)


    @plac.annotations(
        lang=("model language", "positional", None, str),
        output_dir=("output directory to store model in", "positional", None, str),
        train_data=("location of JSON-formatted training data", "positional", None, str),
        dev_data=("location of JSON-formatted development data (optional)", "positional", None, str),
        n_iter=("number of iterations", "option", "n", int),
        parser_L1=("L1 regularization penalty for parser", "option", "L", float),
        no_tagger=("Don't train tagger", "flag", "T", bool),
        no_parser=("Don't train parser", "flag", "P", bool),
        no_ner=("Don't train NER", "flag", "N", bool)
    )
    def train(self, lang, output_dir, train_data, dev_data=None, n_iter=15,
              parser_L1=0.0, no_tagger=False, no_parser=False, no_ner=False):
        """
        Train a model. Expects data in spaCy's JSON format.
        """

        cli_train(lang, output_dir, train_data, dev_data, n_iter, not no_tagger,
                  not no_parser, not no_ner, parser_L1)


    def __missing__(self, name):
        print("\n   Command %r does not exist."
              "\n   Use the --help flag for a list of available commands.\n" % name)


if __name__ == '__main__':
    import plac
    import sys
    cli = CLI()
    sys.argv[0] = 'spacy'
    plac.Interpreter.call(CLI)
