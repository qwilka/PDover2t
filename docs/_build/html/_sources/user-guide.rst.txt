User Guide
============


.. contents:: :local:

The Loadcase class
---------------------

The `Loadcase` class is the 


Creating Loadcase
---------------------

with Python code
^^^^^^^^^^^^^^^^

The following code imports the `Loadcase` class and creates a root (top-level) node:

.. code-block:: python

    from pdover2t import Loadcase
    rootnode = Loadcase("root-node")
    print(f"The name of the root node is «{rootnode.name}»")


