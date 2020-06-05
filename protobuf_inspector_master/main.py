#!/usr/bin/env python3

from sys import stdin, argv
from os.path import ismount, exists, join
from runpy import run_path
from protobuf_inspector_master.lib.types import StandardParser
import protobuf_inspector_master.lib.toJSON


def run(protobuf_response):
    # Parse arguments
    root_type = "root"
    write_json = True


    # Load the config
    config = {}
    directory = "."
    while not ismount(directory):
        filename = join(directory, "protobuf_config.py")
        if exists(filename):
            config = run_path(filename)
            break
        directory = join(directory, "..")

    # Create and initialize parser with config
    parser = StandardParser()
    if "types" in config:
        for type, value in config["types"].items():
            assert(type not in parser.types)
            parser.types[type] = value
    if "native_types" in config:
        for type, value in config["native_types"].items():
            parser.native_types[type] = value

    # Make sure root type is defined and not compactable
    if root_type not in parser.types: parser.types[root_type] = {}
    parser.types[root_type]["compact"] = False

    # PARSE!
    parsed = parser.safe_call(parser.match_handler("message"), protobuf_response, root_type) + "\n"
    #print(parsed)
    if write_json:
        parsedJSON = protobuf_inspector_master.lib.toJSON.run(parsed, write_json=write_json, print_json=False)
    #exit(1 if len(parser.errors_produced) else 0)
    return parsedJSON
