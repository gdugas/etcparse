
# Philosophy

- a config file is a Fieldset container, which contain Fields
- a Field can be one or multiple lines from the config file
- a Field can represent anything from the config file (key / value,
comment, empty line)
- a field can contain a Fieldset (eg: sections in a ini file)


# Quickstart

Here is a simple config file, which contain only key / value pairs:

    var1 = value1;
    
    var2 = value2;
    
    var3 = value3;

First, you need to specify a formatter, which will clean and format your 
config file content:

    formatter = etcparse.Formatter()

Then, you just call your parser, which return the Fieldset associated 
to you config file content:

    parser = etcparse.Parser()
    fieldset = parser.parse(conf)

You can now accessing to your parameters through the fieldset like a 
dict

    var1 = fieldset['var1']
    for k in fieldset:
        field = fieldset[k]
        print field.cleaned_value()

and display your fieldset content in your config file format

    print str(fieldset)


# Installation

With easy_install or pip  
> https://github.com/gdugas/etcparse/archive/master.zip  

or simply download the tarball, unzip, and run  
> python setup.py install

