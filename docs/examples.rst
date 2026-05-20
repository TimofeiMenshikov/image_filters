Input And Output Examples
=========================

Successful processing
---------------------

Input folder:

.. code-block:: text

   images/
   ├── portrait.jpg
   ├── landscape.png
   └── notes.txt

Command:

.. code-block:: bash

   image-filters -i images -o output

Console output:

.. code-block:: text

   Processing: landscape.png
   Saved: /project/output/landscape_blur.png
   Saved: /project/output/landscape_sharpen.png
   Processing: portrait.jpg
   Saved: /project/output/portrait_blur.jpg
   Saved: /project/output/portrait_sharpen.jpg

Output folder:

.. code-block:: text

   output/
   ├── landscape_blur.png
   ├── landscape_sharpen.png
   ├── portrait_blur.jpg
   └── portrait_sharpen.jpg

Empty input folder
------------------

Input folder:

.. code-block:: text

   images/
   └── notes.txt

Command:

.. code-block:: bash

   image-filters --input-folder images

Console output:

.. code-block:: text

   No supported images found in /project/images
