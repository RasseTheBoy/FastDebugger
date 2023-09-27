import inspect, sys, executing, os

from dataclasses    import dataclass
from functools      import wraps
from traceback      import format_exc
from datetime       import datetime
from textwrap       import dedent
from os.path        import basename
from colored        import fg, attr
from typing         import Any


def try_traceback(print_traceback=False) -> Any:
    """Decorator to catch and handle exceptions raised by a function.
    
    Parameters
    ----------
    print_traceback : bool, optional
        Whether to skip printing the traceback information. Default is False.
    
    Returns
    -------
    Any
        The decorated function.
    """
    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if print_traceback:
                    print(f'{format_exc()}\n')
                return None
        return wrapper
    return try_except


class Source(executing.Source):
    """Class to get the source code of a function or method."""
    def get_text_with_indentation(self, node) -> str:
        """Get the source code of a node, including indentation.
        
        Parameters
        ----------
        node : ast.AST
            The node to get the source code of.
            
        Returns
        -------
        str
            The source code of the node, including indentation."""
        result = self.asttokens().get_text(node)
        if '\n' in result:
            result = ' ' * node.first_token.start[1] + result
            result = dedent(result)
        result = result.strip()
        return result


@dataclass
class FD_Variable:
    """Class to store and format variables for Fast Debugger."""

    variable:Any
    use_center:bool = True
    center_amnt:int = 5

    def __post_init__(self):
        self.variable_type = self.variable.__class__.__name__
        self.color = self.get_color()
        self.format_variables()

    def get_color(self):
        """Returns the color of the variable type.
        
        Returns
        -------
        str
            The color of the variable type.
        """
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
            case 'list' | 'ndarray' | 'tuple' | 'dict' | 'set' | 'benedict':
                return 'cornsilk_1'
            case _:
                raise TypeError(f'Unsupported type: {self.variable_type}')

    def format_variables(self):
        def add_center(var_in) -> Any:
            """Adds centering to the variable type.
            
            Parameters
            ----------
            var_in : Any
                The variable to add centering to.
            
            Returns
            -------
            str
                The variable with centering added.
            """
            if self.use_center:
                return str(var_in).center(self.center_amnt)

        def add_color(var_in) -> str:
            """Adds color to the variable type and variable.
            
            Parameters
            ----------
            var_in : Any
                The variable to add color to.
            
            Returns
            -------
            str
                The variable with color added."""
            var_in = str(var_in)
            if not self.color:
                return var_in
                
            return fg(self.color) + var_in + attr('reset')

        self.variable_type = add_center(self.variable_type)

        self.variable_type, self.variable = [add_color(x) for x in (self.variable_type, self.variable)]

    def get_type_and_variable(self):
        """Returns the type and variable of the FD_Variable object.
        
        Returns
        -------
        tuple : (str, Any)
            The type and variable of the FD_Variable object."""
        return self.variable_type, self.variable


@dataclass
class FastDebugger:
    """Fast Debugger (`fd`) is a function that allows you to quickly debug and inspect variables.

    - Print out the type, length, and value of variables passed as arguments.
    - Print out the type, index, and value of elements within a iterable object.
    - Can be `enabled` or `disabled`. When disabled, will not print anything.
    - Prints out the current time by default.
    - Has a `try_traceback` decorator that can be used to catch any exceptions that may occur while using fd.
    - Use the `nl` parameter to print a newline after each fd print statement.

    Usage
    -----
    `fd(variable_1, variable_2, ...)`

    Parameters
    ----------
    *args : Any
        The variables to be inspected.
    nl : bool, optional
        Print a newline after each fd print statement. Default is False.
    end_nl : bool, optional
        Print a newline after the fd print statement. Default is None.
    exit : bool, optional
        Exit the program after the fd print statement. Default is False.
    """
    
    enabled:bool = True
    nl:bool = False
    end_nl:bool = True
    exit:bool = False

    def is_args_empty(self, args):
        """Checks if `args` is empty.
        If args is not empty, returns False.
        If args is empty, prints the current time and returns True.
        
        Parameters
        ----------
        args : Any
            The variables to be inspected.
            
        Returns
        -------
        bool
            Whether `args` is empty.
        """
        if args != ():
            return False
        return True

    def disable(self):
        """Disables Fast Debugger."""
        self.enabled = False

    def enable(self):
        """Enables Fast Debugger."""
        self.enabled = True

    def config(self, **kwargs):
        """Configures Fast Debugger.
        
        Parameters
        ----------
        **kwargs : Any
            The variables to configure.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    

    @try_traceback()
    def __call__(self, *args:Any, **kwargs) -> None:
        """
        Executes Fast Debugger functionality.

        Parameters
        ----------
        args : Any
            The variables to be inspected.
        nl : bool, optional
            Print a newline after each fd print statement. Default is False.
        end_nl : bool, optional
            Print a newline after the fd print statement. Default is None.
        exit : bool, optional
            Exit the program after the fd print statement. Default is False.
        """

        def check_input(input_value_name:str, self_value:Any) -> Any:
            """Checks if the input value is in kwargs.
            
            Parameters
            ----------
            input_value_name : str
                The name of the input value.
            
            Returns
            -------
            Any
                The input value if it is in kwargs, else the self value.
            """
            return kwargs.get(input_value_name, self_value)

        def add_center(var_in:Any, center_amnt:int=3) -> str:
            """Adds centering to the variable type.
            
            Parameters
            ----------
            var_in : Any
                The variable to add centering to.
            
            Returns
            -------
            str
                The variable with centering added.
            """
            return str(var_in).center(center_amnt)
        
        def get_prefix(indx:int, arr:Any) -> str:
            """Gets the prefix for the variable type.
            
            Parameters
            ----------
            indx : int
                The index of the variable.
            
            Returns
            -------
            str
                The prefix for the variable type.
            """
            if indx == len(arr)-1:
                return ' ╚'
            else:
                return ' ╟' 

        def print_args_pairs(args_pairs):
            """Prints the arguments passed to `fd`.
            
            Parameters
            ----------
            args_pairs : list[tuple]
                The arguments passed to `fd`.
            """
            for arg_variable_name, arg_variable_value in args_pairs:
                arg_variable_type = arg_variable_value.__class__.__name__

                if arg_variable_type in ('list', 'ndarray', 'tuple', 'set'):
                    print(f'fd | {add_center(arg_variable_type, 5)} | {add_center(len(arg_variable_value))} | {arg_variable_name}')
                    for array_indx, array_variable in enumerate(arg_variable_value):
                        arr_variable_type, variable = FD_Variable(array_variable).get_type_and_variable()
                        print(f'{get_prefix(array_indx, arg_variable_value)} | {arr_variable_type} | {add_center(array_indx)} | {variable}')

                elif arg_variable_type in ('dict', 'benedict'):
                    print(f'fd | {add_center(arg_variable_type, 5)} | {add_center(len(arg_variable_value))} | {arg_variable_name}')
                    for dict_indx, (dict_key, dict_variable) in enumerate(arg_variable_value.items()):
                        dict_variable_type, dict_variable = FD_Variable(dict_variable).get_type_and_variable()                    
                        print(f'{get_prefix(dict_indx, arg_variable_value)} | {dict_variable_type} | {add_center(dict_indx)} | {dict_key}: {dict_variable}')

                else:
                    variable_type, variable = FD_Variable(arg_variable_value).get_type_and_variable()
                    print(f'fd | {variable_type} | {arg_variable_name}: {variable}')
                
                if nl:
                    print()

        # Check input values
        nl = check_input('nl', self.nl)
        end_nl = check_input('end_nl', self.end_nl)
        exit = check_input('exit', self.exit)

        # Check if args is empty or fd is disabled
        if self.is_args_empty(args) or not self.enabled:
            # Prints the current time as output
            time_now = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            print(f'fd | {time_now}')
        
        else:
            # Get context
            callFrame = sys._getframe(2)
            callNode = Source.executing(callFrame).node
            args_pairs = self._formatArgs(callFrame, callNode, args)

            # Print args
            print_args_pairs(args_pairs)

        # Print extra newline
        if (end_nl == None and self.end_nl) or end_nl:
            print()

        # Exit program if given
        if exit:
            os._exit(0)


    def _formatArgs(self, callFrame, callNode, args) -> list[tuple]:
        """Formats the arguments passed to `fd`
        
        Parameters
        ----------
        callFrame : frame
            The frame of the call to `fd`
        callNode : ast.Call
            The node of the call to `fd`
        args : Any
            The arguments passed to `fd`
        
        Returns
        -------
        list[tuple]
            The formatted arguments passed to `fd`
        """
        source = Source.for_frame(callFrame)
        sanitizedArgStrs = [source.get_text_with_indentation(arg) for arg in callNode.args] # type: ignore

        pairs = list(zip(sanitizedArgStrs, args))
        
        return pairs


    def _getContext(self, callFrame, callNode):
        """Gets the context of the call to `fd`
        
        Parameters
        ----------
        callFrame : frame
            The frame of the call to `fd`
        callNode : ast.Call
            The node of the call to `fd`
        
        Returns
        -------
        tuple : (str, int, str)
            The filename, line number, and parent function of the call to `fd`
        """
        lineNumber = callNode.lineno
        frameInfo = inspect.getframeinfo(callFrame)
        parentFunction = frameInfo.function
        filename = basename(frameInfo.filename)

        return filename, lineNumber, parentFunction



fd = FastDebugger()