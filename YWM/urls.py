from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views 

urlpatterns = [
    url(r'^superadmin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    
    url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^inscription_professionnel', views.inscription_professionnel, name='Inscription pour les professionnels'),
    url(r'^connexion', views.connexion, name='connexion'),
    url(r'^deconnexion', views.deconnexion, name='deconnexion'),
    
    url(r'^boutique/$', views.boutique_accueil, name='boutique'),
    url(r'^boutique/page_produit/(?P<ref>)$' , views.boutique_page_produit, name='Boutique Page Produit'),
    url(r'^boutique/ajout/(?P<ref>)$' , views.boutique_ajout_produit, name='Boutique Ajout Produit'),
    url(r'^boutique/supprimer/(?P<ref>)$' , views.boutique_supprimer_produit, name='Boutique Supprimer Produit'),
    url(r'^boutique/panier/$' , views.boutique_panier, name='Boutique Panier'),
    
    url(r'^boutique/paiement/validation_commande$' , views.boutique_validation_commande, name='Boutique Validation Commande'),
    url(r'^boutique/paiement/confirmation_adresse' , views.boutique_confirmation_adresse, name='Boutique Validation Adresse'),
    url(r'^boutique/paiement/paiement/' , views.boutique_paiement_saisie, name='Boutique Paiement'),
    url(r'^charge', views.boutique_paiement, name='Boutique Paiement'),
    url(r'^boutique/paiement/confirmation/' , views.boutique_paiement_confirmation, name='Boutique Paiement Confirmation'),
    url(r'^boutique/paiement/erreur/' , views.boutique_paiement_confirmation_erreur, name='Boutique Paiement Erreur'),
    url(r'^boutique/remise' , views.boutique_remise, name='Boutique Remise'),
    
    url(r'^admin/mdp', views.mdp, name='mdp'),
    url(r'^admin/$', views.admin_accueil, name='admin_accueil'),
    url(r'^admin/produits', views.admin_produits, name='Produits Admin'),
    url(r'^admin/ajoutproduit', views.admin_ajout_produit, name='Ajout Admin'),
    url(r'^admin/modificationproduit/(?P<ref>)$' , views.admin_modification_produit, name='Modification Produit Admin'),
    url(r'^admin/ajoutproduit$' , views.admin_ajout_produit, name='Ajout Produit Admin'),
    url(r'^admin/commandes' , views.admin_commandes, name='Commandes Admin'),
    url(r'^admin/traitementcmd/(?P<ref>)$' , views.admin_traiter_cmd, name='Traitement Admin'),
    url(r'^admin/utilisateurs' , views.admin_utilisateurs, name='Mes utilisateurs'),
    url(r'^admin/import_image' , views.import_image, name='Import Image'),
    url(r'^admin/ajout_remise' , views.admin_ajout_remise, name='Import Remise'),
    url(r'^admin/ajout_categorie' , views.admin_ajout_categorie, name='Import Categorie'),
    url(r'^admin/ajout_couleur' , views.admin_ajout_couleur, name='Import Couleur'),
    url(r'^admin/ajout_attribue' , views.admin_ajout_attribue, name='Import Attribue'),
    url(r'^admin/remises' , views.admin_remises, name='Remises'),
    url(r'^admin/remise_supprimer/(?P<ref>)$' , views.admin_supprimer_remise, name='Remises'),
    url(r'^admin/analyse_produit/(?P<ref>)$' , views.admin_produit_analyse, name='Analyse Produit'),
    
    url(r'^user/compte/commandes' , views.user_commandes, name='User Commandes'),
    url(r'^user/compte/dashboard' , views.user_compte_dashboard, name='User Dashboard'),
    url(r'^user/compte/changement_mdp' , views.user_changement_mdp, name='User Changement MDP'),
    url(r'^user/compte/changement_adresse' , views.user_changement_adresse, name='User Changement Adresse'),
    url(r'^user/ajoutfavori/(?P<ref>)$' , views.user_ajout_favori, name='User Ajout Favori'),
    url(r'^user/supprimerfavori/(?P<ref>)$' , views.user_supprimer_favori, name='User Ajout Favori'),
    url(r'^user/compte/favoris$' , views.user_favori, name='User Favoris'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
