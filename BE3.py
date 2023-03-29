
from operator import itemgetter
import time
from PIL import Image # importation de la librairie d’image PILLOW
from math import sqrt, log10 # fonctions essentielles de la librairie math
im = Image.open("lyon.png") # ouverture du fichier d’image
px = im.load() # importation des pixels de l’image
W, H = im.size

## Exercice 1.1----------------------

def peindre(x,y,w,h,r,g,b):
    assert x + w <= W and y + h <= H, 'Erreur de dimensions'
    for i in range(w):
        for j in range(h):
            px[x+i, y+j]=(r,g,b)

## Exercice 1.2----------------------

def moyenne(x,y,w,h):
    R,G,B=0,0,0
    for i in range(w):
        for j in range(h):
            r,g,b=px[x+i, y+j]
            R+=r
            G+=g
            B+=b
    n=w*h
    return(R/n,G/n,B/n)

## Exercice 1.3----------------------

def ecart_type(x,y,w,h):
    mR,mG,mB=moyenne(x,y,w,h)
    R,G,B=0,0,0
    n=w*h
    for i in range(w):
        for j in range(h):
            r,g,b=px[x+i, y+j]
            R+=r**2
            G+=g**2
            B+=b**2
    return(sqrt(R/n-mR**2),sqrt(G/n-mG**2),sqrt(B/n-mB**2))
'''Les résultats obtenu sont légérement différents de ceux données`
par l'énoncé'''

## Exercice 1.4----------------------

def homogeniete(x,y,w,h,seuilh):
    return sum(ecart_type(x,y,w,h))/3 <= seuilh

## Exercice 1.5----------------------

def diviser(x,y,w,h):
    assert w>0 and h>0 and not w==h==1
    i = (w+1)//2
    j = (h+1)//2
    return (
		(x, y, i, j),
		(x+i, y, w-i, j) if w>1 else None,
		(x, y+j, i, h-j) if h>1 else None,
		(x+i, y+j, w-i, h-j) if w>1 and h>1 else None)
    
## Exercice 2.1----------------------

class Noeud:
    def __init__(self, x, y, l, h, r, v, b, hg, hd, bg, bd):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.r = r
        self.v = v
        self.b = b
        self.hg = hg # haut-gauche
        self.hd = hd # haut-droite
        self.bg = bg # bas-gauche
        self.bd = bd # bas-droite
    def get_N(self):
        target=self.bd.hg
        return (target.x,target.y,target.l,target.h,target.r,target.v,target.b)



    

racine = Noeud(0, 0, 4, 4, 128, 128, 128,
               Noeud(0, 0, 2, 2, 255, 255, 255, None, None, None, None),
               Noeud(2, 0, 2, 2, 128, 128, 128, 
                     Noeud(2,0,1,1,128,128,128,None,None,None,None),
                     Noeud(3,0,1,1,0,0,0,None,None,None,None),
                     Noeud(2,1,1,1,0,0,0,None,None,None,None),
                     Noeud(3,1,1,1,128,128,128,None,None,None,None)),
               Noeud(0,2,2,2,0,0,0,None,None,None,None),
               Noeud(2,2,2,2,128,128,128,
                     Noeud(2,2,1,1,255,255,255,None,None,None,None),
                     Noeud(3,2,1,1,255,255,255,None,None,None,None),
                     Noeud(2,3,1,1,128,128,128,None,None,None,None),
                     Noeud(3,3,1,1,128,128,128,None,None,None,None)))

## Exercice 2.2----------------------
p=0
def arbre(x,y,w,h,seuilh):
    global p
    r,g,b=moyenne(x,y,w,h)
    print('testh')
    if homogeniete2(x,y,w,h,seuilh) or p==99999999:
        return Noeud(x,y,w,h,r,g,b,None,None,None,None)
    else :
        p+=1
        print(p)
        hg,hd,bg,bd=diviser(x,y,w,h)
        return Noeud(x,y,w,h,r,g,b,arbre(*hg, seuilh) if hg!=None else None,
                     arbre(*hd, seuilh) if hd!=None else None,
                     arbre(*bg, seuilh) if bg!=None else None,
                     arbre(*bd, seuilh) if bd!=None else None)
    
## Exercice 2.3----------------------

def compter(Noeud):
    if Noeud == None :
        return 0
    return 1+compter(Noeud.hg)+compter(Noeud.hd)+compter(Noeud.bg)+compter(Noeud.bd)

## Exercice 2.4----------------------
        
def peindre_Noeud(Noeud):
    if Noeud == None :
        return
    if Noeud.hg==Noeud.hd==Noeud.bg==Noeud.bd==None :
        peindre(Noeud.x,Noeud.y,Noeud.l,Noeud.h,int(Noeud.r),int(Noeud.v),int(Noeud.b))
        return 
    peindre_Noeud(Noeud.hg)
    peindre_Noeud(Noeud.hd)
    peindre_Noeud(Noeud.bg)
    peindre_Noeud(Noeud.bd)

## Exercice 2.5----------------------

def peindre_profondeur(Noeud,p=0):
	if Noeud == None:
		return
	if Noeud.hg==Noeud.hd==Noeud.bg==Noeud.bd==None:
		n = W*H
		peindre(Noeud.x, Noeud.y, Noeud.l, Noeud.h, int(255*p//n), int(255*p//n), int(255*p//n))
	else:
		peindre_profondeur(Noeud.hg, p+1)
		peindre_profondeur(Noeud.hd, p+1)
		peindre_profondeur(Noeud.bg, p+1)
		peindre_profondeur(Noeud.bd, p+1)

## Exercice 2.6----------------------

def EQ(Noeud):
	if Noeud == None:
		return 0
	if Noeud.hg==Noeud.hd==Noeud.bg==Noeud.bd==None:
		eq = 0
		for i in range(Noeud.x, Noeud.x+Noeud.l):
			for j in range(Noeud.y, Noeud.y+Noeud.h):
				r, g, b = px[i, j]
				eq += (r-Noeud.r)**2 + (g-Noeud.v)**2 + (b-Noeud.b)**2
		return eq
	else:
		return EQ(Noeud.hg) + EQ(Noeud.hd) + EQ(Noeud.bg) + EQ(Noeud.bd)

def PSNR(Noeud):
	return 20 * log10(255) - 10 * log10(EQ(Noeud) / 3 / Noeud.l / Noeud.h)

## Exercice 3.2----------------------

class Noeud2:

	def __init__(self):
		self.valeurs = []

	def add_Noeud(self, x, y, l, h, r, v, b):
		self.valeurs.append((x, y, l, h, r, v, b)) 

	def get_pere(self,i):
		return self.valeurs[int((i-1)/4)]  

	def get_position(self,x, y, l, h, r, v, b):
		return self.valeurs.index((x,y,l,h,r,v,b))

	def get_fhg(self,i):
		return self.valeurs[(4*i)+1]        

	def get_fhd(self,i):
		return self.valeurs[(4*i)+2]

	def get_fbg(self,i):
		return self.valeurs[(4*i)+3]

	def get_fbd(self,i):
		return self.valeurs[(4*i)+4]

arbre1=Noeud2()
arbre1.add_Noeud(0, 0, 4, 4, 128, 128, 128)
arbre1.add_Noeud(0, 0, 2, 2, 255, 255, 255)
arbre1.add_Noeud(2,0,2,2,128,128,128)
arbre1.add_Noeud(0, 2, 2, 2, 0, 0, 0)
arbre1.add_Noeud(2,2,2,2,128,128,128)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(2,0,1,1,128,128,128)
arbre1.add_Noeud(3,0,1,1,0,0,0)
arbre1.add_Noeud(2,1,1,1,0,0,0)
arbre1.add_Noeud(3,1,1,1,128,128,128)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(None,None,None,None,None,None,None)
arbre1.add_Noeud(2,2,1,1,255,255,255)
arbre1.add_Noeud(3,2,1,1,255,255,255)
arbre1.add_Noeud(2,3,1,1,128,128,128)
arbre1.add_Noeud(3,3,1,1,128,128,128)

## Exercice 3.4----------------------

def EQ2(noeud):
      if noeud == None:
          return(0)
      elif noeud.hg==noeud.hd==noeud.bg==noeud.bd==None:
          eq = 0
          for i in range(noeud.x,noeud.x+noeud.l):
              for j in range(noeud.y,noeud.y+noeud.h):
                  r, g, b = px[i, j]
                  eq += (r-noeud.r)**2 + 1.5*(g-noeud.v)**2 + (b-noeud.b)**2 #double importance du vert
                  #erreur de la luminance
                  eq += 0.8*(((0.2126*noeud.r) + (0.7152*noeud.v) + (0.0722*noeud.b))-((0.2126*r) + (0.7152*g) + (0.0722*b)))**(2) 
                  #erreur du contrase 
                  eq+= 0.5*((noeud.r+noeud.v+noeud.b)/3-(r+g+b)/3)**(2)
                  
          return(eq)
      else:
          return(EQ(noeud.hg) + EQ(noeud.hd) + EQ(noeud.bg) + EQ(noeud.bd))
      
def PSNR2(Noeud):
    return(20*log10(255)-log10(EQ2(Noeud)/(3*W*H)))

def homogeniete2(x,y,w,h,seuilh):
    return( (sum(ecart_type(x,y,w,h))/3 <= seuilh) and (EQ2(Noeud(x,y,w,h,0,0,0,None,None,None,None))*10**(-5)<=seuilh) )




if __name__ == "__main__": 
    Arbre = arbre(0,0,W,H,20 )
    print(PSNR(Arbre))
    print(EQ(Arbre))
    peindre_Noeud(Arbre)
    im.show()
    im.save("lyon_compressé.png","PNG")