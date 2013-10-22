try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyqis',
    version='0.1dev',
    author='James R. Garrison',
    packages=[
        'pyqis',
    ],
    install_requires=['numpy', 'ipython[notebook]', 'matplotlib'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
