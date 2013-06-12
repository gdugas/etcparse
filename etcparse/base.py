class FieldException(Exception):
    pass
class InvalidFormat(Exception):
    pass


class Field(object):
    
    pattern = '^\s*(?P<name>[^\s]*)\s+=\s+(?P<value>.*)\s*;$'
    
    class ValidationError(Exception):
        pass
    
    def __init__(self, name=None, value=None, **kwargs):
        self.name = name
        self.value = value
        self.kwargs = kwargs
    
    @classmethod
    def match(cls, formatted, offset):
        import re
        m = re.match(cls.pattern, formatted[offset], re.MULTILINE)
        if not m:
            return None
        else:
            d = m.groupdict()
            f = cls(**d)
            
            if not f.name:
                name = 'row' + str(offset)
                f.name = name
            
            return (f, offset)
    
    def str_value(self):
        return str(self.cleaned_value())
    
    def clean(self, value):
        return value
    
    def cleaned_value(self):
        value = self.clean(self.value)
        self.validate(value)
        return value
    
    def validate(self, value):
        pass
    
    def __str__(self):
        str_field = " = ".join([str(self.name), self.str_value()])
        return str_field + ";"



class BlankField(Field):
    pattern = '^\s*$'
    
    def __str__(self):
        return ""
    
    def clean(self):
        return ""



class Fieldset(object):
    
    fields_class = [Field, BlankField]
    
    def __init__(self):
        self.index = {}
        self.fields = []
    
    def __getitem__(self, key):
        return self.index[key][1]
    
    def __setitem__(self, key, field):
        cls = getattr(field, '__class__', None)
        
        if not cls or cls not in self.fields_class:
            m = 'field must be a registered Field class'
            raise FieldException(m)
            
        if key in self.index:
            del self[key]
        
        self.fields.append(field)
        i = len(self.fields) - 1
        self.index[key] = (i, field)
    
    def __delitem__(self, key):
        if key in self.index:
            self.fields.pop(self.index[key][0])
        del self.index[key]
    
    def __iter__(self):
        return iter(self.index)
    
    def __str__(self):
        str_fieldset = ''
        for field in self.fields:
            str_fieldset = str_fieldset + str(field) + '\n'
        return str_fieldset



class Formatter(object):
    
    def format(self, raw):
        formatted = []
        for line in raw.split("\n"):
            formatted.append(line.strip())
        return formatted



class Parser(object):
    
    def parse(self, content, formatter = None, fieldset = None):
        
        if not formatter:
            formatter = Formatter()
        if not fieldset:
            fieldset = Fieldset()
        
        formatted = formatter.format(content)
        
        i = 0
        clength = len(formatted)
        while i < clength:
            for F in fieldset.fields_class:
                m = F.match(formatted, i)
                if m:
                    (field, offset) = m
                    fieldset[field.name] = field
                    i = offset
                    break
            i = i + 1
        
        return fieldset
