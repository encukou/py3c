from distutils.core import setup, Extension

test_py3c_module = Extension(
    'test_py3c',
    sources=['test_py3c.c'],
    include_dirs=['../include'],
    extra_compile_args = ['--std=c++0x', '-l mylib'],
)

setup_args = dict(
    name='test_py3c',
    version='0.0',
    description = '',
    ext_modules = [test_py3c_module]
)

if __name__ == '__main__':
    setup(**setup_args)
