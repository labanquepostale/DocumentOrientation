# Description du prototype

Le but de ce prototype est d'automatiser le redressement de documents scannés dans le bon sens. Lorsqu'un document est scanné, il est difficile de savoir si celui-ci sera dans le bon sens ou tourné de 90, 180 ou 270 degrés. L'objectif est donc ici de trouver une méthode pour détecter correctement cet angle de rotation, et retourner le scan en conséquence.

# Lancement du programme

python orientationDetectorOpenCV.py -i YOUR_INPUT_DIRECTORY -o YOUR_OUTPUT_DIRECTORY