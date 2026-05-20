Usage
=====

Installation
------------

Install project dependencies:

.. code-block:: bash

   python3 -m pip install -r requirements.txt

Command-line interface
----------------------

Run the application directly:

.. code-block:: bash

   python3 process_images.py --input-folder images --output-folder output

Or use the installed script:

.. code-block:: bash

   image-filters --input-folder images --output-folder output

Short options are available too:

.. code-block:: bash

   image-filters -i images -o output

Run targets
-----------

The project defines Poe the Poet targets in ``pyproject.toml``.

.. code-block:: bash

   poe help
   poe run
   poe test
   poe docs
