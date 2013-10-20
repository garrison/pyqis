pyqis
=====

python quantum information simulator, written especially for IPython
notebook

https://github.com/garrison/pyqis

Goal: create an easy way to intuitively interact with a quantum
computer simulator using a lucid visual representation.

Install
-------

Install using pip::

    $ pip install -e https://github.com/garrison/pyqis.git#egg=pyqis

And run within ipython notebook::

    $ ipython notebook

You may wish to do this within a virtualenv.

Getting started
---------------

Best run within ipython notebook

.. code::

    from pyqis import QuantumBitMachine

    # create a 4 qubit quantum computer
    machine = QuantumBitMachine(4)

    # apply the X (NOT) gate to bit #2
    machine.X(2)

Author(s)
---------

* Jim Garrison

License
-------

MIT license
