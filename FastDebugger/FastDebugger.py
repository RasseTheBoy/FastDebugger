import inspect, sys, executing

from py_basic_commands  import try_traceback
from dataclasses    import dataclass
from datetime   import datetime
from textwrap   import dedent
from os.path    import basename
from colored    import fg, attr
from typing     import Any


class Source(executing.Source):
    def get_text_with_indentation(self, node):
        result = self.asttokens().get_text(node)
        if '\n' in result:
            result = ' ' * node.first_token.start[1] + result
            result = dedent(result)
        result = result.strip()
        return result


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
    enabled:bool = True

    def is_args_empty(self, args):
        if args != ():
            return False
        
        time_now = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        print(f'fd | {time_now}')
        return True


    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
    

    @try_traceback()
    def __call__(self, *args:Any, nl:bool=False):
        def add_center(var_in:Any, center_amnt:int=3):
            return str(var_in).center(center_amnt)
        
        def get_prefix(indx:int, arr:Any):
            if indx == len(arr)-1:
                return ' ╚'
            else:
                return ' ╟' 

        if self.is_args_empty(args) or not self.enabled:
            return

        callFrame = sys._getframe(2)
        callNode = Source.executing(callFrame).node
        args_pairs = self._formatArgs(callFrame, callNode, args)

        for arg_variable_name, arg_variable_value in args_pairs:
            arg_variable_type = arg_variable_value.__class__.__name__
            if arg_variable_type in ('list', 'ndarray', 'tuple', 'set'):
                print(f'fd | {add_center(arg_variable_type, 5)} | {add_center(len(arg_variable_value))} | {arg_variable_name}')
                for array_indx, array_variable in enumerate(arg_variable_value):
                    arr_variable_type, variable = FD_Variable(array_variable).get_type_and_variable()
                    print(f'{get_prefix(array_indx, arg_variable_value)} | {arr_variable_type} | {add_center(array_indx)} | {variable}')

            elif arg_variable_type == 'dict':
                print(f'fd | {add_center(arg_variable_type, 5)} | {add_center(len(arg_variable_value))} | {arg_variable_name}')
                for dict_indx, (dict_key, dict_variable) in enumerate(arg_variable_value.items()):
                    dict_variable_type, dict_variable = FD_Variable(dict_variable).get_type_and_variable()                    
                    print(f'{get_prefix(dict_indx, arg_variable_value)} | {dict_variable_type} | {add_center(dict_indx)} | {dict_key}: {dict_variable}')

            else:
                variable_type, variable = FD_Variable(arg_variable_value).get_type_and_variable()
                print(f'fd | {variable_type} | {arg_variable_name}: {variable}')
            
            if nl:
                print()

    def _formatArgs(self, callFrame, callNode, args):
        source = Source.for_frame(callFrame)
        sanitizedArgStrs = [
            source.get_text_with_indentation(arg)
            for arg in callNode.args]

        pairs = list(zip(sanitizedArgStrs, args))
        
        return pairs

    def _getContext(self, callFrame, callNode):
        lineNumber = callNode.lineno
        frameInfo = inspect.getframeinfo(callFrame)
        parentFunction = frameInfo.function
        filename = basename(frameInfo.filename)

        return filename, lineNumber, parentFunction

fd = FastDebugger()