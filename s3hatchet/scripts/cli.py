# Skeleton of a CLI

import click, json

import s3hatchet

@click.group()
def cli():
    pass

@click.command('load')
@click.argument('output_dump', type=click.Path(exists=False))
@click.argument('input_ls', default='-', required=False)
@click.option('--extract-template', '-et', nargs=2, type=str)
@click.option('--summarize', '-s', nargs=2)
def load(input_ls, output_dump, extract_template, summarize):
    try:
        input_ls = click.open_file(input_ls).readlines()
    except IOError:
        input_ls = [input_ls]

    extractRegex, attributes = extract_template

    attributes = json.loads(attributes)

    sField, sVar = summarize

    sVar = json.loads(sVar)

    s3hatchet.loader(input_ls, output_dump, extractRegex, attributes, sField, sVar)

cli.add_command(load)
