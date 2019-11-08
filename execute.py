import six
from vk_api.utils import sjson_dumps


class VkFunction(object):
    __slots__ = ('code', '_minified_code', 'args', 'clean_args', 'return_raw')

    def __init__(self, code, args=None, clean_args=None, return_raw=False):
        self.code = code
        self._minified_code = minify(code)

        self.args = () if args is None else args
        self.clean_args = () if clean_args is None else clean_args

        self.return_raw = return_raw

    def compile(self, args):
        compiled_args = {}

        for key, value in six.iteritems(args):
            if key in self.clean_args:
                compiled_args[key] = str(value)
            else:
                compiled_args[key] = sjson_dumps(value)

        return self._minified_code % compiled_args

    def __call__(self, *args, **kwargs):
        args = parse_args(self.args, args, kwargs)

        return {'code': self.compile(args)}


def minify(code):
    return ''.join(i.strip() for i in code.splitlines())


def parse_args(function_args, args, kwargs):
    parsed_args = {}

    for arg_name in six.iterkeys(kwargs):
        if arg_name in function_args:
            parsed_args[arg_name] = kwargs[arg_name]
        else:
            raise Exception()

    args_count = len(args) + len(kwargs)
    func_args_count = len(function_args)

    if args_count != func_args_count:
        raise Exception()

    for arg_name, arg_value in zip(function_args, args):
        parsed_args[arg_name] = arg_value

    return parsed_args
