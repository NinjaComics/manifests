#!/usr/bin/python2.7

##
# This is a translator between json and md+yaml files that are
# used by static site generators such as jekyll and pelican (with
# a plugin). The post content gets loaded as the description field
# and all other front-matter is preserved as object fields.
#
# Give it one (or possibly more) input files that are either json or
# md+yaml and it will output either md+yaml or json files for you.
##

import argparse
import yaml
import json


def read_yaml(yaml_file):
    '''
    The name is a lie. This actually reads a md file with yaml
    frontmatter. The md content winds up in the description field
    of the generated object. Otherwise the yaml load is straight
    forward.
    ''' 
    f = open(yaml_file, 'r')
    c = f.read()
    yaml_index = c.rfind('---') 
    yaml_content = c[:yaml_index]
    yaml_data = yaml.load(yaml_content)
    description = c[yaml_index+4:]
    yaml_data['description'] = description
    return yaml_data


def read_json(json_file):
    '''
    Pretty straight forward json load since we don't do anything
    fancy with json output.
    '''
    json_data = json.load(json_file)
    return json_data


def read_file(file_name_list):
    '''
    Determine input file type and call the appropriate reader.
    This is just a wrapper so main doesn't have to have logic.
    '''
    metadata = {}
    for file_name in file_name_list:
        if file_name.endswith('md'):
            module_name = file_name.strip('.md')
            metadata[module_name] = read_yaml(file_name)
        elif file_name.endswith('json'):
            module_name = file_name.strip('.json')
            metadata[module_name] = read_json(file_name)
        else:
            print "This file does not end with json or yaml"
        return metadata


def write_output(output_format, output_loc, metadata):
    '''
    Determine the output type and call the appropriate function.
    This is just a wrapper so main doesn't have to have logic.
    '''
    if output_format == 'json':
        write_json(output_loc, metadata)
    elif output_format == 'yaml':
        write_yaml(output_loc, metadata)
    else:
        print "Output format not known"


def write_json(output_loc, metadata):
    '''
    Just a standard json dump. The description field winds up
    looking hideous.
    '''
    for module in metadata.keys():
        json_pp = json.dumps(metadata[module], sort_keys=True,
                    indent=4, separators=(',', ': '))
        module_file_parts = module.split('/')
        if output_loc is None:
            output_loc = '/'.join(module_file_parts[:-1])
        fname = output_loc + "/" + module_file_parts[-1] + ".json"
        ofile = open(fname, "w")
        ofile.write(json_pp)
        ofile.close()


def write_yaml(output_loc, metadata):
    '''
    The name is a lie. This actually prints a yaml+md document
    that can be used in pelican/jekyll like page generators.
    The description is set as the page content, everything else
    is yaml frontmatter.
    '''
    for module in metadata.keys():
        try:
          description = metadata[module].pop('description')
        except:
          description = ''
        yaml_pp = yaml.dump(metadata[module], default_flow_style=False)
        module_file_parts = module.split('/')
        if output_loc is None:
            output_loc = '/'.join(module_file_parts[:-1])
        fname = output_loc + "/" + module_file_parts[-1] + ".md"
        ofile = open(fname, "w")
        ofile.write('---\n')
        ofile.write(yaml_pp)
        ofile.write('---\n')
        ofile.write(description)
        ofile.close()


def parse_options():
    '''
    Set up our translator options
    '''
    parser = argparse.ArgumentParser(description="Convert between yaml and json files")
    parser.add_argument("--file", dest="infile", type=str, nargs="+",
                            help="The input file(s) to process")
    parser.add_argument("--format", dest="output_format", type=str, default="json",
                            help="The output format (json or yaml)")
    parser.add_argument("--output", dest="output_loc", type=str,
                            help="The output directory")
    return parser.parse_args()


if __name__ == '__main__':
    options = parse_options()
    metadata = read_file(options.infile)
    write_output(options.output_format, options.output_loc, metadata)
