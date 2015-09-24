# slaprinter

The *slaprinter* repository consist of thre sub projects from which two are softwares complementing each other and the third is essentially only a script for analytical purposes. After this short statement regarding what the repository actually contains, an introduction to our project seems to be in order.First of all, the repository you are looking at here contains the software developed for operating a sla 3D printer build by the TU Darmstadt iGEM Team for the 2015 contest. For a more complete information regarding the whole project visit the project [wiki](http://2015.igem.org/Team:TU_Darmstadt). Or to be a bit more specific the description of the printer can be found [here](http://2015.igem.org/Team:TU_Darmstadt/Project/Tech/Hardware). Now to go on with the actual introduction, the printer developed uses steroelithography (*SLA*) as additive manufacturing method. This means the composition of an physical object is reached by illumination a photo-reactive resin, so a fluid hardening under illumination with an according scope of wavelengths.

A simple method for printing any 3D object is to slice the 3D modell into layers and print the object layer after layer. The SLA technique in principle allows for thre dimensional printing using two-photon polymerization, however this requires a more complex hardware as well as software. 

In order to reduce complexity as well as cost we chose to use a simple projector, as commonly used in presentations, to handle the illumination process.
The interior of the slaprinter contains mainly of the beamer, a raspbery pi, a basin and a screw thread on which a stepper motor moves a metallic board holding the print up or down. So to print an arbitrary 3D model it needs to be cut into slices, each of which then will be projected onto the resin by the beamer, thus resulting in a according hardening.

A schematic of the printer together with the software is illustrated here:

![sla printer schematic ](http://2015.igem.org/wiki/images/7/74/TU_Darmstadt_tech_scheme_new.png) 

The raspberry pi within the printer is used to control the illumination as well as motor movement. To enable a simple acces to our printer the idea is that the slicing should be done with a client software communicating with the server software onboard the pi. The according pieces of software are the sla_client subproject as the client software and the sla_printer subproject as the server software running on the pi.
 
## scripts

The script folder contains some scripts produced for analysis of our 3D printer. Currently there are only two scripts contained, the measurement script and the manual_printing script. The measurement script is a simple analysis of printer step height distributions. Which were produced by measuring the height of single steps with a digital ruler.

The more interesting script would be the manual_printing script which as the name suggest is used for actual printing. This script needs to run on the raspberry pi controlling the printer. To select from one of the several possible working modes of the manual_printing script an input device is needed. In our case this was a simple USB gamepad with a SNES controller layout. The specific layout regarding the according functionality with the script is as illustrated here:

![gamepad layout ](https://raw.githubusercontent.com/entropybit/slaprinter/master/scripts/manual_printing/controller.png) 

So the arrow keys are used to move the stepper motor around. The shoulder keys can be used to move the board for holding the printed object to the lower or upper end of the printer,e.g., for moving the finished object out of the basin.

After starting the script it looks for folders within the subfolder slices, containing png files. 
Each such subfolder will be loaded as series of slices. With the **Y** button the actual slice in the actually selected slice series will be displayed for about 1s (enough time to see the picture on the bottom of the basin without causing significant hardening). With **B** one can iterate through the slices of the current slice series. And with the **A** button it is possible to go through the slice series which were generated according to the found subfolders of */slices* and there contained *.png* files. 
Upon pressing **X** a rectangle illustrating the displaying area will be shown on the display.

The functionality of the **select** key is to just show or hide a control picture / eich picture which can be used to examine how stuff will be displayed on the basin ground. Finally, with pressing **start** the printing procedure defined in the programm.dat will be started with the currently selected slice series.

## sla_client

The functionality of the client software is composed of visualization, slicing and communication with the printer. Currently only *.stl* files are supported, however there are several open source tools available which will produce *.stl* files from any given commonly used 3D file type. Therefore, this is not really a limitation, additionally support for othe types can of course be implemented. In fact this would be really easy, as it is only required to give a specification of how to read theses files. 
This is the case because the entire software layout follows the *Model-View-Controller* Pattern, although this is not completely fulfilled in the main Controller class, which is partly due to the useage of QT. 

In the following you can see a basic demonstration of how the client software works:

[![software demo video](http://img.youtube.com/vi/ugnCqa_hhho/0.jpg)](https://www.youtube.com/watch?v=ugnCqa_hhho)

## sla_printer


