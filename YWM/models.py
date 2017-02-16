# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import default

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image')

class Utilisateur(User):
    
    #Adresse Livraison
    
    voie_livraison = models.CharField(max_length=250, default='Renseignez votre adresse')
    code_postal_livraison = models.CharField(max_length=250, default='Renseignez votre code postal')
    lieu_livraison = models.CharField(max_length = 250, default='Renseignez votre ville')
    pays_livraison = models.CharField (max_length=250, default='Renseigner votre pays')
    
    #Adresse Facturation
    
    voie_facturation = models.CharField(max_length=250, default='Non renseigné')
    code_postal_facturation = models.CharField(max_length=250, default='Non renseigné')
    lieu_facturation = models.CharField(max_length = 250, default='Non renseigné')
    pays_facturation = models.CharField (max_length=250, default='Non renseigné')
    
    #Professionnel 
    
    professionnel = models.BooleanField(default=False)
    nom_entreprise = models.CharField(max_length=250, null="Nom de l'entreprise")
    numero_siret = models.CharField(max_length=250, null='Numero Siret')
    

    
class Attribue(models.Model):
    nom = models.CharField(max_length=60)
    def __str__(self):
        return self.nom
    
class Categorie(models.Model):
    nom = models.CharField(max_length=60)
    def __str__(self):
        return self.nom
    
class Couleur(models.Model):
    nom = models.CharField(max_length=60)
    def __str__(self):
        return self.nom

class Remise (models.Model):
    code = models.CharField(max_length=60)
    quantite = models.IntegerField(default=0)
    pourcentage = models.IntegerField(default=0)
    valeur = models.IntegerField(default=0)
    
    pour_tous = models.BooleanField(default = True)
    pour_pro = models.BooleanField(default = False)
    utilisateurs = models.ManyToManyField(Utilisateur, null = True)
    
    
    def __str__(self):
        return self.code

    
class Produit(models.Model):
    reference = models.CharField(max_length=60)
    attribues = models.ManyToManyField(Attribue)
    categorie = models.ManyToManyField(Categorie)
    couleurs = models.ManyToManyField(Couleur)

    nom = models.CharField(max_length=60)
    prix = models.FloatField(verbose_name="Prix unitaire en € comprenant les frais de livraison")
        
    description = models.TextField(max_length=1000, blank=True)
    
    infos = models.CharField(verbose_name="Information courte", max_length=100, default=" ")
    hauteur = models.FloatField(verbose_name="Hauteur en cm", default = 0)
    largeur = models.FloatField(verbose_name="Largeur en cm", default = 0)
    profondeur = models.FloatField(verbose_name="Profondeur en cm", default = 0)
    
    volume = models.FloatField(verbose_name="Volume en cm3", default = 0)
    poids = models.FloatField(verbose_name="Poids en kg", default = 0)
    
    photo1 = models.ImageField(upload_to = "image/produit")
    photo2 = models.ImageField(upload_to = "image/produit")
    photo3 = models.ImageField(upload_to = "image/produit")

    stock = models.PositiveIntegerField(verbose_name="Stock", default = 1)
    
    conditionnement = models.TextField(max_length=1000, blank=True)

    
    def __str__(self):
        return self.nom
    
    
class Commande(models.Model):
    
    numero = models.CharField(max_length=250)
    client = models.ForeignKey('Utilisateur' ,related_name="relationutilisateur")
    
    email = models.CharField(max_length=250, default='Email')
    
    payee = models.BooleanField(default=False)

    etat = models.CharField(max_length=250)
    
    total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total en €")
    remise = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Remise en €")
    
    
    voie_livraison = models.CharField(max_length=250, default='Renseignez votre adresse')
    code_postal_livraison = models.CharField(max_length=250, default='Renseignez votre code postal')
    lieu_livraison = models.CharField(max_length = 250, default='Renseignez votre ville')
    pays_livraison = models.CharField (max_length=250, default='Renseigner votre pays')
    
    date = models.DateTimeField()
    
    def __str__(self):
        return self.numero


class Produit_Cmd(models.Model):
    
    commande = models.ForeignKey('Commande' ,related_name="relationcommande")
    
    produit = models.ForeignKey (Produit)
    
    quantite = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total en €")
    
    sous_total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total en €")
    
    