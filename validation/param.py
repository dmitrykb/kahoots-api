import re


class Param():
    
    def __init__(self):
        self.name = None
        self.type = "string"
        self.required = False
        self.error_code = 0
        self.value = None
        self.allowed_values = []
        self.error_message = None
        self.min_value = None
        self.max_value = None
        self.regex = None
        
        self.validation_map = {
            "string": self.validate_string,
            "int": self.validate_int,            
            "float": self.validate_float,
            "enum": self.validate_enum,
            "int_array": self.validate_int_array,
            "string_array": self.validate_string_array
            }
    
    def validate(self):
        # required check
        if (not self.value and self.required):
            self.error_message = self.name + " is missing"
            return
        # ignore if missing
        if (self.value is None):
            return
        # check type
        validation_function = self.validation_map[self.type]
        is_valid, error_message = validation_function()
        if not is_valid:
            self.error_message = error_message
            return

    def get_error_message(self):
        return self.error_message
    
    def validate_string(self):
        isvalid = True
        if self.regex:
            isvalid = re.match(self.regex, self.value)
        if not isvalid:
            return(False, self.print_invalid_value())
        else:
            return (True, "")
    
    def validate_int(self):
        try:
            int(self.value)
            if(self.not_in_range()):
                return (False, self.print_not_in_range())
            return (True, "")
        except ValueError as e:
            return (False, self.print_invalid_int())

    def validate_float(self):
        try:
            float(self.value)
            return True, ""
        except ValueError as e:
            return (False, self.print_invalid_float())

    def not_in_range(self):
        if self.min_value is not None and int(self.value) < int(self.min_value):
            return True
        if self.max_value is not None and int(self.value) > int(self.max_value):
            return True
        return False

    def validate_enum(self):
        if len(self.allowed_values) == 0:
            return (True, "")
        for allowed_value in self.allowed_values:
            if (allowed_value == self.value):
                return (True, "")
        return (False, self.print_invalid_enum())

    def validate_int_array(self):
        try:
            values = str(self.value).split(',')
            for value_to_test in values:
                try:
                    int(value_to_test)
                    pass
                except:
                    return (False, self.print_invalid_int_array())
        except:
            return (False, self.print_invalid_int_array())
        return (True, "")

    def validate_string_array(self):
        try:
            values = str(self.value).split(',')
            for value_to_test in values:
                try:
                    str(value_to_test)
                    pass
                except:
                    return (False, self.print_invalid_string_array())
        except:
            return (False, self.print_invalid_string_array())
        return (True, "")



    
    def print_invalid_value(self):
        return self.name + " is invalid: '" + self.value + "'"
    
    def print_invalid_int(self):
        return self.name + " is invalid: '" + self.value + "' is not an integer"

    def print_invalid_float(self):    
        return self.name + " is invalid: '" + self.value + "' is not a number"
        
    def print_invalid_enum(self):
        return self.name + " is invalid: '" + self.value + "' (" + '/'.join(map(str,self.allowed_values)) + ")"

    def print_not_in_range(self):
        return self.name + " is not in range "

    def print_invalid_int_array(self):
        return self.name + " should be list of int values separated with ','"

    def print_invalid_string_array(self):
        return self.name + " should be list of string values separated with ','"
