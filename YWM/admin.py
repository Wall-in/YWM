from django.contrib import admin
from YWM.models import Produit, Categorie, Couleur, Attribue, Commande, Produit_Cmd, Remise, Utilisateur

admin.site.register(Utilisateur)
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Couleur)
admin.site.register(Attribue)
admin.site.register(Commande)
admin.site.register(Produit_Cmd)
admin.site.register(Remise)