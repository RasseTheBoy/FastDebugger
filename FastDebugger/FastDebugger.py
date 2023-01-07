from icecream   import ic

# from FastDebugger   import fd
import numpy as np

import traceback

from py_basic_commands  import fprint, try_traceback
from dataclasses    import dataclass
from datetime   import datetime
from colored    import fg, attr
from typing     import Any

@dataclass
class FD_Variable:
    variable:Any
    use_center:bool = True
    center_amnt:int = 5

    def __post_init__(self):
        self.variable_type = self.variable.__class__.__name__
        self.color = self.get_color()
        self.format_variables()

    def get_color(self):
        match self.variable_type:
            case 'bool':
                if self.variable:
                    return 'green'
                else:
                    return 'red'
            case 'int' | 'float':
                return 'blue'
            case 'str':
                self.variable = f'{self.variable!r}'
            case 'list' | 'ndarray' | 'tuple' | 'dict' | 'set':
                return 'cornsilk_1'

    def format_variables(self):
        def add_center(var_in):
            if self.use_center:
                return str(var_in).center(self.center_amnt)

        def add_color(var_in):
            var_in = str(var_in)
            if not self.color:
                return var_in
                
            return fg(self.color) + var_in + attr('reset')

        self.variable_type = add_center(self.variable_type)

        self.variable_type, self.variable = [add_color(x) for x in (self.variable_type, self.variable)]

    def get_type_and_variable(self):
        return self.variable_type, self.variable


class FastDebugger:
    def find_fd_brackets(self, code:str) -> Any:
        fd_indxs = []
        for char_indx, char in enumerate(code):
            if code[char_indx-2:char_indx+1] == 'fd(':
                fd_indxs.append({'start': char_indx+1, 'end': None})
            elif char == ')':
                for x in fd_indxs[::-1]:
                    if not x['end']:
                        x['end'] = char_indx
        self.fd_indxs = fd_indxs


    def is_args_empty(self, args):
        if args != ():
            return False
        
        time_now = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        print(f'fd | {time_now}')
        return True
    

    @try_traceback()
    def __call__(self, *args:Any, nl:bool=False):
        def add_center(var_in:Any, center_amnt:int=3):
            return str(var_in).center(center_amnt)
        
        def get_prefix(indx:int, arr:Any):
            if indx == len(arr)-1:
                return ' ╚'
            else:
                return ' ╟' 

        if self.is_args_empty(args):

            return

        filename, lineno, function_name, code = traceback.extract_stack()[-3]

        if ';' in code:
            code_split = code.split(';')
            for func in code_split:
                if 'fd(' in func:
                    code = func
                    continue
        
        self.find_fd_brackets(code)

        var_lst = [x.strip() for x in code[self.fd_indxs[0]['start']:self.fd_indxs[0]['end']].split(',')]
        for var_indx, args_variable in enumerate(args):
            args_variable_type:str = args_variable.__class__.__name__

            if args_variable_type in ('list', 'ndarray', 'tuple', 'set'):
                print(f'fd | {add_center(args_variable_type, 5)} | {add_center(len(args_variable))} | {var_lst[var_indx]}')
                for array_indx, array_variable in enumerate(args_variable):
                    arr_variable_type, variable = FD_Variable(array_variable).get_type_and_variable()
                    print(f'{get_prefix(array_indx, args_variable)} | {arr_variable_type} | {add_center(array_indx)} | {variable}')

            elif args_variable_type == 'dict':
                print(f'fd | {add_center(args_variable_type, 5)} | {add_center(len(args_variable))} | {var_lst[var_indx]}')
                for dict_indx, (dict_key, dict_variable) in enumerate(args_variable.items()):
                    dict_variable_type, dict_variable = FD_Variable(dict_variable).get_type_and_variable()                    
                    print(f'{get_prefix(dict_indx, args_variable)} | {dict_variable_type} | {add_center(dict_indx)} | {dict_key}: {dict_variable}')

            else:
                variable_type, variable = FD_Variable(args_variable).get_type_and_variable()
                print(f'fd | {variable_type} | {var_lst[var_indx]}: {variable}')

            if nl:
                print()

fd = FastDebugger()