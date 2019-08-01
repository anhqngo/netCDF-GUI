################
Development
################

Hello fellow developers! This page will get you started on developing the graphical user interface.

*********************
Installation
*********************

Before getting a local copy of the repository on your machine, make sure that you have the following requirements:

- Python 3 (the GUI was built with Python 3.6) and pip
- `PROJ4 <https://proj.org/install.html?highlight=exe/>`_

Now, go ahead and clone the repository to your local machine::

    git clone https://github.com/ngojason9/netCDF-GUI
    cd netCDF-GUI

Here is the directory tree of the repository::

    ├── README.md
    ├── docs
    │   ├── ...
    │   └── source
    ├── requirements.txt
    ├── run.sh
    ├── src
    │   ├── build
    │   └── main
    │       ├── icons
    │       ├── python
    │       └── resources
    ├── tests
    │   ├── datasets
    │   └── jupyter_tests
    └── ui2py.sh

Now, let's install all dependencies::

    pip install -r requirements.txt

Once you have installed all dependencies, go ahead and type ``fbs run`` into the terminal; the GUI should pop up.

*************************
Modifying User Interface
*************************

The interface was built with Qt, a cross-platform software development framework. If you want to make changes to the interface, first install `Qt Designer <https://build-system.fman.io/qt-designer-download>`_.

Once you have installed Qt Designer, you can open the ``.ui`` files in ``src/main/resources/designer``. After you have made changes to the interface, run the bash script ``ui2py.sh`` to convert all the designer files to Python classes that can be imported to ``main.py``.

There are a lot of Qt Tutorials online, go check them out!

*************************
Modifying functionalities
*************************

In ``src/main/python``, you will see:

- ``main.py``, which includes all the logic for our GUI. As an alternative to the command ``fbs run``, you can also execute the file ``main.py`` in the terminal to start the GUI
- ``ui`` package, which includes Python scripts that renders the interface
- ``utils`` package, which incldues helper plotting functions, or I/O functions.

If you want to modify/add more functionalities, go ahead and find or add the relevant modules.

*************************
Modifying documentation
*************************

All the source files for documentation are in ``docs/source``. I used ``Sphinx`` to generate ``.html`` files from ``.rst`` files. 

All the HTML files are hosted on branch ``gh-pages`` separately from the source code ``master`` branch. Generate the HTML files with Sphinx, and then copy all the HTML files to that branch.

The documentation is included in the repository (on ``gh-pages`` branch) and online at https://jasonngo.net/netCDF-GUI

*********************
Testing framework
*********************

Currently, the GUI does not have any testing framework. I have looked at a few testing options such as ``selenium`` and ``pytest-qt`` but have not had time to implement those testing frameworks.

In the future, it is highly desired that there is a GUI testing framework in place.

********************
Modules and Packages
********************

.. toctree::

   modules/main
   modules/ui
   modules/utils
