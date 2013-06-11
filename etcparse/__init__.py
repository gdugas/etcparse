from etcparse.base import Field, Fieldset, Formatter, Parser,\
                          FieldException, InvalidFormat

def parse_file(path, parser):
    f = open(path)
    conf = ''
    for line in f:
        conf += line
    f.close()
    return parser.parse(conf)

