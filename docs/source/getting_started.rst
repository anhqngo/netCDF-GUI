################
Getting Started
################

Motivation
************

The Data Assimilation Research Testbed (DART) is an open-source community
software facility for ensemble data assimilation developed at the National
Center for Atmospheric Research (NCAR). The DART distribution includes MATLAB
diagnostic tools that examine the differences between observed values and
predicted values from a model.

The output for these diagnostic tools are netCDF files containing ensemble
values and relevant metadata. The cross-platform DART Viewer application is
designed to help users quickly visualize those output files to understand their
model performance and assimilation process.

Features
*********

- 3D scatter plot
- Subset the dataset with respect to geolocation
- Subset the dataset with respect to predefined groups
- Logic operator support for combinations of the subset criteria
- Basic database query functionalities

Note: DART Viewer only works with DART output netCDF files. Sample test files can be found in the ``tests/datasets`` directory. To visualize other
types of netCDF files, please use other tools like `Panoply <https://www.giss.nasa.gov/tools/panoply/>`_ or `IDV <https://www.unidata.ucar.edu/software/idv/>`_.

Installation
************

Download the binary installation file `here <https://github.com/ngojason9/netCDF-GUI/releases/tag/v0.0.2>`_.