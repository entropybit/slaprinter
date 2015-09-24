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

The more interesting script would be the manual_printing script which as the name suggest is used for actual printing. This script needs to run on the raspberry pi controlling the printer. To select from one of the several possible working modes of the manual_printing script an input device is needed. In our case this was a simple USB gamepad with a SNES controller layout.

![gamepad layout ]() 

## sla_client

## sla_printer


