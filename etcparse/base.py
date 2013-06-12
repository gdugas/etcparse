
class FieldException(Exception):
    pass

class InvalidFormat(Exception):
    pass

class ImplementationError(Exception):
    pass


class Field(object):
    
    pattern = '^(?P<field>.*)$'
    
    class ValidationError(Exception):
        pass
    
    def __init__(self, groupdict = {}):
        self.groupdict = groupdict
    
    def get_identifier(self):
        import uuid
        if not getattr(self, 'uid', None):
            self.uid = str(uuid.uuid4())
        return self.uid
    
    @classmethod
    def match(cls, formatted, offset):
        import re
        m = re.match(cls.pattern, formatted[offset], re.MULTILINE)
        if m:
            f = cls(groupdict=m.groupdict())
            return (f, offset)
    
    def validate(self, value):
        pass
    
    def __unicode__(self):
        if 'field' in self.kwargs:
            return unicode(self.kwargs)
        else:
            return ''
    
    def __str__(self):
        return self.__unicode__()



class BlankField(Field):
    pattern = '^\s*$'
    
    def __unicode__(self):
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
    
    def __unicode__(self):
        str_fieldset = ''
        for field in self.fields:
            str_fieldset = str_fieldset + unicode(field) + '\n'
        return str_fieldset



class Formatter(object):
    
    def format(self, raw):
        formatted = []
        for line in raw.split("\n"):
            formatted.append(line.strip())
        return formatted



class Parser(object):
    
    formatter_class = Formatter
    fieldset_class = Fieldset
    
    def parse(self, content, formatter = None, fieldset = None):
        if not formatter:
            formatter = self.formatter_class()
        
        if not fieldset:
            fieldset = self.fieldset_class()
        
        formatted = formatter.format(content)
        
        i = 0
        clength = len(formatted)
        while i < clength:
            for F in fieldset.fields_class:
                m = F.match(formatted, i)
                if m:
                    (field, offset) = m
                    fieldset[field.get_identifier()] = field
                    i = offset
                    break
            i = i + 1
        
        return fieldset
    
    
    def parse_file(self, path, formatter=None, fieldset=None):
        f = open(path)
        txt = ''
        for line in f:
            txt += line
        return self.parse(txt, formatter=formatter, fieldset=fieldset)

