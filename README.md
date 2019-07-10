# DART Viewer

DART Viewer is a cross-platform application for visualization of output netCDF files from Data Assimilation Research Testbed (DART).

## Introduction
The Data Assimilation Research Testbed (DART) is an open-source community software facility for ensemble data assimilation developed at the National Center for Atmospheric Research (NCAR). The DART distribution includes MATLAB diagnostic tools that examine the differences between observed values and predicted values from a model.

The output for these diagnostic tools are netCDF files containing ensemble values and relevant metadata. The cross-platform application DART Viewer is designed to help users quickly visualize those output files to understand their model performance and assimilation process.

## Features

- 2D and 3D scatter plot
- Subset the dataset with respect to geolocation
- Subset the dataset with respect to predefined groups
- Basic database query functionalities

*Note: DART Viewer only works with DART output netCDF files. To visualize other types of netCDF files, please use other tools like Panoply or IDV.*

## Installing
Download the binary installation file.
Since I do not own a Mac Development license, users might need to go to setting and trust to open the applications.

## Usage
Gifs of user flow

## Contributing

First, make sure you have the following installed:
- netCDF (ncdump, ncgen, nco). See website.
- Python 3 and pip

Then, follow the instructions below:
- Clone the project to your local directory
- Install all dependencies using
```
pip install -r requirements.txt
```
There you go, you have had a local isntallation of the netCDF-GUI tool on your local machine.
You can fire up the tool by running `fbs run`.

### Feedback
Please email me at ngojason9@gmail.com with any questions or suggestions.

## Acknowledgement
Author: Jason Ngo, Haverford College'21

Project: Implementing a Support System for Observation Files

Mentors: Jeffrey Anderson, Nancy Collins.
The DAReS team.
SIParCS | CISL | NCAR | UCAR

## License
DART software - Copyright UCAR. This open source software is provided by UCAR, "as is", without charge, subject to all terms of use at http://www.image.ucar.edu/DAReS/DART/DART_download