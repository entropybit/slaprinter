# slaprinter

The *slaprinter* repository consist of thre sub projects from which two are softwares complementing each other and the third is essentially only a script for analytical purposes. After this short statement regarding what the repository actually contains, an introduction to our project seems to be in order.First of all, the repository you are looking at here contains the software developed for operating a sla 3D printer build by the TU Darmstadt iGEM Team for the 2015 contest. For a more complete information regarding the whole project visit the project [wiki](http://2015.igem.org/Team:TU_Darmstadt). Or to be a bit more specific the description of the printer can be found [here](http://2015.igem.org/Team:TU_Darmstadt/Project/Tech/Hardware). Now to go on with the actual introduction, the printer developed uses steroelithography (*SLA*) as additive manufacturing method. This means the composition of an physical object is reached by illumination a photo-reactive resin, so a fluid hardening under illumination with an according scope of wavelengths.

A simple method for printing any 3D object is to slice the 3D modell into layers and print the object layer after layer. The SLA technique in principle allows for thre dimensional printing using two-photon polymerization, however this requires a more complex hardware as well as software. 
To further reduce complexity and also cost instead of using laser systems the illumination in our 3D printer is simply handled by a projector as commonly used for presentations.
The interior of the slaprinter contains mainly of the beamer, a raspbery pi, a basin and a screw thread on which a stepper motor is moving a metallic board up or down.
So to print an arbitrary 3D model it needs to be cut into slices each of which then will be projected onto the resin by the beamer thus resulting in a according hardening.

A schematic of the printer together with the software is given aftewards

![sla printer schematic ](http://2015.igem.org/wiki/images/7/74/TU_Darmstadt_tech_scheme_new.png)


 

## sla_client

## sla_printer

## scripts
