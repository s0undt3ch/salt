Salt's Python Requirements
==========================

Salt is currently using pip-tools to lock down the python requirements to specific versions.
The reason for this is stability.

Install Python Dependencies
---------------------------

Salt currently defines several requirements files, each defines a set of python requiremnts.

* ``base.in``: Core requirements to run salt
* ``zeromq.in``: Requirements to Salt's default communication transport
* ``dev.in``: Development requirements
* ``tests.in``: Test suite requiremnts
* ``opt.in``: Optional requirements

Under Python 2
~~~~~~~~~~~~~~

.. code-block:: sh

   pip install -r requiremnts/py2/<requirements-file>.txt

Under Python 3
~~~~~~~~~~~~~~

.. code-block:: sh

   pip install -r requiremnts/py3/<requirements-file>.txt


New Python Dependency
---------------------

When adding a new python dependency, please select the appropriate requirements file,
the ``.in`` requirements file, not any of the ``.txt`` requirements files.

Once that's done, the requirements files will need to be regenerated.
Both a ``python2`` and a ``python3`` binaries are required, the reason for this is
that python 2 requiremnts are different than python 3 requirements and that difference
needs to go into separate requirements files.


(Re)Generate Python 2 Requirements Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   make compile-requirements-py2

(Re)Generate Python 3 Requirements Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   make compile-requirements-py3


Upgrade A Dependency Defined In On Of The ``.in`` Files
-------------------------------------------------------


.. code-block:: sh

   make upgrade-pip-requirement req=<python-package-name>
