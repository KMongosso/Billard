# -*- coding: utf-8 -*-

#=========================================
#
#       o O  TP 9 : Billard   Oo
#
#==========================================
#
# Fichier : classe.py
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

import pygame
from math import sqrt

############# Quelques constantes utiles #############

RAYON = 17	# rayon des boules, en pixel
DELTA_T = 0.35	# intervalle de temps entre deux rafraîchissement de la position
ACC = 7		# accélération subie par les boules en mouvement
EPSILON = 10	# constante en dessous de laquelle la vitesse devient nulle

# taille de la fenêtre d'affichage pour pyGame
LARGEUR = 500
LONGUEUR = 800

# largeur des bandes
BORD = 25


############# Classe Boule #############

class Boule:
	""" Classe qui définit une boule.
	Une boule sera définie par :
		- ses coordonnées (x, y)
		- sa vitesse (vx, vy)
		- une image pour une représentation graphique, dimensionnée suivant le rayon
	"""


	def __init__(self, position, vitesse, nomFichierImage):
		""" Constructeur d'une Boule.
		Paramètres :
			- position : tuple des coordonnées initiales du centre de la boule
			- vitesse : tuple des coordonnées du vecteur vitesse initial
			- nomFichierImage : nom du fichier de l'image utilisée pour l'afficher
		"""
		# coordonnées du centre de la boule
		self.x = position[0] 
		self.y = position[1]

		# coordonnées du vecteur vitesse
		self.vx = vitesse[0]
		self.vy = vitesse[1]

		# l'image de la boule
		self.image = pygame.image.load(nomFichierImage)		# ...			(chargement de l'image , transparence du fond, redimensionnement)
		self.image = pygame.transform.scale(self.image,(RAYON*2,RAYON*2))	



	def __str__(self):
		""" Renvoie une chaine de caractère décrivant la Boule (position et vitesse) """
		# ...
		s = "La boule a pour coordonnee (" + str(self.x) + "," + str(self.y) + ") et se deplace a une vitesse de (" + str(self.vx) + "," + str(self.vy) + ")"
		return s

	def affiche(self,ecran):
		""" Affiche une Boule sur l'écran.
		Paramètres :
			- ecran : l'écran sur lequel la Boule doit s'afficher
		"""
		# Attention, le vecteur position utilisé pour l'affichage est un translaté du vecteur position stocké en attribut
		s = ecran.blit(self.image, (self.x,self.y))
		return s

	def deplace(self):
		""" Déplace une Boule en fonction de sa vitesse. On utilise une intégration par rectangle (l'intervalle de temps considéré est DELTA_T, donné dans les constantes)
			"""
		x = self.x
		y = self.y
		self.x += self.vx*DELTA_T
		self.y += self.vy*DELTA_T
		self.vx = (self.x-x)/DELTA_T
		self.vy = (self.y-y)/DELTA_T

	def rebond(self):
		""" Permet de gérer le rebond des particules sur les bandes de la table """

		if self.x <= 25 or self.x >= 500 - 25 - RAYON*2:
			if self.x <= 25:
				self.x = 26
			else:
				self.x = 500 - 24 - RAYON*2
			self.vx = -self.vx

		if self.y <= 25 or self.y >= 800 - 25 - RAYON*2:
			if self.y <= 25:
				self.y = 26
			else:
				self.y = 800 - 24 - RAYON*2

			self.vy = -self.vy

	def dist(self,b):
		""" Calcule et renvoie la distance euclidienne entre la Boule et une autre Boule
		Paramètre:
			- b : l'autre Boule avec laquelle est calculée la distance
		Retour: la distance"""
		d = sqrt((b.x-self.x)**2+(b.y-self.y)**2)
		return d

	def collision(self,b):
		""" Gère la collision entre deux boules de même masse lors d'un choc élastique
		Paramètre :
			- b : l'autre boule avec laquelle la collision a lieu
		"""
		n = [0,0]
		g = [0,0]
		
		d = self.dist(b)
		
		if self.dist(b) <=  2*RAYON:

			#vecteur n normal au plan de collision
			n[0] = (b.x - self.x)/d
			n[1] = (b.y - self.y)/d  

			#normalisation de n
			g[0] = n[1]
			g[1] = -n[0]

			#rotation pi/2 sens direct du vecteur n par exemple pour le vecteur tangentiel normalisé g
			vngself = [n[0]*self.vx+n[1]*self.vy,g[0]*self.vx+g[1]*self.vy]
			vngb = [n[0]*b.vx+n[1]*b.vy,g[0]*b.vx+g[1]*b.vy]

			#si les boules se superposent, on les replace en position de contact strict (ici, le vecteur g est inutile)
			posngself = [n[0]*self.x+n[1]*self.y,g[0]*self.x+g[1]*self.y]
			posngb = [n[0]*b.x+n[1]*b.y,g[0]*b.x+g[1]*b.y]
			posngself[0]=posngself[0]-(RAYON*2-abs(posngself[0]-posngb[0]))/2
			posngb[0]= posngb[0]+(RAYON*2-abs(posngself[0]-posngb[0]))/2
			self.x = n[0]*posngself[0]+g[0]*posngself[1] 
			self.y = n[1]*posngself[0]+g[1]*posngself[1]
			b.x = n[0]*posngb[0]+g[0]*posngb[1]
			b.y = n[1]*posngb[0]+g[1]*posngb[1]
			
			#decomposition des vitesses sur la nouvelle base orthonormee (n,g)
			v1 = [vngb[0],vngself[1]]
			v2 = [vngself[0],vngb[1]]

			#echange des composantes normales ; les composantes tangentielles sont conservees
			
			self.vx = n[0]*v1[0]+g[0]*v1[1]
			self.vy = n[1]*v1[0]+g[1]*v1[1]
			b.vx = n[0]*v2[0]+g[0]*v2[1]
			b.vy = n[1]*v2[0]+g[1]*v2[1]

			if(self.vx>100):
					self.vx=100
			if(self.vy>100):
				self.vy=100


	def calculeVitesse(self):
		""" Calcule la vitesse en intégrant l'accélération ; le vecteur accélération a même direction et sens contraire à celui de la vitesse """
		v = sqrt((self.vx*ACC)**2+(self.vy*ACC)**2)

		#si vitesse trop petite, on stoppe la boule
		if v < EPSILON:
                        self.vx = 0
                        self.vy = 0
		#sinon, la vitesse diminue
		else:
			self.vx = self.vx-ACC*DELTA_T*self.vx/sqrt(self.vx**2+self.vy**2)
			self.vy = self.vy-ACC*DELTA_T*self.vy/sqrt(self.vx**2+self.vy**2)
