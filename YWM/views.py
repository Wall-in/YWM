# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager,AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext
import stripe, random, code, string, re

from django.contrib.redirects.models import Redirect
from locale import currency
from datetime import *
from django.db.transaction import commit

from YWM.models import *
from YWM.forms import *

from stripe.resource import Customer
from _ast import IsNot
from django.db.models.fields import Empty

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage

import json, os
from django.core.files import File
from calendar import month
from decimal import Decimal

stripe.api_key = "sk_test_PIF9aNPnjijSvto3uKp6YfW6"

def message_alerte (request):
    
    try :
        messages = request.session['messages']
        del request.session ['messages']
        return messages
    except :
        return False

def import_image (request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    if request.method == 'POST': 
        form = Formulaire_Import_Image(request.POST, request.FILES)
        if form.is_valid():
            image_import = form.cleaned_data['image'] 
            name = form.cleaned_data['name'] 
            
            
            image =Image(image = image_import, name = name)
            image.save()
            
            request.session['messages'] = "L'image a bien été importée! " 
    else :
        form = Formulaire_Import_Image()
    return render(request, 'YWM/admin/import_image.html', locals()) 

def home(request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    couleurs = Couleur.objects.all()
    categories = Categorie.objects.all()
    attribues = Attribue.objects.all()
    produits = Produit.objects.all()
    

        
    if request.method == 'POST': 
        categorie = request.POST.getlist('Categorie')
        couleur = request.POST.getlist('Couleur')
        attribue = request.POST.getlist('Attribue')
        prix = request.POST['prix']
        
        try : 
            position = prix.find(',')
            prix_inf = int(prix[:position])
            prix_sup = int(prix[(position+1):])
        
        except ValueError:
            prix_inf = 0
            prix_sup = 25000
    
        liste = {}
        liste_critere = {}
        liste_tampon = {}
        
        if categorie == []:
            for c in categories:
                categorie.append(c.nom)
        if couleur == []:
            for c in couleurs:
                couleur.append(c.nom)
            
        if attribue == []:
            for a in attribues:
                attribue.append(a.nom)
        
        
        i = 1
        
        for cat in categorie :
            test = Produit.objects.filter(categorie__nom = cat)
            for t in test:
                if not test in liste and t.prix < prix_sup and t.prix > prix_inf :
                    liste[t] = i
                    i = i+1
        
        i = 1
        
        for coul in couleur :
            test = Produit.objects.filter(couleurs__nom = coul)
            for t in test:
                if not test in liste_critere:
                    liste_critere[t] = i
                    i = i+1
         
        
        i = 1
        
        for l in liste:
            if l in liste_critere:
                liste_tampon[l] = i
                i = i +1
        
        liste = liste_tampon        
                
    
                
    
        liste_critere = {}
        liste_tampon = {}
        i = 1
        
        for at in attribue :
            test = Produit.objects.filter(attribues__nom = at)
            for t in test:
                if not test in liste_critere:
                    liste_critere[t] = i
                    i = i+1
       
        i = 1
        
        for l in liste:
            if l in liste_critere:
                liste_tampon[l] = i
                i = i +1
         
                
        liste = liste_tampon
        
        
        produits = liste
                       
    return render(request, 'YWM/index.html', locals()) 

def inscription(request):
    
    lien_source = False
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    try:
        lien_source = request.session['lien']
        del request.session['lien']
    except KeyError :
        pass
    
    if request.method == 'POST':  
        form = Formulaire_Inscription(request.POST)  

        if form.is_valid(): 
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user = Utilisateur.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
           
            user.save()
            request.session['messages'] = "Vous êtes bien inscrit."
            inscription_email (request, user)
            
            user = authenticate(username=username, password=password) 
            if user:  
                login(request, user)  
            
            if lien_source != False :
                return redirect("/"+lien_source)
            else :
                return redirect('home')

    else: 
        form = Formulaire_Inscription()  
    

    return render(request, 'YWM/user/inscription.html', locals())

def inscription_professionnel(request):
    
    lien_source = False
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    try:
        lien_source = request.session['lien']
        del request.session['lien']
    except KeyError :
        pass
    
    if request.method == 'POST':  
        form = Formulaire_Inscription_Professionnel(request.POST)  

        if form.is_valid(): 
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            nom_entreprise = form.cleaned_data['nom_entreprise']
            numero_siret = form.cleaned_data['numero_siret']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user = Utilisateur.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
            
            user.professionnel = True
            user.numero_siret = numero_siret
            user.nom_entreprise = nom_entreprise
           
            user.save()
            request.session['messages'] = "Vous êtes bien inscrit."
            inscription_email (request, user)
            
            user = authenticate(username=username, password=password) 
            if user:  
                login(request, user)  
            
            if lien_source != False :
                return redirect("/"+lien_source)
            else :
                return redirect('home')

    else: 
        form = Formulaire_Inscription_Professionnel()  
    

    return render(request, 'YWM/user/inscription_professionnel.html', locals())

def inscription_email (request, utilisateur):
    
    subject = "Mody | mobilier design - Confirmation d'inscription"
    to = [utilisateur.email]
    from_email = 'noreply@mody.com'

    image = Image.objects.get(name='logo')
    
    image_mail = open(image.image.path, "rb")
    msg_img = MIMEImage(image_mail.read())
    msg_img.add_header('Content-ID', '<logo>')
    
    ctx = {
        'utilisateur': utilisateur,
    }

    message = get_template('YWM/email/template_confirmation_compte.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.attach(msg_img)
    msg.send()

    return HttpResponse('inscription_email')


def connexion(request):
    
    error = False
    lien_source = False
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
     
    try:
        lien_source = request.session['lien']
        del request.session['lien']
    except KeyError :
        pass
    
    if request.method == "POST":
        form = Formulaire_Connexion(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)
            
            if user:  
                login(request, user)
                
                if lien_source != False and lien_source != "connexion":
                    return redirect("/"+lien_source)
                
                else:
                    request.session['messages'] = "Bienvenue " + user.first_name + "!"
                    return redirect(home)
                            
            else:
                error = True
            
    else:
        form = Formulaire_Connexion()
    

    return render(request, 'YWM/user/connexion.html', locals())


def deconnexion(request):
    boutique_vider_panier(request)
    logout(request)
    
    return redirect(reverse(connexion))


def mdp (request):
    
    if request.method == 'POST':  
        
        token = request.POST['token']
        
        if token == 'carnage':
            
            request.session['admin'] = True
            return redirect(admin_accueil)
    
    return render(request, 'YWM/admin/mdp.html', locals())

def acces_admin (request):
    
    test = False
    
    try :
        if request.session['admin'] == True:
            test = True
    
    except :
        pass
    
    return test  
  

def admin_accueil (request):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    produits = Produit.objects.all()
    utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
    
    if acces_admin(request) == False :
        return redirect(mdp)
    
    
    if request.method == "POST":
        date_avant = request.POST['date_avant']
        date_apres = request.POST['date_apres']
        
        try :
            date_avant = datetime.strptime(date_avant, '%Y-%m-%d')
            
        except ValueError : 
            date_avant = datetime.now()
            
            
        try :
            date_apres = datetime.strptime(date_apres, '%Y-%m-%d')
        
        except ValueError : 
            date_apres = datetime.now()
    
    else :
        
        date_avant = datetime.now() - timedelta(days=30)
        date_apres = datetime.now() 
    duree_graphique = []
    
    duree_axe_x_m = date_avant.month - 1
    duree_axe_x_d = date_avant.day + 1
    
    duree = date_apres - date_avant
    
    duree = duree.days

    i = 0
    
    while i < duree :
        
        element = date_apres- timedelta(days=i)
        test = element.strftime('%Y/%m/%d')
        duree_graphique.insert(0,test)
        i += 1
    
    commandes = Commande.objects.all().order_by('date')
    commandes_limitees = Commande.objects.all().order_by('-date')[:10]

    test_liste = []
    graphique = []
    taille = len(duree_graphique)
    i = 0
    total_commandes = 0
    
    while i < duree :
        date = duree_graphique[i]
        intermediaire = 0
        for commande in commandes:
            total_commandes = total_commandes + commande.total
            test = commande.date.strftime('%Y/%m/%d')
            test_liste.insert(0,test)
            if test == date :
                intermediaire = int(commande.total + intermediaire)
        graphique.append(intermediaire) 
        i += 1   

    return render(request, 'YWM/admin/accueil.html', locals())

def admin_produits (request):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    if acces_admin(request) == False :
        return redirect(mdp)
    
    produits = Produit
    produits = Produit.objects.all()

    return render (request, 'YWM/admin/produits.html', locals())

def admin_ajout_categorie(request):
    
    if request.method == 'POST':
        try :
                categorie_input = request.POST['categorie'] 
                categorie = Categorie(nom = categorie_input)
                categorie.save()
                request.session['messages'] = "La catégorie a bien été enregistrée" 
                
        except :
            pass
    
    return redirect(admin_ajout_produit)

def admin_ajout_attribue(request):
    
    if request.method == 'POST':
        try :
                attribue_input = request.POST['attribue'] 
                attribue = Attribue(nom = attribue_input)
                attribue.save()
                request.session['messages'] = "La caractéristique a bien été enregistrée" 
                
        except :
            pass
    
    return redirect(admin_ajout_produit)

def admin_ajout_couleur(request):
    
    if request.method == 'POST':
        try :
                couleur_input = request.POST['couleur'] 
                couleur = Couleur(nom = couleur_input)
                couleur.save()
                request.session['messages'] = "La couleur a bien été enregistrée" 
                
        except :
            pass
    
    return redirect(admin_ajout_produit)

def admin_ajout_produit (request):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    if acces_admin(request) == False :
        return redirect(mdp)
    produit = Produit

    if request.method == 'POST':
        form = Formulaire_Ajout_Produit(request.POST, request.FILES)  
        
        if form.is_valid(): 
            
            nom = form.cleaned_data['nom']
            prix = form.cleaned_data['prix']
            description = form.cleaned_data['description']
            
            infos = form.cleaned_data['infos']
            hauteur = form.cleaned_data['hauteur']
            largeur = form.cleaned_data['largeur']
            profondeur = form.cleaned_data['profondeur']
            volume = form.cleaned_data['volume']
            poids = form.cleaned_data['poids']
            photo1 = form.cleaned_data['photo1']
            photo2 = form.cleaned_data['photo2']
            photo3 = form.cleaned_data['photo3']
            stock = form.cleaned_data['stock']
            conditionnement = form.cleaned_data['conditionnement']
            
            categories = request.POST.getlist('categorie')
            couleurs = request.POST.getlist('couleurs')
            attribues = request.POST.getlist('attribues')
            
            
            ref = ""
    
            i = 0
            
            liste_char=string.ascii_letters+string.digits
            
            while i < 18:
                ref+=liste_char[random.randint(0,len(liste_char)-1)]
                i = i+1
                
            reference = "ref"+ref
            
            produit = Produit(nom=nom, prix=prix, description=description, \
                              infos=infos, hauteur=hauteur, largeur=largeur, profondeur=profondeur, volume=volume, poids=poids, photo1=photo1, \
                              photo2=photo2, photo3=photo3, stock=stock, conditionnement=conditionnement, \
                              reference= reference)
            
            produit.save()
            
            for categorie in categories:
                produit.categorie.add(categorie)
            
            for couleur in couleurs:
                produit.couleurs.add(couleur)   
            
            for attribue in attribues:
                produit.attribues.add(couleur) 
                
            
            try :
                test_produit = Produit
                test_produit = Produit.objects.get(reference=reference)
                
            except :
                pass
            
            if test_produit :
                request.session['messages'] = "Le produit à bien était ajouté!" 
                return redirect(reverse(admin_accueil))
            else : 
                request.session['messages'] = "Le produit n'a pas était enregistré!" 
                return redirect(reverse(admin_accueil))
            
    
    else :
        form = Formulaire_Ajout_Produit    

    return render(request, 'YWM/admin/ajout_produit.html', locals())

def admin_ajout_remise (request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    utilisateurs = Utilisateur.objects.all()
    
    if request.method == 'POST': 
        form = Formulaire_Remise(request.POST)
        
        if form.is_valid():
            
            users = request.POST.getlist('users')
            
            code = form.cleaned_data['code'] 
            quantite = form.cleaned_data['quantite']
            valeur = form.cleaned_data['valeur']
            pourcentage = form.cleaned_data['pourcentage']
            pour_pro = form.cleaned_data['pour_pro']
            pour_tous = form.cleaned_data['pour_tous']
           
            remise = Remise(code = code, quantite = quantite, valeur = valeur, pourcentage = pourcentage, pour_pro = pour_pro, pour_tous = pour_tous)
           
            remise.save()
            request.session['messages'] = "La réduction a été enregistrée!" 
            
            for user in users:
                useradd =Utilisateur.objects.get(username = user)
                remise.utilisateurs.add(useradd) 
           
    else :
        form = Formulaire_Remise()
        
        
    return render(request, 'YWM/admin/ajout_remise.html', locals()) 
    
def admin_remises (request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    codes = Remise.objects.all()
    
    return render(request, 'YWM/admin/remises.html', locals()) 

def admin_supprimer_remise (request, ref):
    
    ref = request.GET['ref']
    
    Remise.objects.get(id = ref).delete()
    
    
    return redirect(admin_remises)

def admin_modification_produit(request, ref):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    couleurs = Couleur.objects.all()
    categories = Categorie.objects.all()
    attribues = Attribue.objects.all()
    
    if acces_admin(request) == False :
        return redirect(mdp)
    
    try : 
        ref = request.GET['ref']
        request.session['ref'] = ref
        
    except KeyError :
        pass
    
    produit = Produit.objects.get(reference=ref)
    produit_couleurs = produit.couleurs.all()
    produit_categorie = produit.categorie.all()
    produit_attribues = produit.attribues.all()
    
    if request.method == 'POST':  # S'il s'agit d'une requete POST
           
        produit = Produit.objects.get(reference=ref)
        
        initiale = {'nom' : produit.nom, 'prix' : produit.prix, 'description' : produit.description, 'infos' : produit.infos, \
                    'hauteur' : produit.hauteur, 'largeur' : produit.largeur, 'profondeur' : produit.profondeur, 'volume': produit.volume, \
                    'poids' : produit.poids, 'stock' : produit.stock, 'conditionnement' : produit.conditionnement, 'photo1' : produit.photo1, \
                    'photo2' : produit.photo2, 'photo3' : produit.photo3, }
        
        form = Formulaire_Modification_Produit(request.POST, request.FILES, initial = initiale)
        
        if form.is_valid() :
            
            categorie = request.POST.getlist('Categorie')
            couleur = request.POST.getlist('Couleur')
            attribue = request.POST.getlist('Attribue')
            
            produit.nom = form.cleaned_data['nom']
            produit.prix = form.cleaned_data['prix']
            produit.description = form.cleaned_data['description']
            produit.infos = form.cleaned_data['infos']
            produit.hauteur = form.cleaned_data['hauteur']
            produit.largeur = form.cleaned_data['largeur']
            produit.profondeur = form.cleaned_data['profondeur']
            produit.volume = form.cleaned_data['volume']
            produit.poids = form.cleaned_data['poids']
            produit.photo1 = form.cleaned_data['photo1']
            produit.photo2 = form.cleaned_data['photo2']
            produit.photo3 = form.cleaned_data['photo3']
            produit.stock = form.cleaned_data['stock']
            produit.conditionnement = form.cleaned_data['conditionnement']

            
            produit.save()
            
            produit.couleurs.clear()
            produit.categorie.clear()
            produit.attribues.clear()
            
            for c in categorie:
                cat = Categorie.objects.get(nom= c)
                produit.categorie.add(cat)
            
            for c in couleur:
                cl = Couleur.objects.get(nom = c)
                produit.couleurs.add(cl)   
            
            for a in attribue:
                at = Attribue.objects.get(nom=a)
                produit.attribues.add(at) 
                
            return redirect(admin_produits )
          
    else :
         

        produit = Produit
        produit = Produit.objects.get(reference = ref)
        
        initiale = {'nom' : produit.nom, 'prix' : produit.prix, 'description' : produit.description, 'couleur' : produit.couleurs, 'infos' : produit.infos, \
                    'hauteur' : produit.hauteur, 'largeur' : produit.largeur, 'profondeur' : produit.profondeur, 'volume': produit.volume, \
                    'poids' : produit.poids, 'stock' : produit.stock, 'conditionnement' : produit.conditionnement, 'photo1' : produit.photo1, \
                    'photo2' : produit.photo2, 'photo3' : produit.photo3 }
        
        form = Formulaire_Modification_Produit(initial = initiale)
    
    return render (request, 'YWM/admin/modification_produit.html', locals())

def admin_traiter_cmd (request, ref):
    
    ref = request.GET['ref']
    
    produit = Produit
    produit = Commande.objects.get(numero=ref)
    
    if request.method == 'POST': 
 
        etat = request.POST.getlist('etat')
        
        for e in etat :
            produit.etat  = e
            produit.save()  
        
        return redirect(admin_commandes)
    

def admin_commandes (request):

    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    liste = ["Non Traitée", "Traitée", "Envoyée", "Reçue"]
    if acces_admin(request) == False :
        return redirect(mdp)
      
    if request.method == 'POST': 
        
        if request.POST['numero']:
            numero = request.POST['numero']
            etat = request.POST.getlist("etat_select")
            for e in etat :
                if e == "Tout" :
                    commandes = Commande.objects.filter(numero = numero).order_by('-date')
            
                else :
                    commandes = Commande.objects.filter(etat = e, numero = numero).order_by('-date')
                
        else :
            
            etat = request.POST.getlist("etat_select")
            for e in etat :
                if e == "Tout" :
                    commandes = Commande.objects.all().order_by('-date')
            
                else :
                    commandes = Commande.objects.filter(etat = e).order_by('-date')
            
    else :   
        commandes = Commande.objects.all().order_by('-date')

    

    return render (request, 'YWM/admin/commandes.html', locals())


def admin_utilisateurs (request):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    if request.method == 'POST': 
        if request.POST['username']:
            username=request.POST['username']
            try :
                utilisateurs = Utilisateur.objects.filter(username = username)
            
            except :
                utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
                pass
    
    else :
        utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
    
    return render (request, 'YWM/admin/utilisateurs.html', locals())

@login_required(login_url='connexion')
def user_compte_dashboard (request):
    
    identifiant_utilisateur = request.user.id
    utilisateur = Utilisateur.objects.get(id=identifiant_utilisateur)
 
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    commandes_utilisateur = Commande.objects.filter(client = utilisateur).order_by('-date')
    
    return render(request, 'YWM/user/compte/dashboard.html', locals())

@login_required(login_url='connexion')
def user_commandes(request):
    
    messages = message_alerte(request)
    identifiant_utilisateur = request.user.id
    utilisateur = Utilisateur.objects.get(id=identifiant_utilisateur)

    commandes_utilisateur = Commande.objects.filter(client = utilisateur).order_by('-date')
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    
    return render(request, 'YWM/user/compte/commandes.html', locals())

@login_required(login_url='connexion')
def user_changement_mdp (request):
    
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    error = False
    
    if request.method == 'POST':
        form = Formulaire_Change_MDP(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            
            if password1 != password2 :
                error = True
            
            else :
                request.user.set_password(password1)
                request.session['messages'] = "Votre nouveau mot de passe a bien été enregistré."
                return redirect(user_compte_dashboard)
    
    else :
        form = Formulaire_Change_MDP()
     
  
    return render(request, 'YWM/user/compte/changement_mdp.html', locals())

@login_required(login_url='connexion')
def user_changement_adresse (request):
    
    lien_source = False
    messages = message_alerte(request)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    
    try:
        lien_source = request.session['lien']
        del request.session['lien']
    except KeyError :
        pass

    if request.method == 'POST':
        form = Formulaire_adresse(request.POST)
        
        if form.is_valid():
            
            voie_livraison = form.cleaned_data['voie_livraison']
            ville_livraison = form.cleaned_data['lieu_livraison']
            code_livraison = form.cleaned_data['code_postal_livraison']
            pays_livraison = form.cleaned_data['pays_livraison']
            
            utilisateur = request.user
            utilisateur_donnee = Utilisateur.objects.get(id=utilisateur.id)
            
            utilisateur_donnee.voie_livraison = voie_livraison
            utilisateur_donnee.code_postal_livraison = code_livraison
            utilisateur_donnee.lieu_livraison = ville_livraison
            utilisateur_donnee.pays_livraison = pays_livraison
            
            utilisateur_donnee.save()
            request.session['messages'] = "Votre nouvelle adresse est bien enregistrée."
            
            if lien_source != False :
                return redirect("/"+lien_source)
            else:
                return redirect(user_compte_dashboard)
    
    else :
        form = Formulaire_adresse()

  
    return render(request, 'YWM/user/compte/changement_adresse.html', locals())

def boutique_mon_panier_contenu (request):
    
    try :
        remise = request.session['remise']
    
    except KeyError:
        remise = 0
        pass
        
    
    try:
        mon_panier = request.session['mon_panier']
        mes_quantites = request.session['mes_quantites']

    except KeyError:
        mon_panier = []
        pass
    
    
    elements = {}
    total = 0
    nombre = len(mon_panier)
    
    for ref in mon_panier :
        position = mon_panier.index(ref)
        produit = Produit.objects.get(reference=ref)
        elements[produit] = mes_quantites[position]
        
        total = total + produit.prix* int(mes_quantites[position])
    
    total = round(total - remise,2)
    
    return (elements, total, nombre, remise)


def boutique_accueil(request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    couleurs = Couleur.objects.all()
    categories = Categorie.objects.all()
    attribues = Attribue.objects.all()
    produits = Produit.objects.all()
    
        
    if request.method == 'POST': 
        categorie = request.POST.getlist('Categorie')
        couleur = request.POST.getlist('Couleur')
        attribue = request.POST.getlist('Attribue')
        prix = request.POST['prix']
        
        try : 
            position = prix.find(',')
            prix_inf = int(prix[:position])
            prix_sup = int(prix[(position+1):])
        
        except ValueError:
            prix_inf = 0
            prix_sup = 25000
    
        liste = {}
        liste_critere = {}
        liste_tampon = {}
        
        if categorie == []:
            for c in categories:
                categorie.append(c.nom)
        if couleur == []:
            for c in couleurs:
                couleur.append(c.nom)
            
        if attribue == []:
            for a in attribues:
                attribue.append(a.nom)
        
        
        i = 1
        
        for cat in categorie :
            test = Produit.objects.filter(categorie__nom = cat)
            for t in test:
                if not test in liste and t.prix < prix_sup and t.prix > prix_inf :
                    liste[t] = i
                    i = i+1
        
        i = 1
        
        for coul in couleur :
            test = Produit.objects.filter(couleurs__nom = coul)
            for t in test:
                if not test in liste_critere:
                    liste_critere[t] = i
                    i = i+1
         
        
        i = 1
        
        for l in liste:
            if l in liste_critere:
                liste_tampon[l] = i
                i = i +1
        
        liste = liste_tampon        
                
    
                
    
        liste_critere = {}
        liste_tampon = {}
        i = 1
        
        for at in attribue :
            test = Produit.objects.filter(attribues__nom = at)
            for t in test:
                if not test in liste_critere:
                    liste_critere[t] = i
                    i = i+1
       
        i = 1
        
        for l in liste:
            if l in liste_critere:
                liste_tampon[l] = i
                i = i +1
         
       
                
                
        liste = liste_tampon
        
        
        produits = liste

    return render(request, 'YWM/boutique/accueil.html', locals())

def boutique_page_produit(request, ref):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    ref = request.GET['ref']

    produit = Produit.objects.get(reference=ref)
    

    return render(request, 'YWM/boutique/page_produit.html', locals())

def boutique_ajout_produit(request, ref):
   
    ref = request.GET['ref']
    
    produit = Produit.objects.get(reference = ref)
    
    if request.method == 'POST': 
        
        quantite = request.POST['quantite'] 
    
        try:
            mon_panier = request.session['mon_panier']
            mes_quantites = request.session['mes_quantites']
             
            if ref in mon_panier:
                position = mon_panier.index(ref)
                mes_quantites[position]= mes_quantites[position] + int(quantite)
            else :
                mon_panier.append(ref)
                mes_quantites.append(int(quantite))
                
    
        except KeyError:
            mon_panier = []
            mes_quantites = []
    
            mon_panier.append(ref)
            mes_quantites.append(int(quantite))
            
            pass
    
        
        
    else :
    
        try:
            mon_panier = request.session['mon_panier']
            mes_quantites = request.session['mes_quantites']
             
            if ref in mon_panier:
                position = mon_panier.index(ref)
                mes_quantites[position]= mes_quantites[position] + 1
            else :
                mon_panier.append(ref)
                mes_quantites.append(1)
                
    
        except KeyError:
            mon_panier = []
            mes_quantites = []
    
            mon_panier.append(ref)
            mes_quantites.append(1)
            
            pass
    
    request.session['messages'] = 'Le produit : "'+ produit.nom +'" a bien été ajouté à votre panier.'
    request.session['mon_panier'] = mon_panier
    request.session['mes_quantites'] = mes_quantites
            
   
    return redirect(boutique_accueil)
    

def boutique_supprimer_produit(request, ref):
    
    ref = request.GET['ref']
    
    try:
        mon_panier = request.session['mon_panier']
        mes_quantites = request.session['mes_quantites']
        position = mon_panier.index(ref) 
        del mon_panier[position]
        del mes_quantites[position]

    except KeyError:
        mon_panier = []
        mes_quantites = []
        pass
     
    request.session['mon_panier'] = mon_panier
    request.session['mes_quantites'] = mes_quantites
    request.session['messages'] = "Le produit a été supprimé de votre panier!"
   
    return redirect(boutique_accueil)

def boutique_remise(request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    identifiant_utilisateur = request.user.id
    
    try :
        remise = request.session['remise']
        total = total + remise
        
    except KeyError :
        remise = 0
        pass
    
    if request.method == 'POST': 
        code = request.POST['code'] 
        
        remise_code = False
        
        try :
            remise_code = Remise.objects.get(code = code)
        
        except :
            pass
        
        
        if remise_code != False :                  
            if remise_code.pour_tous == True :
                if remise_code.valeur != 0 and remise_code.quantite > 0:
                    remise = remise_code.valeur
                    request.session['remise'] = remise
                    request.session['messages'] = "Votre code réduction a bien été pris en compte!"
                    remise_code.quantite = remise_code.quantite - 1
                    remise_code.save()
                    return redirect(boutique_panier)
                else :
                    if remise_code.quantite > 0 :
                        remise = round(total * (remise_code.pourcentage/100),2)
                        request.session['remise'] = remise
                        request.session['messages'] = "Votre code réduction a bien été pris en compte!"
                        remise_code.quantite = remise_code.quantite - 1
                        remise_code.save()
                        return redirect(boutique_panier)
            
            if remise_code.pour_tous == False :
                if identifiant_utilisateur != None :
                    utilisateur = Utilisateur.objects.get(id=identifiant_utilisateur)
                    if remise_code.pour_pro == True :
                        if utilisateur.professionnel == True :
                            if remise_code.valeur != 0 and remise_code.quantite > 0:
                                remise = remise_code.valeur
                                request.session['remise'] = remise
                                request.session['messages'] = "Votre code réduction réservé aux professionnels a bien été pris en compte!"
                                remise_code.quantite = remise_code.quantite - 1
                                remise_code.save()
                                return redirect(boutique_panier)
                            else :
                                if remise_code.quantite > 0 : 
                                    remise = round(total * (remise_code.pourcentage/100),2)
                                    request.session['remise'] = remise
                                    request.session['messages'] = "Votre code réduction réservé aux professionnels a bien été pris en compte!"
                                    remise_code.quantite = remise_code.quantite - 1
                                    remise_code.save()
                                    return redirect(boutique_panier)
                            
                    if utilisateur in remise_code.utilisateurs.all() :
                        if remise_code.valeur != 0 and remise_code.quantite > 0:
                            remise = remise_code.valeur
                            request.session['remise'] = remise
                            request.session['messages'] = "Votre code réduction a bien été pris en compte!"
                            remise_code.quantite = remise_code.quantite - 1
                            remise_code.save()
                            return redirect(boutique_panier)
                        else :
                            if remise_code.quantite > 0 : 
                                remise = round(total * (remise_code.pourcentage/100),2)
                                request.session['remise'] = remise
                                request.session['messages'] = "Votre code réduction a bien été pris en compte!"
                                remise_code.quantite = remise_code.quantite - 1
                                remise_code.save()
                                return redirect(boutique_panier)
                    else :
                        request.session['messages'] = "Vous n'etes pas autorisé à utiliser ce code."
                        return redirect(boutique_panier)
                
                else :
                    request.session['messages'] = "Vous devez être connecté à votre compte pour pouvoir utiliser ce code."
                    return redirect(boutique_panier)
                
    request.session['messages'] = "Aucun code de réduction reconnu."          
    return redirect(boutique_panier)

def boutique_panier(request):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    test = True
    
    for element in elements:
        if element.stock == 0 or elements[element] > element.stock:
            test = False
    
    return render(request, 'YWM/boutique/panier.html', locals())

def boutique_validation_commande(request):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    form1 = Formulaire_Connexion()
    form2 = Formulaire_Inscription()
    
    request.session['lien'] = "boutique/paiement/validation_commande"

    if request.user.id : 
        return redirect(reverse(boutique_confirmation_adresse))
    
    return render(request, 'YWM/boutique/paiement/validation_commande.html', locals())

@login_required(login_url='connexion')
def boutique_confirmation_adresse(request):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    identifiant_utilisateur = request.user.id
    client = Utilisateur.objects.get(id=identifiant_utilisateur)
    
    if request.method == 'POST':  
        form = Formulaire_Modification_Adresse(request.POST)  

        if form.is_valid(): 
            
            voie_livraison = form.cleaned_data['voie_livraison']
            ville_livraison = form.cleaned_data['lieu_livraison']
            code_livraison = form.cleaned_data['code_postal_livraison']
            pays_livraison = form.cleaned_data['pays_livraison']
            
            
            client.voie_livraison = voie_livraison
            client.code_postal_livraison = ville_livraison
            client.lieu_livraison = code_livraison
            client.pays_livraison = pays_livraison
            
            client.save()
            
            return redirect(boutique_paiement_saisie)

    else: 
        form = Formulaire_Modification_Adresse()

    return render(request, 'YWM/boutique/paiement/confirmation_adresse.html', locals())

def boutique_enregistrement_commande(request, numero):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)

    
    identifiant_utilisateur = request.user.id
    client = Utilisateur.objects.get(id=identifiant_utilisateur)
    
    date_commande = datetime.now()

    numero = numero
    
    commande = Commande(client = client, payee = False, total = total, remise= remise, email = client.email, voie_livraison = client.voie_livraison, \
                        lieu_livraison = client.lieu_livraison, code_postal_livraison = client.code_postal_livraison, pays_livraison = client.pays_livraison, \
                        numero = numero, etat = "Non Traitée", date = date_commande)
    commande.save()   
    
    
    for produit in elements :
        
        quantite = elements[produit]
        sous_total = produit.prix * int(quantite)
        
        produit_cmd = Produit_Cmd(commande = commande, produit = produit, quantite = quantite, prix = produit.prix, sous_total = sous_total)

        produit_cmd.save()
        

    return

def boutique_vider_panier (request):
    
    try :
        del request.session['mon_panier']
        del request.session['remise']
        del request.session['mes_quantites']
        
    except:
        pass
    
    return

def boutique_mise_a_jour_stock (request):
    
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    for element in elements:
        element.stock = element.stock - elements[element]
        element.save()
    
    return

def boutique_envoie_mail_client (request, numero, commande, utilisateur):
    
    subject = "Mody | mobilier design - Confirmation commande n°" + numero
    to = [utilisateur.email]
    from_email = 'noreply@mody.com'

    image = Image.objects.get(name='logo')
    
    image_mail = open(image.image.path, "rb")
    msg_img = MIMEImage(image_mail.read())
    msg_img.add_header('Content-ID', '<logo>')
    
    ctx = {
        'commande' : commande ,
        'client': utilisateur,
    }

    message = get_template('YWM/email/template.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.attach(msg_img)
    msg.send()

    return HttpResponse('boutique_envoie_mail_client')

def boutique_envoie_mail_admin (request, numero, commande, utilisateur):
    
    subject = "Mody | mobilier design - Confirmation commande n°" + numero
    to = ['maximiliengdeb@gmail.com']
    from_email = 'noreply@mody.com'

    image = Image.objects.get(name='logo')
    
    image_mail = open(image.image.path, "rb")
    msg_img = MIMEImage(image_mail.read())
    msg_img.add_header('Content-ID', '<logo>')
    
    ctx = {
        'commande' : commande ,
        'client': utilisateur,
    }

    message = get_template('YWM/email/template_admin.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.attach(msg_img)
    msg.send()

    return HttpResponse('boutique_envoie_mail_client')



@login_required(login_url='connexion')
def boutique_paiement(request):
    # Récupération des données primaire de l'utilisateur
    identifiant_utilisateur = request.user.id
    utilisateur = Utilisateur.objects.get(id=identifiant_utilisateur)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    token = request.POST['stripeToken']
    customer = False
    
    numero = request.session['numero']
        
           
    try:
        
        #recherche du customer
        customer = Customer.retrieve(utilisateur.username)

    
    except stripe.InvalidRequestError :
        pass


    if customer != False :
        id = customer.id
        
        try:
            charge = stripe.Charge.create(
            amount= int(total*100),
            currency="eur",
            customer = customer.id,
          )
            
            request.session['messages'] = "Votre commande à bien été passée."
            
            boutique_mise_a_jour_stock(request)
            boutique_enregistrement_commande(request, numero)
            boutique_vider_panier(request)
            commande = Commande.objects.get(numero = numero)
            boutique_envoie_mail_client(request, numero, commande, utilisateur)
            boutique_envoie_mail_admin(request, numero, commande, utilisateur)
            
            return redirect(boutique_paiement_confirmation)
      
        except stripe.error.CardError:
          # The card has been declined
          request.session['messages'] = "Une erreur est intervenue lors de votre commande, veuillez réessayer ou nous contacter, merci."
          return redirect(boutique_paiement_confirmation_erreur)
          pass
        
    else :
        
        try : 
            customer = stripe.Customer.create(
            source=token,
            id = utilisateur.username,
            email = utilisateur.email,  
            )
            
            stripe.Charge.create(
            amount=int(total*100),
            currency="eur",
            customer=customer.id,
            description = numero
            )
            
            request.session['messages'] = "Votre commande à bien été passée."
                
            boutique_mise_a_jour_stock(request)
            boutique_enregistrement_commande(request, numero)
            boutique_vider_panier(request)
            commande = Commande.objects.get(numero = numero)
            boutique_envoie_mail_client(request, numero, commande, utilisateur)
            boutique_envoie_mail_admin(request, numero, commande, utilisateur)
            
            return redirect(boutique_paiement_confirmation)
        
        except stripe.error.CardError:
          # The card has been declined
          request.session['messages'] = "Une erreur est intervenue lors de votre commande, veuillez réessayer ou nous contacter, merci."
          return redirect(boutique_paiement_confirmation_erreur)
          pass
    
    return 

@login_required(login_url='connexion')
def boutique_paiement_saisie (request):
    
    # Récupération des données primaire de l'utilisateur
    identifiant_utilisateur = request.user.id
    client = Utilisateur.objects.get(id=identifiant_utilisateur)
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    
    numero = ""
    
    i = 0
    
    liste_char=string.ascii_letters+string.digits
    
    while i < 15:
        numero+=liste_char[random.randint(0,len(liste_char)-1)]
        i = i+1
        
    request.session['numero'] = numero
    
    # Récupération des données primaire de l'utilisateur
    identifiant_utilisateur = request.user.id
    utilisateur = Utilisateur.objects.get(id=identifiant_utilisateur)
    
    total_affichage = total*100
   
    return render(request, 'YWM/boutique/paiement/paiement.html', locals())

@login_required(login_url='connexion')
def boutique_paiement_confirmation (request):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
    try :
        numero = request.session['numero']
        commande = Commande.objects.get(numero = numero)
        
    except :
        pass
    
    
   
    return render(request, 'YWM/boutique/paiement/confirmation.html', locals())

@login_required(login_url='connexion')
def boutique_paiement_confirmation_erreur (request):
    
    #Fonctions des bases
    elements, total, nombre, remise = boutique_mon_panier_contenu(request)
    messages = message_alerte(request)
    
   
    return render(request, 'YWM/boutique/paiement/erreur.html', locals())