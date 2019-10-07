# démo deux coroutines 
#    routine 1 : compter nombre d'appui bouton
#    routine 2 : clignoter autant de fois que d'appuis

import time
from machine import Pin
Cnt=0		

def thWait():
	deadline = time.ticks_ms()
	while True:
		while time.ticks_diff(deadline, time.ticks_ms()) > 0:
			yield True
		cnt=(yield False)
		deadline = time.ticks_add(time.ticks_ms(), cnt)
		
#----------------------------------------------------------------------------------------------
#------------------------------- templace, ne pas changer, à recopier uniquement
#----------------------------------------------------------------------------------------------
def tThread_template(): 
	waitms=thWait() # variable locale à la thread, en créer au moins une par thread pour permettre pause multi-tâche non bloquante
	next(waitms)		# indispensable pour la syntaxe x=(yield)
	while True:   #boucle main() infinie de la tâche
		while waitms.send(100):
			yield

	
#----------------------------------------------------------------------------------------------
def tBouton():
	global Cnt
	waitms=thWait()
	next(waitms)
	p22=Pin(22,Pin.IN, Pin.PULL_UP) 
	while True:
		while p22.value()==1:
			yield
		Cnt=Cnt+1
		while waitms.send(50): #anti rebond
			yield
		while p22.value()==0:
			yield
		while waitms.send(50): #anti rebond
			yield
	

#----------------------------------------------------------------------------------------------
def tClignot():
	global Cnt
	waitms=thWait()
	next(waitms)
	p2=Pin(2,Pin.OUT)
	p2.off()
	while True:
		while Cnt==0:
			yield
		Cnt=Cnt-1
		p2.on()
		while waitms.send(100):
			yield
		p2.off()
		while waitms.send(400):
			yield


Th1=tBouton()
Th2=tClignot()
while True:
	next(Th1)
	next(Th2)

