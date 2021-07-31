import setuptools

assert tuple(map(int, setuptools.__version__.split('.')[:3])) >= (39, 2, 0), \
    'Please upgrade setuptools by `pip install -U setuptools`'

setuptools.setup()
