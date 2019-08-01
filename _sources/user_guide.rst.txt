################
User Guide
################

Hello there, this section contains all you need to know to start using DART
Viewer

Open File
=====================

When you open the GUI, you will be prompted to choose a netCDF file. Alternatively, you can choose to open the file by navigating  through the menubar ``File > Open..``.

Inspect File
=====================

Once you open the file, you will be greeted with the following interface:

.. figure:: images/GUI_interface.png
   :scale: 30%
   :alt: GUI interface

   DART Viewer User Interface

On the left you can see a box containing the header contents of the file. Users can therefore inspect quickly the dimensions, coordinates and variables of the file.

Look up Parent Groups
==========================

Below the header contents is the index look up box. Because in our implementation of netCDF file, each observation can be in multiple groups, you query for all the parents groups that an observation is in by inputting its index in the field.

Plot
=====================

Now, on the right hand side is the plotting panel. Users will first choose a variable that they want to plot from the list of variables in the file. Users will then choose to plot all the observations of that variable in which groups. Here, the root group represents the entire dataset.
Logic operators indicating whether I want to plot the intersection of these two groups, or the union of the two groups.

Once you click plot. a subset dialog will pop up, pre-filled with the min and max values of the lon/lat and time coordinates. Users can make changes to these prefilled values to inspect a specific region in space or time.

.. figure:: images/subset_dialog.png
   :scale: 100%
   :alt: DART Viewer Subset Dialog

   DART Viewer Subset Dialog

Below is the DART Quality Control selections. Each observation is assigned a DART quality control value, indicating whether that observation is assimilated, evaluated or rejected. There are 7 quality control in total. For now, let’s not make any changes and click “plot”. The default value for DART Quality Control Selection is All.

Right now, DART Viewer can generate three plots:
- 3D Scatter plot of point data
- Quality control time series
- Distribution of quality control values

*More customizable plots will be added in the future.*

Feedback
======================

Any feedback should be sent to dart@ucar.edu or ngojason9@gmail.com