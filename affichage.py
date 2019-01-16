# -*- coding: utf-8 -*-

#=========================================
#
#       o O  TP 9 : Billard   Oo
#
#==========================================
#
# Fichier : affichage.py
# Date : 2 décembre 12
# Auteurs : Eynard Julien/Karl Mongosso
# 
# Eynard Julien : squelette du code pour la gestion
# et l'affichage du billard
#
# Karl Mongosso : implémentation des fonctions du jeu
#
#===========================================


############# Quelques modules utiles #############

from boule import Boule,RAYON,LARGEUR,LONGUEUR
import pygame
from pygame.locals import *


############# Quelques fonctions utiles #############





def position_initiale():
	""" On récupère dans le fichier infos_boules.txt les positions initiales de chaque boules, et on crée toutes les boules sur ces positions """
	fichier = open('infos_boules.txt','r')
	ligne = fichier.readline()
	listBoule = []
	while ligne!="":
		ligne = ligne.split(',')
		position = (int(ligne[0]),int(ligne[1]))
		vitesse = (0,0)
		boule = Boule(position,vitesse,ligne[2].replace("\n",""))
		listBoule = listBoule + [boule]
		ligne = fichier.readline()
	
	return listBoule

def gestion_collisions(listeBoules):
	""" gestion des collisions de boules contenues dans la liste passée en paramètre, en utilisant la méthode collision de la classe Boule
	Paramètre :
		- listeBoules : liste des boules auxquelles on applique les méthodes de collision
	"""
	#attention, comme la méthode collision modifie la boule sur laquelle on appelle la méthode et la boule passée en paramètre, on n'appliquera pas plus d'une fois cette méthode sur les deux mêmes boules : ie si B1.collision(B2), alors on ne fera pas B2.collision(B1)
	for i in range(0,len(listeBoules)):
		for j in range(i,len(listeBoules)):
			if i!=j:
				listeBoules[i].collision(listeBoules[j])


def gestion_gagne(listeBoules):
	""" gestion des collisions de boules contenues dans la liste passée en paramètre, en utilisant la méthode collision de la classe Boule
	Paramètre :
		- listeBoules : liste des boules auxquelles on applique les méthodes de collision
	"""
	#attention, comme la méthode collision modifie la boule sur laquelle on appelle la méthode et la boule passée en paramètre, on n'appliquera pas plus d'une fois cette méthode sur les deux mêmes boules : ie si B1.collision(B2), alors on ne fera pas B2.collision(B1)
	temp = [boule for boule in listeBoules if ((boule.x>50 or boule.y>50) and (boule.x>50 or boule.y<730) and (boule.x<430 or boule.y>50) and (boule.x<430 or boule.y<730))]

	
				
	return temp
				


############# Création du billard, affichage graphique #############





# on initialise pygame
pygame.init()

# on crée une fenêtre que l'on stocke dans une variable nommée ecran. Les dimensions de la fenêtre sont celles stockées dans les variables LARGEUR et LONGUEUR (exprimées en pixels)
ecran = pygame.display.set_mode((500,800))

# on donne un joli titre à la fenêtre
pygame.display.set_caption("Jeu de Billard")

# on récupère le fond qui est l'image du billard avec ses bandes, que l'on met dans une variable nommée fond
fond = pygame.image.load('billard.png')

# création boule(s) 
#position = (0,0)
#vitesse = (0,0)
#position = (RAYON+9,RAYON+9)
#vitesse = (10,10)
#boule = Boule(position,vitesse,'boule_jaune.png')
#position = (500 - 2*RAYON - 24,RAYON+9)
#vitesse = (-10,-10)
#boule1 = Boule(position,vitesse,'boule_rouge.png')
listeBoules = position_initiale()
listeBoules[-1] = Boule((242,717),(0,0),'boule_blanche.png')
BB = listeBoules[-1]

# boucle de gestion des événements et d'affichage (dont on ne sort que si l'on ferme la fenêtre)
onContinue = True
horloge = pygame.time.Clock()
while onContinue:
	
	# Gestion des événements (on parcourt tous les événements, et si un évènement est de type QUIT, alors on ne continue plus)
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			onContinue = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# clic gauche pour tirer
			if event.button == 1:
				# on récupère la position de la souris
				posM = pygame.mouse.get_pos()	# posM est un tuple d'entier : coordonnées de la position de la souris au moment du clic
				
				# le nouveau vecteur vitesse de la boule blanche est le vecteur allant du centre de la boule à la position de la souris
				BB.vx = (posM[0]-BB.x)/2
				BB.vy = (posM[1]-BB.y)/2

				if(BB.vx>70):
					BB.vx=70
				if(BB.vy>70):
					BB.vy=70
			# clic droit pour redémarrer le jeu
			if event.button == 3:
				listeBoules = position_initiale()
				BB = listeBoules[-1]
	# on colle le fond dans la fenêtre
	ecran.blit(fond, (0,0))
	
	# calcul de la nouvelle vitesse, déplacement, vérification rebonds et collisions, et affichage graphique boule(s)
	for i in range(0,len(listeBoules)):
		listeBoules[i].deplace()
		listeBoules[i].rebond()
	
	gestion_collisions(listeBoules)

	listeBoules = gestion_gagne(listeBoules)
	
	for i in range(0,len(listeBoules)):
		listeBoules[i].calculeVitesse()
		listeBoules[i].affiche(ecran)



	#boule1.affiche(ecran)
	#boule.deplace()
	#boule1.deplace()
	#boule.rebond()
        #boule1.rebond()
	

	# on met à jour l'affichage
	pygame.display.flip()

	# on attend un petit peu, pour ne boucler que 25 fois maxi par seconde
	horloge.tick(25)

