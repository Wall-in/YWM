# -*- coding: utf-8 -*-

from django import forms
from YWM.models import Utilisateur, Produit, Image, Remise
from django.forms.widgets import Widget

class Formulaire_Inscription(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [ 'username', 'password',  'first_name', 'last_name']
        widgets = {
            'username' : forms.TextInput (attrs={'class': 'form-control', 'type' : 'email', 'placeholder': 'Adresse Mail'}),
            'password' : forms.TextInput (attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Mot de Passe'}),
            'first_name' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Nom'}),
        }
        
        labels ={
            'username' : (''),
            'password' : (''),
            'first_name' : (''),
            'last_name' : (''),
  
            }

class Formulaire_Inscription_Professionnel(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [ 'username', 'password',  'first_name', 'last_name','nom_entreprise', 'numero_siret']
        widgets = {
            'username' : forms.TextInput (attrs={'class': 'form-control', 'type' : 'email', 'placeholder': 'Adresse Mail'}),
            'password' : forms.TextInput (attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Mot de Passe'}),
            'first_name' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'nom_entreprise' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Nom Entreprise'}),
            'numero_siret' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Numéro SIRET'}),
        }
        
        labels ={
            'username' : (''),
            'password' : (''),
            'first_name' : (''),
            'last_name' : (''),
            'numero_siret' : (''),
            'nom_entreprise' : (''),
  
            }
        
        
class Formulaire_Import_Image (forms.ModelForm):
    class Meta:
        model = Image 
        fields = ['name', 'image']

class Formulaire_Remise (forms.ModelForm):
    class Meta:
        model = Remise 
        fields = ['code', 'quantite', 'valeur', 'pourcentage', 'pour_tous', 'pour_pro']
        widgets = {
            'code' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'quantite' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Quantite'}),
            'valeur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Valeur'}),
            'pourcentage' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Pourcentage'}),
        }
        

class Formulaire_Ajout_Produit (forms.ModelForm):
        class Meta:
            model = Produit
            fields = ['nom', 'prix', 'cout_achat', 'cout_estimation_livraison', 'description', 'infos', 'categorie' , 'couleurs', 'attribues', 'hauteur', 'largeur', 'profondeur', 'volume' , 'poids', 'photo1', 'photo2', 'photo3', 'stock', 'conditionnement']
            widgets = {
            'nom' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prix' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Prix'}),
            'cout_achat' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Coût achat du produit fournisseur'}),
            'cout_estimation_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Estimation Livraison'}),
            'description' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Description'}),
            
            'infos' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Infos'}),
            'hauteur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Hauteur'}),
            'largeur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Largeur'}),
            'profondeur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Profondeur'}),
            'volume' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Volume'}),
            'poids' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Poids'}),
            
            
            'stock' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Stock'}),

            'conditionnement' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Conditionnement'}),
            
        }
                    
class Formulaire_Modification_Produit(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        if not args: # args is empty, meaning a fresh object            
            super(Formulaire_Modification_Produit, self).__init__(*args, **kwargs)

        else:
            # Retrieving the form's information
            self.nom = args[0].get('nom')
            self.prix = args[0]['prix']
           

            super(Formulaire_Modification_Produit, self).__init__(*args, **kwargs)
    
    class Meta:
            model = Produit
            fields = [ 'nom', 'prix', 'cout_achat', 'cout_estimation_livraison', 'description', 'infos', 'hauteur', 'largeur', 'profondeur', 'volume' , 'poids', 'photo1', 'photo2', 'photo3', 'stock',  'conditionnement', ]
            widgets = {
            'nom' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            
            'prix' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Prix'}),
            'cout_achat' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Coût achat du produit fournisseur'}),
            'cout_estimation_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Estimation Livraison'}),
            
            'description' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'description' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Description'}),
            
            'infos' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Infos'}),
            'hauteur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Hauteur'}),
            'largeur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Largeur'}),
            'profondeur' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Profondeur'}),
            'volume' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Volume'}),
            'poids' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Poids'}),
            
            
            'stock' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Stock'}),

            'conditionnement' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Conditionnement'}),

        }
        
class Formulaire_Connexion(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Adresse Mail'}), required=True)
    password = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Mot de passe'}), required=True)
    
class Formulaire_Change_MDP(forms.Form):
    password = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Mot de passe'}), required=True)
    password2 = forms.CharField(label='',widget=forms.TextInput (attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Confirmation mot de passe'}), required=True)
    
class Formulaire_Change_Mail(forms.Form):
    mail = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control','type':'email', 'placeholder': 'Adresse Mail'}), required=True)
    mail2 = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control','type':'email', 'placeholder': "Confirmation de l'adresse Mail"}), required=True)

class Formulaire_adresse(forms.Form):
    voie_livraison = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Voie'}), required=True)
    lieu_livraison = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control',  'placeholder': 'Ville'}), required=True)
    code_postal_livraison = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Code Postal'}), required=True)
    pays_livraison = forms.CharField(label='', widget=forms.TextInput (attrs={'class': 'form-control',  'placeholder': 'Pays'}), required=True) 
    

class Formulaire_Modification_Adresse(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        if not args: # args is empty, meaning a fresh object            
            super(Formulaire_Modification_Adresse, self).__init__(*args, **kwargs)

        else:
            super(Formulaire_Modification_Adresse, self).__init__(*args, **kwargs)
    
    class Meta:
            model = Utilisateur
            fields = [ 'voie_livraison', 'lieu_livraison', 'code_postal_livraison', 'pays_livraison']
            widgets = {
            'voie_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Rue'}),
            'lieu_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'code_postal_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Code Postal'}),
            'pays_livraison' : forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Pays'}),
            
        }