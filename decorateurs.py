from datetime import datetime # Nécessaire pour récupérer les dates auquels ont lieu les erreurs
from time import sleep # Nécessaire pour attendre entre 2 requêtes
import collections

import traceback

class Décorateurs():
	@staticmethod
	def exécuter_jusqu_à_accomplissement_ou_dépassement_du_nombre_d_essais_autorisés(
			fichier_log, nombre_d_essais, temps_d_attente_entre_2_essais = 5,
			enregistrement_des_premières_erreurs = False
		):
		"""
			Permet de d'éxecuter une requête jusqu'à ce qu'elle ne retourne plus d'erreur.

			Arguments:
				- fichier_log :		fichier de log utilisé pour enregistrer la liste des erreurs avec un horodatage
				- nombre_d_essais :	nombre de requêtes maximum à effectuer avant d'arrêter le programme
				- temps_d_attente_entre_2_essais : temps d'attente en secondes entre 2 essais consécutifs (valeur par défaut: 5)
				- enregistrement_des_premières_erreurs : paramètre permettant de signaler si l'on souhaite enregister
				les codes d'erreurs correspondant aux requêtes qui ont échouées. Sachant que si la dernière requête
				autorisée échoue le code d'erreur sera enregister dans le fichier log. (valeur par défaut: False)


		"""
		def decorateur(requête):
			def wrapper(*args, **kwargs):

				resultat = None
				compteur_essai = 0
				while (resultat is None) and  (compteur_essai < nombre_d_essais):

					try:
						resultat = requête(*args, **kwargs)

					except Exception as e:
						compteur_essai += 1
						if enregistrement_des_premières_erreurs or compteur_essai == nombre_d_essais:

							# On génère le message d'erreur horodaté

							data = '\n\n\n ---- \n\n'
							data += f'{datetime.now()}\n'
							data += f'Essai: {compteur_essai}\n'
							data += str(traceback.format_exc())

							# On enregistre le message d'erreur horodaté dans le fichier de log
							with open(fichier_log, 'a') as fichier:
								fichier.write(data)

						if compteur_essai == nombre_d_essais:
							raise e

						if isinstance(temps_d_attente_entre_2_essais, collections.abc.Iterable):
							it = iter(temps_d_attente_entre_2_essais)
							dt = next(it)
						else:
							dt = temps_d_attente_entre_2_essais
						sleep(dt)

				return resultat
			return wrapper
		return decorateur
