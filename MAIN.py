# DÉPENDANCES & DEFAULTS
import math #........................Fonctionnalités mathématiques
import numpy as np #.................Numpy pour travailler avec des tableaux
import plotly as py #................Importer Plotly 
import plotly.graph_objs as go #.....Importer des objets graphiques
import streamlit as st


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Introduction
############################################
############################################
###########################################################################################################
###########################################################################################################
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('EZZINE AYOUB - CIVIL ENGINEER')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [EZZINE AYOUB](https://www.linkedin.com/in/ayoub-ezzine/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Lauréat de l'école nationale des sciences appliquées d'Al-Hoceima, je mets ma curiosité et ma créativité au service du monde du génie civil pour améliorer mes compétences et enrichir mes expériences.")
    st.markdown("You can find the source code in the [EZZ-AY GitHub Repository](https://github.com/EZZINEAYOUB/MV)")
    st.markdown("If you are interested in how this app was developed contact me : +212 6 64 89 27 38")
st.markdown("")
st.markdown("")
st.markdown("")

###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ The sidebar
############################################
############################################
###########################################################################################################
###########################################################################################################

st.sidebar.markdown("**Veuillez entrer les données de départ :** 👇")
span = st.sidebar.number_input('la portée')
A = st.sidebar.number_input("Distance par rapport à l'appui gauche")
B = st.sidebar.number_input("Distance par rapport à l'appui droit")
E = st.sidebar.selectbox("Module de Young", (1000, 2000, 3000, 4000))
st.sidebar.subheader('Données de la section de la poutre')
a = st.sidebar.number_input("Entrez la valuer de la base (b)")
b = st.sidebar.number_input("Entrez la valuer de la hauteur(h)")
I= (a*(b**3)/12)
st.sidebar.write("Le moment d'inertie est:", I)
YN = st.sidebar.multiselect("Selectionnez le type des forces que vous avez",["Force concentrée","Charge uniformément répartie","Charge linéairement variée","Moment dans un point donné"])
        

###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ The center
############################################
############################################
###########################################################################################################
###########################################################################################################  
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1 : 
    st.subheader("Les données de départ")
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row2_1:
    Portee = "📏Portée = " + str(span) + " m"
    st.markdown(Portee)
with row2_2:
    Module_Young= "E=" + str(E) + " N/m^2"
    st.markdown(Module_Young)
with row2_3:
    Moment_Inertie = "I=" + str(round(I,4)) + " m^4)"
    st.markdown(Moment_Inertie)
st.markdown("")

row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    see_data = st.expander('Cliquer ici pour voir le schéma de référence 👉')
    with see_data:
        st.image('test1.png')
    
st.text('')


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Valeurs par défaut & Initisalisations
############################################
############################################
###########################################################################################################
###########################################################################################################
NB_PL = 0
NB_UDL = 0
NB_LDL = 0
NB_PM = 0
pointLoads = np.array([[0,0,0]]) #Forces concentrées [location, xMag, yMag]
pointMoments = np.array([[0,0]]) #Moments dans des points données [location, mag] (le sens des aiguilles est positif)
distributedLoads = np.array([[0,0,0]]) #Charges uniformément réparties [xStart, xEnd, yMag]
linearLoads = np.array([[0,0,0,0]]) #Charges réparties dont la magnitude varie linéairement [xStart, xEnd, startMag, endMag]
delta = 0.005 #la distance entre deux division
X = np.arange(0,span + delta,delta) #Plage des coordonnées x
nPL = len(pointLoads[0]) #Test pour les charges ponctuelles à prendre en compte
nPM = len(pointMoments[0]) #Test pour les charges uniformément réparties à considérer
nUDL = len(distributedLoads[0]) #Test pour les charges uniformément réparties à considérer
nLDL = len(linearLoads[0]) #Essai pour les charges de magnitude linéairement variable à considérer
#Initialiser les conteneurs de données
reactions = np.array([0.0,0,0]) #Reactions (Va, Ha, Vb) - Défini comme un tableau de floats
shearForce = np.empty([0,len(X)]) #Forces de cisaillement à chaque point de données
bendingMoment = np.empty([0,len(X)]) #Moment de flexion à chaque point de données
#ESTIMATION D'ENTRÉE POUR LA ROTATION INITIALE AU SUPPORT A ET LE PAS DE BALAYAGE 
deltaRot = 0.000005 #La taille du pas dans l'estimation de rotation
initRot = -0.0021 #Valeur initiale de la rotation au support A (VALEUR ASSUMÉE)

###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Les données de départs (Entrées)
############################################
############################################
###########################################################################################################
###########################################################################################################

row12_spacer1, row12_1, row12_spacer2 = st.columns((.2, 7.1, .2))
if "Force concentrée" in YN :
    with row12_1:
        st.subheader('Forces concentrées')
        st.markdown('Veuillez entrer les données qui concernent les forces concentrés')
        st.write(" ")
        #ajouter une image
        NB_PL = st.slider('Combien de forces concentrés', 1, 6, step=1)
        for i in range(0,NB_PL,1) :
             loc=st.number_input("L'emplacement de la Force N°{one}".format(one=i+1),min_value=1, step=1)
             xmag=st.number_input("L'amplitude horizontale de la Force N°{one} --- | (+) vers le haut & (-) vers le bas|".format(one=i+1))
             ymag=st.number_input("L'amplitude verticale de la Force N°{one} --- | (+) vers le haut & (-) vers le bas|".format(one=i+1))
             pointLoads = np.append(pointLoads,[np.array([loc, xmag, ymag])], axis=0)


if "Charge uniformément répartie" in YN :
    with row12_1:
        st.subheader('Charges uniformément réparties')
        st.markdown('Veuillez entrer les données qui concernent les Charges uniformément réparties')
        st.write(" ")
        #ajouter une image descriptive
        NB_UDL = st.slider('Combien de Charges réparties vous avez ?', 1, 6, step=1)
        for i in range(0,NB_UDL,1) :
             xStart=st.number_input("L'emplacement du début de la charge répartie N°{one}".format(one=i+1),min_value=1, step=1)
             xEnd=st.number_input("L'emplacement de la fin de la charge répartie N°{one}".format(one=i+1))
             yMag=st.number_input("L'amplitude verticale de la charge répartie N°{one} --- | (+) vers le haut & (-) vers le bas|".format(one=i+1))
             distributedLoads = np.append(distributedLoads,[np.array([xStart, xEnd, yMag])], axis=0)

if "Charge linéairement variée" in YN :
    with row12_1:
        st.subheader('Charges linéairement variées')
        st.markdown('Veuillez entrer les données qui concernent les Charges linéairement variées')
        st.write(" ")
        #ajouter une image descriptive
        NB_LDL = st.slider('Combien de Charges linéairement variées vous avez ?', 1, 6, step=1)
        for i in range(0,NB_LDL,1) :
             xStart=st.number_input("L'emplacement du début de la charge linéairement variée N°{one}".format(one=i+1),min_value=1, step=1)
             xEnd=st.number_input("L'emplacement de la fin de la charge linéairement variée N°{one}".format(one=i+1))
             startMag=st.number_input("L'amplitude verticale de début de la charge linéairement variée N°{one} --- | (+) vers le haut & (-) vers le bas|".format(one=i+1))
             endMag=st.number_input("L'amplitude verticale de la fin de la charge linéairement variée N°{one} --- | (+) vers le haut & (-) vers le bas|".format(one=i+1))
             linearLoads = np.append(linearLoads,[np.array([xStart, xEnd, startMag, endMag])], axis=0)

if "Moment dans un point donné" in YN :
    with row12_1:
        st.subheader('Moments')
        st.markdown('Veuillez entrer les données qui concernent le moment')
        st.write(" ")
        #ajouter une image descriptive
        NB_PM = st.slider('Combien de moments vous avez ?', 1, 6, step=1)
        for i in range(0,NB_PM,1) :
             location=st.number_input("L'emplacement du moment N°{one}".format(one=i+1),min_value=1, step=1)
             mag=st.number_input("La valeur du moment N°{one} --- | le sens des aiguilles est positif |".format(one=i+1))
             pointMoments = np.append(pointMoments,[np.array([location, mag])], axis=0)   


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Les fonctions principales & le calcul du projet
############################################
############################################
###########################################################################################################
###########################################################################################################
def reactions_PL(n):       
    xp = pointLoads[n,0] #Emplacement de la charge ponctuelle
    fx = pointLoads[n,1] #Magnitude de la composante horizontale de la charge ponctuelle 
    fy = pointLoads[n,2] #Magnitude de la composante verticale de la charge ponctuelle 
    
    la_p = A-xp  #Bras de levier de la charge ponctuelle autour du point A
    mp = fy*la_p #Moment généré par une charge ponctuelle autour de A
    la_vb = B-A  #Bras de levier de la réaction verticale en B autour du point A

    Vb = mp/la_vb #Réaction verticale à B
    Va = -fy-Vb   #Réaction verticale à A    
    Ha = -fx      #Réaction horizontale à A
    
    return Va, Vb, Ha    

def reactions_PM(n):       
    xm = pointMoments[n,0] #Emplacement du moment du point
    m = pointMoments[n,1]  #Magnitude du moment du point    
   
    la_vb = B-A #Bras de levier de la réaction verticale en B autour du point A

    Vb = m/la_vb #Réaction verticale à B
    Va = -Vb     #Réaction verticale à A    
    
    return Va, Vb

def reactions_UDL(n): 
    xStart = distributedLoads[n,0] #Emplacement du début des charges uniformément réparties (seront notées UDL)
    xEnd = distributedLoads[n,1]   #Emplacement de la fin des charges uniformément réparties (seront notées UDL)
    fy = distributedLoads[n,2]     #Amplitudes des UDL
    
    fy_Res = fy*(xEnd-xStart)          #Amplitudes de la résultante des UDL 
    x_Res = xStart + 0.5*(xEnd-xStart) #Emplacement de la résultante
    
    #COMME LA FONCTION DE CHARGE PONCTUELLE D'ICI 
    la_p = A-x_Res   #Bras de levier de la charge résultante autour du point A
    mp = fy_Res*la_p #Moment généré par la charge résultante autour de A
    la_vb = B-A      #Bras de levier de la réaction verticale en B autour du point A
    
    Vb = mp/la_vb   #Réaction verticale à B
    Va = -fy_Res-Vb #Réaction verticale à A
    
    return Va, Vb

def reactions_LDL(n): 
    xStart = linearLoads[n,0]   #Emplacement du début du LDL
    xEnd = linearLoads[n,1]     #Emplacement de l'extrémité du LDL
    fy_start = linearLoads[n,2] #Ampleur du LDL sur le côté gauche
    fy_end = linearLoads[n,3]   #Ampleur des LDL du côté droit
    
    #Déterminer l'emplacement et la magnitude de la résultante
    if abs(fy_start)>0:
        fy_Res = 0.5*fy_start*(xEnd-xStart)  #Ampleur de la résultante 
        x_Res = xStart + (1/3)*(xEnd-xStart) #Emplacement de la résultante
    else:
        fy_Res = 0.5*fy_end*(xEnd-xStart) 
        x_Res = xStart + (2/3)*(xEnd-xStart)
        
    
    #COMME LA FONCTION UDL D'ICI 
    la_p = A-x_Res   #Bras de levier de la charge résultante autour du point A
    mp = fy_Res*la_p #Moment généré par la charge résultante autour de A   
    la_vb = B-A      #Bras de levier de la réaction verticale en B autour du point A

    Vb = mp/la_vb   #Réaction verticale à B
    Va = -fy_Res-Vb #Réaction verticale à A    
    
    return Va, Vb

PL_record = np.empty([0,3])
if(nPL>0):
    for n, p in enumerate(pointLoads):
        va, vb, ha = reactions_PL(n) #Calculer les réactions
        PL_record = np.append(PL_record, [np.array([va, ha, vb])], axis=0) #Stocker les réactions pour chaque charge ponctuelle

        #Ajouter des réactions à l'enregistrement (principe de superposition)
        reactions[0] = reactions[0] + va 
        reactions[1] = reactions[1] + ha 
        reactions[2] = reactions[2] + vb 

PM_record = np.empty([0,2])
if(nPM>0):
    for n, p in enumerate(pointMoments):
        va, vb = reactions_PM(n) #Calculer les réactions
        PM_record = np.append(PM_record, [np.array([va, vb])], axis=0) #Stocker les réactions pour chaque moment

        #Ajouter des réactions à l'enregistrement (principe de superposition)
        reactions[0] = reactions[0] + va 
        reactions[2] = reactions[2] + vb         


UDL_record = np.empty([0,2])
if(nUDL>0):
    for n, p in enumerate(distributedLoads):
        va, vb = reactions_UDL(n) #Calculer les réactions
        UDL_record = np.append(UDL_record, [np.array([va, vb])], axis=0) #Stocker les réactions pour chaque charge répartie

        #Ajouter des réactions à l'enregistrement (principe de superposition)
        reactions[0] = reactions[0] + va 
        reactions[2] = reactions[2] + vb 


LDL_record = np.empty([0,2])
if(nLDL>0):
    for n, p in enumerate(linearLoads):
        va, vb = reactions_LDL(n) #Calculer les réactions
        LDL_record = np.append(LDL_record, [np.array([va, vb])], axis=0) #Store reactions for each linearly distributed load

        #Ajouter des réactions à l'enregistrement (principe de superposition)
        reactions[0] = reactions[0] + va 
        reactions[2] = reactions[2] + vb 


def shear_moment_PL(n):    
    xp = pointLoads[n,0] #Emplacement de la charge ponctuelle
    fy = pointLoads[n,2] #Magnitude de la composante verticale de la charge ponctuelle 
    Va = PL_record[n,0]  #Réaction verticale en A pour cette charge ponctuelle
    Vb = PL_record[n,2]  #Réaction verticale en B pour cette charge ponctuelle
    
    #Parcourez la structure et calculez l'effort tranchant et le moment de flexion en chaque point.
    Shear = np.zeros(len(X))  #Initialise un conteneur pour contenir toutes les données de force de cisaillement pour cette charge ponctuelle.
    Moment = np.zeros(len(X)) #Initialise un conteneur pour contenir toutes les données de moment et de force pour cette charge ponctuelle.
    for i, x in enumerate(X):    
        shear = 0  #Initialiser la force de cisaillement pour ce point de données
        moment = 0 #Initialiser le moment de flexion pour ce point de données

        if x>A:
            #Calculer le cisaillement et le moment à partir de la réaction en A
            shear = shear + Va
            moment = moment - Va*(x-A)

        if x>B:
            #Calculer le cisaillement et le moment à partir de la réaction en A
            shear = shear + Vb
            moment = moment - Vb*(x-B)

        if x>xp:
            #Calculer le cisaillement et le moment à partir d'une charge ponctuelle
            shear = shear + fy
            moment = moment - fy*(x-xp)

        #Stocker le cisaillement et le moment pour cet emplacement
        Shear[i] = shear
        Moment[i] = moment

    return Shear, Moment


def shear_moment_PM(n):    
    xm = pointMoments[n,0] #Emplacement du moment
    m = pointMoments[n,1]  #Magnitude du moment du point 
    Va = PM_record[n,0]    #Réaction verticale en A pour ce moment ponctuel
    Vb = PM_record[n,1]    #Réaction verticale en A pour ce moment ponctuel
    
    #Parcourez la structure et calculez l'effort tranchant et le moment de flexion en chaque point.
    Shear = np.zeros(len(X))  #Initialiser un conteneur pour contenir toutes les données de force de cisaillement pour ce moment de point
    Moment = np.zeros(len(X)) #Initialiser un conteneur pour contenir toutes les données de force de moment pour ce moment de point
    for i, x in enumerate(X):    
        shear = 0  #Initialiser la force de cisaillement pour ce point de données
        moment = 0 #Initialiser le moment de flexion pour ce point de données

        if x>A:
            #Calculer le cisaillement et le moment à partir de la réaction en A
            shear = shear + Va
            moment = moment - Va*(x-A)

        if x>B:
            #Calculer le cisaillement et le moment de la réaction à B
            shear = shear + Vb
            moment = moment - Vb*(x-B)

        if x>xm:
            #Calculer le moment dû au moment ponctuel (Pas d'influence sur le cisaillement)            
            moment = moment - m

        #Stocker le cisaillement et le moment pour cet emplacement
        Shear[i] = shear
        Moment[i] = moment

    return Shear, Moment


def shear_moment_UDL(n):    
    xStart = distributedLoads[n,0] #Emplacement du début de l'UDL
    xEnd = distributedLoads[n,1]   #Emplacement de la fin de l'UDL
    fy = distributedLoads[n,2]     #Ampleur de l'UDL
    Va = UDL_record[n,0] #Réaction verticale à A pour cette UDL
    Vb = UDL_record[n,1] #Réaction verticale à B pour cette UDL
    
    #Parcourez la structure et calculez l'effort tranchant et le moment de flexion en chaque point.
    Shear = np.zeros(len(X))  #Initialiser un conteneur pour contenir toutes les données de force de cisaillement pour cet UDL.
    Moment = np.zeros(len(X)) #Initialiser un conteneur pour contenir toutes les données de moment et de force pour cette UDL.
    for i, x in enumerate(X):    
        shear = 0  #Initialiser la force de cisaillement pour ce point de données
        moment = 0 #Initialiser le moment de flexion pour ce point de données
                
        if x>A:
            #Calculer le cisaillement et le moment à partir de la réaction en A
            shear = shear + Va
            moment = moment - Va*(x-A)

        if x>B:
            #Calculer le cisaillement et le moment de la réaction à B
            shear = shear + Vb
            moment = moment - Vb*(x-B)
        
        if x>xStart and x<=xEnd:
            #Coupe à travers l'UDL - calcule du cisaillement et le moment à partir de UDL
            shear = shear + fy*(x-xStart)
            moment = moment - fy*(x-xStart)*0.5*(x-xStart)
        elif x>xEnd:
            #Coupe à droite de l'UDL - calcule du cisaillement et le moment à partir de l'UDL
            shear = shear + fy*(xEnd-xStart)
            moment = moment - fy*(xEnd-xStart)*(x - xStart - 0.5*(xEnd-xStart))

        #Stocker le cisaillement et le moment pour cet emplacement
        Shear[i] = shear
        Moment[i] = moment    

    return Shear, Moment                

def shear_moment_LDL(n): 
    xStart = linearLoads[n,0]   #Emplacement du début du LDL
    xEnd = linearLoads[n,1]     #Emplacement de l'extrémité du LDL
    fy_start = linearLoads[n,2] #Magnitude du côté gauche du LDL
    fy_end = linearLoads[n,3]   #Magnitude du côté droit du LDL
    Va = LDL_record[n,0] #Réaction verticale en A pour ce LDL
    Vb = LDL_record[n,1] #Réaction verticale à B pour ce LDL
    
    #Parcourez la structure et calculez l'effort tranchant et le moment de flexion à chaque point.
    Shear = np.zeros(len(X))  #Initialiser un conteneur pour contenir toutes les données de force de cisaillement pour ce LDL.
    Moment = np.zeros(len(X)) #Initialiser un conteneur pour contenir toutes les données de force du moment pour cette LDL.
    for i, x in enumerate(X):    
        shear = 0  #Initialiser la force de cisaillement pour ce point de données
        moment = 0 #Initialiser le moment de flexion pour ce point de données
                
        if x>A:
            #Calculer le cisaillement et le moment à partir de la réaction en A
            shear = shear + Va
            moment = moment - Va*(x-A)

        if x>B:
            #Calculer le cisaillement et le moment de la réaction à B
            shear = shear + Vb
            moment = moment - Vb*(x-B)
        
        if x>xStart and x<=xEnd:
            #Coupe entre la LDL - calcule du cisaillement et le moment du LDL
            if abs(fy_start)>0:
                x_base = x-xStart #Base de la distribution triangulaire de la charge
                f_cut = fy_start - x_base*(fy_start/(xEnd-xStart)) #Magnitude du LDL à la coupure
                R1 = 0.5*x_base*(fy_start-f_cut) #Magnitude de la résultante pour la portion triangulaire de la charge
                R2 = x_base*f_cut #Magnitude de la résultante pour une portion constante de la charge 
                shear = shear + R1 + R2
                moment = moment - R1*(2/3)*x_base - R2*(x_base/2)
            else:
                x_base = x-xStart #Base de la distribution triangulaire de la charge
                f_cut = fy_end*(x_base/(xEnd-xStart)) #Magnitude du LDL à la coupure
                R = 0.5*x_base*f_cut #Ampleur de la résultante
                shear = shear + R
                moment = moment - R*(x_base/3)
                
        elif x>xEnd:
            #Coupe à droite du LDL - calculer le cisaillement et le moment à partir du LDL
            if abs(fy_start)>0:
                R = 0.5*fy_start*(xEnd-xStart)
                xr = xStart + (1/3)*(xEnd-xStart)                
                shear = shear + R
                moment = moment - R*(x-xr)
            else:
                R = 0.5*fy_end*(xEnd-xStart)
                xr = xStart + (2/3)*(xEnd-xStart)                
                shear = shear + R
                moment = moment - R*(x-xr)
                

        #Stocker les effets de cisaillement et de moment pour cet emplacement
        Shear[i] = shear
        Moment[i] = moment    

    return Shear, Moment   


#Calculer la force de cisaillement et le moment de flexion à chaque point de données en raison de la charge ponctuelle.
if(nPL>0):
    for n, p in enumerate(pointLoads):
        Shear, Moment = shear_moment_PL(n)
        shearForce = np.append(shearForce, [Shear], axis=0)        #Enregistrement de l'effort de cisaillement pour chaque charge ponctuelle
        bendingMoment = np.append(bendingMoment, [Moment], axis=0) #Stocker l'enregistrement du moment de flexion pour chaque charge ponctuelle


#Calculer la force de cisaillement et le moment de flexion à chaque point de données en raison du moment ponctuel.
if(nPM>0):
    for n, p in enumerate(pointMoments):
        Shear, Moment = shear_moment_PM(n)
        shearForce = np.append(shearForce, [Shear], axis=0)        #enregistrement de la force de cisaillement pour chaque moment ponctuel
        bendingMoment = np.append(bendingMoment, [Moment], axis=0) #Stocker l'enregistrement du moment de flexion pour chaque moment ponctuel


#Calculer la force de cisaillement et le moment de flexion à chaque point de données en raison de l'UDL.
if(nUDL>0):
    for n, p in enumerate(distributedLoads):
        Shear, Moment = shear_moment_UDL(n)
        shearForce = np.append(shearForce, [Shear], axis=0)        #Enregistrez l'effort de cisaillement pour chaque UDL.
        bendingMoment = np.append(bendingMoment, [Moment], axis=0) #Stocker l'enregistrement du moment de flexion pour chaque UDL


#Calculer la force de cisaillement et le moment de flexion à chaque point de données en raison du LDL.
if(nLDL>0):
    for n, p in enumerate(linearLoads):
        Shear, Moment = shear_moment_LDL(n)
        shearForce = np.append(shearForce, [Shear], axis=0) #Stocker l'enregistrement de la force de cisaillement pour chaque LDL
        bendingMoment = np.append(bendingMoment, [Moment], axis=0) #Stocker l'enregistrement du moment de flexion pour chaque LDL


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Configuration du diagramme de la force de cisaillement
############################################
############################################
###########################################################################################################
###########################################################################################################
#Définir l'objet de la mise en page
layout1 = go.Layout(
    title={
        'text': "Diagramme de la force de cisaillement",
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    titlefont=dict(size=15),
    yaxis = dict(
        title='Force de cisaillement (kN)'
    ),
    xaxis = dict(
        title='Distance (m)',       
        range=[-1, span+1]
    ),
    showlegend=False,        
)

#Définir la trace de la force de cisaillement
line1 = go.Scatter(
    x = X,
    y = sum(shearForce),
    mode='lines',
    name='Force de cisaillement',
    fill='tonexty',
    line_color='green',
    fillcolor='rgba(0, 255, 0, 0.1)'
)

#Définir une ligne horizontale pour représenter la structure
axis1 = go.Scatter(
    x = [0, span],
    y = [0,0],
    mode='lines',
    line_color='black'
)
###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Configuration du diagramme du Moment de flexion
############################################
############################################
###########################################################################################################
###########################################################################################################
#Définir l'objet de mise en page
layout2 = go.Layout(
    title={
        'text': "Diagramme du moment de flexion",
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    titlefont=dict(size=15),
    yaxis = dict(
        title='Moment de flexion (kNm)',
        autorange="reversed",   
    ),
    xaxis = dict(
        title='Distance (m)',       
        range=[-1, span+1]
    ),
    showlegend=False 
)

#Définir la trace du Moment de Flexion
line2 = go.Scatter(
    x = X,
    y = -sum(bendingMoment),
    mode='lines',
    name='Moment de flexion',
    fill='tonexty',
    line_color='red',
    fillcolor='rgba(255, 0, 0, 0.1)'
)

#Définir une ligne horizontale pour représenter la structure
axis2 = go.Scatter(
    x = [0, span],
    y = [0,0],
    mode='lines',
    line_color='black'
)

###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Généreration des figures
############################################
############################################
###########################################################################################################
###########################################################################################################

fig1 = go.Figure(data=[line1, axis1], layout=layout1)
fig2 = go.Figure(data=[line2, axis2], layout=layout2)

###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Affichage des résultats
############################################
############################################
###########################################################################################################
###########################################################################################################

with row12_1:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    if st.button('Démarrer les calculs'):
        with row12_1:
            st.subheader("Les résultats d'analyse")
            with row12_1:
                st.write('La réaction verticale en A est {one} kN'.format(one=round(reactions[0],2)))
                st.write('La réaction verticale en B est {one} kN'.format(one=round(reactions[2],2)))
                st.write('La réaction horizontale en A est {one} kN'.format(one=round(reactions[1],2)))
                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
    else:
        st.write('Merci de remplir les données de départ')


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Calcul de la flèche
############################################
############################################
###########################################################################################################
###########################################################################################################
#Constantes initiales
if span !=0 and a !=0 and b !=0 : 
    M = -sum(bendingMoment) #Valeurs du moment de flexion utilisées pour l'intégration
    delX = X[1]-X[0] #Distance entre les valeurs du moment de flexion
    EI=E*I
    initDef = 0 #Valeur initiale du déplacement à l'appui A
    supportIndexA = np.where(X == A)[0].item() #L'indice des valeurs au support A
    supportIndexB = np.where(X == B)[0].item() #L'indice des valeurs au support B
    def calcDeflection(M, EI, delX, theta_0, v_0):            
        #Réaffectation des arguments d'entrée aux variables utilisées dans la fonction
        theta_im1 = theta_0 #Rotation initiale
        v_im1 = v_0 #Déplacement initial
        #On désigne par im1 l'indice (i-1)[i moins 1]

        #Initialiser les conteneurs pour contenir la rotation et la flèche
        Rotation = np.zeros(len(X))
        Rotation[supportIndexA] = theta_im1
        Deflection = np.zeros(len(X))
        Deflection[supportIndexA] = v_im1

        #Boucler les données et les intégrer (règle du trapèze)
        for i, m in enumerate(M[supportIndexA::]):
            ind = i + supportIndexA #Tenir compte du fait que le support A peut ne pas se trouver au début de la poutre.
            if i>0:        
                M_im1 = M[ind-1]
                M_i = M[ind]        
                M_avg = 0.5*(M_i + M_im1)        

                theta_i = theta_im1 + (M_avg/EI)*delX #Intégrer les valeurs du moment pour obtenir les rotations                     
                v_i = v_im1 + 0.5*(theta_i+theta_im1)*delX #Intégrer les valeurs de rotation pour obtenir les déplacements

                #Stockage des données
                Rotation[ind] = theta_i        
                Deflection[ind] = v_i

                #Mise à jour des valeurs pour la prochaine itération de la boucle
                theta_im1 = theta_i     
                v_im1 = v_i
                
        return Rotation, Deflection

    def zeroCrossing(Deflection, guessStep, initRot, initDef):
        """
        Trouvez la valeur de la rotation initiale qui minimise la déviation au niveau du support droit en identifiant l'endroit où l'erreur passe par zéro.
        """
        
        
        #Si l'erreur de déviation est positive
        if Deflection[supportIndexB]>0:
            errorIsPositive = True 
            
            #Continuez à tester des valeurs de rotation initiales plus faibles jusqu'à ce que l'erreur devienne NÉGATIVE
            while errorIsPositive:
                initRot = initRot + guessStep
                Rotation, Deflection = calcDeflection(M, EI, delX, initRot, initDef)
                
                #Si l'erreur est devenue NÉGATIVE, changez la valeur logique pour permettre à la boucle de s'arrêter.
                if Deflection[supportIndexB]<0:
                    errorIsPositive = False
                    solvedInitRotation = initRot #Enregistrez la valeur "résolue" qui minimise l'erreur.
        
        #Sinon, si l'erreur de déviation est négative
        elif Deflection[supportIndexB]<0:
            errorIsPositive = False 
            
            #Continuez à tester des valeurs de rotation initiales plus faibles jusqu'à ce que l'erreur devienne POSITIVE.
            while not errorIsPositive:
                initRot = initRot + guessStep
                Rotation, Deflection = calcDeflection(M, EI, delX, initRot, initDef)
                
                #Si l'erreur est devenue POSITIVE, changez la valeur logique pour permettre à la boucle de s'arrêter.
                if Deflection[supportIndexB]>0:
                    errorIsPositive = True
                    solvedInitRotation = initRot #Enregistrez la valeur "résolue" qui minimise l'erreur.
        
        return solvedInitRotation   

    #Vérifier si la réduction ou l'augmentation de la rotation initiale entraîne une réduction de l'erreur de la flèche à l'autre support
    testDef = np.zeros(3)
    for i, r in enumerate([initRot-deltaRot, initRot, initRot+deltaRot]):
        Rotation, Deflection = calcDeflection(M, EI, delX, r, initDef)
        testDef[i] = Deflection[supportIndexB]
            
    if(abs(testDef[0])<abs(testDef[1])):
        #Nécessité de tester dans le sens de rotation négatif en réduisant l'estimation de la rotation initiale
        print('Besoin de tester dans la direction négative')    
        solvedInitRotation = zeroCrossing(Deflection, -deltaRot, initRot, initDef)            

    elif(abs(testDef[2])<abs(testDef[1])):
        #Nécessité de tester dans le sens de rotation positif en incrémentant la supposition de rotation initiale
        print('Besoin de tester dans la direction positive')    
        solvedInitRotation = zeroCrossing(Deflection, deltaRot, initRot, initDef)      

    #Exécutez le calcul de la flèche avec la valeur résolue de la rotation initiale.
    Rotation, Deflection = calcDeflection(M, EI, delX, solvedInitRotation, initDef)    

    if A!=0:
        print("Il y a une console sur le côté gauche - résoudre la déviation en intégrant dans le sens inverse.")
        
        theta_im1 = -solvedInitRotation #Rotation sur l'autre côté du support A
        v_im1 = 0 #flèche verticale au niveau du support A

        #Générer une série d'indices dans le sens inverse du support A à l'extrémité gauche de la poutre.
        reverseRange = np.arange(supportIndexA-1,-1,-1) 

        #Boucler les données et les intégrer (règle du trapèze) - DIRECTION INVERSE
        for i in reverseRange:                        
            M_im1 = M[i+1] #Attribuer la valeur précédente de M (sens inverse)
            M_i = M[i] #Attribuer la valeur actuelle de M (sens inverse)
            M_avg = 0.5*(M_i + M_im1)   
            
            theta_i = theta_im1 + (M_avg/EI)*delX #Intégrer les valeurs du moment pour obtenir les rotations                     
            v_i = v_im1 + 0.5*(theta_i+theta_im1)*delX #Intégrer les valeurs de rotation pour obtenir les déplacements
            
            #Stockage des données
            Rotation[i] = theta_i        
            Deflection[i] = v_i

            #Mise à jour des valeurs pour la prochaine itération de la boucle
            theta_im1 = theta_i     
            v_im1 = v_i                     


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Configuration du diagramme de la flèche
############################################
############################################
###########################################################################################################
###########################################################################################################
if span !=0 and a !=0 and b !=0 : 
    #Définir l'objet de mise en page
    layout3 = go.Layout(
        title={
            'text': "La flèche",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        yaxis = dict(
            title='La flèche'
        ),
        xaxis = dict(
            title='Distance (m)',       
            range=[-1, span+1]
        ),
        showlegend=False,        
    )

    #Définir la trace de la force de cisaillement
    line3 = go.Scatter(
        x = X,
        y = Deflection,
        mode='lines',
        name='Deflection',
        line_color='orange',
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.1)'
    )

    #Définir une ligne horizontale pour représenter la structure
    axis3 = go.Scatter(
        x = [0, span],
        y = [0,0],
        mode='lines',
        line_color='black'
    )

    #Générer et visualiser la figure
    fig3 = go.Figure(data=[line3,axis3], layout=layout3)


###########################################################################################################
###########################################################################################################
############################################
############################################
############################################ Affichage de diagramme de la flèche
############################################
############################################
###########################################################################################################
###########################################################################################################

if span!=0 and a!=0 and b!=0 :
    with row12_1:
        if st.button('calculer la flèche') :
                 with row12_1:
                        st.plotly_chart(fig3)
            
