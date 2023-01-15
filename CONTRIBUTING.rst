Developer, welcome!
===================

Contributing to ``duplicates`` has never been so easy:

- clone this repository
- if you don't know how to start take a look at the `Dev env`_ section
- the `testing suite <Testing_>`_ (coming soon) ensures compatibility for you
- create a `pull request <Pull Requests_>`_
- no idea? Feel free to pick an item from the `TODO list`_!


Philosophy
----------

A clean code should:

-  be readable and concise
-  prefer clarity over comments
-  be reusable
-  have short functions focusing each on a single task
-  use composition over inheritance
-  use immutable objects where possible
-  have a layered architecture
-  avoid premature optimization
-  be thread-safe


Pull Requests
-------------

Please consider the following before creating a pull-request:

- follow the coding conventions; applying ``black --check`` on the new code is
  usually enough
- create standalone, minimal commits with an explicit message; take a look at
  existing commits to get an idea of how to write your commit message
- merge against the ``develop`` branch


Dev env
-------

tldr;
^^^^^

.. code-block:: bash

    pipx install -e .

Even if not mandatory, I strongly recommend to insulate your development
environment into a ``virtualenv``. It will ensure that **all and only** the
needed requirements will be available to your program (no more *works for me*), 
and prevent incompatibility issues between multiple versions of other Python
packages.

I personnally use ``virtualenv`` and ``virtualenvwrapper`` to ease my venv 
management. One can also use ``pipx``, though I don't know how it will be able
to manage the dependencies declared in the ``requirements.txt`` file in the
future.

install
^^^^^^^

If you want to give ``virtualenvwrapper`` a chance, here is how I used to set it
up:

.. code-block:: bash

    pip install -U pip virtualenv virtualenvwrapper

Then add to your ``.bashrc`` file::

    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source $HOME/.local/bin/virtualenvwrapper.sh

usage
^^^^^

To set up your dev env (first time only):

.. code-block:: bash

    # git clone this repository
    # cd into your working copy
    mkvirtualenv duplicates
    pip install -r dev-requirements.txt

To exit the virtual environment:

.. code-block:: bash

    deactivate duplicates

To get the dev env back:

.. code-block:: bash

    workon duplicates

To remove the dev env:

.. code-block:: bash

    rmvirtualenv duplicates

You can check the state of your dev env any time with:

.. code-block:: bash

    pip list


Testing
-------

.. code-block:: bash

    python3 duplicates/duplicates.py 2>&1 | tee dup.log


Bugs
----

``duplicates`` is at its early stages of development.
Even if it is inteded to be a read-only program, backup your data before
testing against real-life data or change ``duplicates`` behavior.


License
-------

By contributing to ``duplicates``, you agree that your contributions will be
licensed under the terms given in the `LICENSE file`_.


Miscellaneous
-------------

Recommended listening while developing: `alt-J - An Awesome Wave`_


.. _LICENSE file: ./LICENSE
.. _TODO list: ./TODO.rst
.. _alt-J - An Awesome Wave: https://en.wikipedia.org/wiki/An_Awesome_Wave
