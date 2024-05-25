from maya import cmds, OpenMaya
import maya.mel as mm
def getpos(object2):       
    values=cmds.exactWorldBoundingBox(object2)
    maxX=values[3]
    minX=values[0]
    maxY=values[4]
    minY=values[1]
    maxZ=values[5]
    minZ=values[2]            
    x = minX + ((maxX - minX) /2)
    y = minY + ((maxY - minY) /2)
    z = minZ + ((maxZ - minZ) /2)
    return (x,y,z)
def circleTopo(nam,sub,ax):
    ligaFace(15,sub,nam,2)
    cmds.select(nam)
    cmds.CenterPivot()
    pos=cmds.xform(nam,q=1,t=1)
    mm.eval("PolySelectConvert 3;")
    cmds.scale(0.99,0.99,0.99,r=1,p=(pos[0],pos[1],pos[2]),xn=1,xc='live')
    
def ligaFace(spami,lopi,namelopp,lopi2):
        cmds.rebuildCurve("curve1",ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=spami,d=3,tol=0.01)
        cmds.rebuildCurve("curve2",ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=spami,d=3,tol=0.01)

        cmds.select('curve1','curve2')
        cmds.loft(ch=1,u=1,c=0,ar=1,d=3,ss=1,rn=0,po=0,rsn=1)
        mylof=cmds.ls(sl=1)
        cmds.nurbsToPoly(mylof,mnd=1,ch=1,f=2,pt=1,pc=30,chr=0.9,ft=0.01,mel=0.001,d=0.1,ut=1,un=lopi,vt=1,vn=lopi2,uch=0,ucr=0,cht=0.2,es=0,ntr=0,mrt=0,uss=1)
        cmds.CenterPivot() 
        mesh=cmds.ls(sl=1)
        cmds.rename(mesh[0],namelopp)
        cmds.DeleteHistory()
        cmds.delete('curve1','curve2',mylof[0])
class Mr_window(object):

    def __init__(self):
        
        self.window = "Mr_window"
        self.title = "Ceviche"
        self.mast=None
        self.sub=None 
        self.fin=None 
        self.ini=None 
        if cmds.window(self.window,exists = True):
            cmds.deleteUI(self.window, window= True)
        
        self.window = cmds.window(self.window,title=self.title,s=1)
        
#botones        
        cmds.columnLayout('mainLayout',w=210)
        cmds.separator(w=230,h=10,style='none')
        cmds.rowLayout(w=230,nc=5,parent='mainLayout')
        self.comv=cmds.optionMenu(w=57)
        cmds.menuItem('all')
        cmds.menuItem('rotate')
        cmds.menuItem('translate')
        self.mas=cmds.button(label='master',command=self.master,w=57)    
        self.ctrl=cmds.button(label='Control',command=self.follhijo,w=57,bgc=(.7,.9,.9))    

        cmds.rowLayout(w=230,nc=5,parent='mainLayout')
        self.bini=cmds.button(label='start',command=self.frini,w=57)    
        self.bfin=cmds.button(label='ent',command=self.frfin,w=57)    
        cmds.button(label='Bake',command=self.bakekey2,w=57,bgc=(.9,.9,.9))    
        cmds.rowLayout(w=230,nc=5,parent='mainLayout')
        cmds.button(label='select Loc',command=self.sel,w=114)        
        cmds.showWindow()
    def sel(self, *args):
        cmds.select(self.sub[0]+'_followLOK')        
    def frfin(self, *args):
        self.fin=cmds.currentTime(q=1)
        cmds.button(self.bfin,e=1,l='%s'%int(self.fin))    
    def frini(self, *args):
        self.ini=cmds.currentTime(q=1)
        cmds.button(self.bini,e=1,l='%s'%int(self.ini))    
    def master(self, *args):
        self.mast=cmds.ls(sl=1)[0]
        cmds.button(self.mas,e=1,l=self.mast)    
    def follhijo(self,*args):
        valuerot=cmds.optionMenu(self.comv,q=1,v=1)
        self.sub=cmds.ls(sl=1)
        cmds.button(self.ctrl,e=1,l=self.sub[0])    
        if self.mast==None:
            cmds.spaceLocator(n='masterF')
            self.mast='masterF'
        def foolok(a):
            cmds.spaceLocator(n=a+'_followLOK')
            cmds.parentConstraint(a,a+'_followLOK')
            cmds.parentConstraint(a,a+'_followLOK',rm=1)
            cmds.parent(a+'_followLOK',self.mast)
        if valuerot=='rotate':
            foolok(self.sub[0])
            cmds.orientConstraint(self.sub[0]+'_followLOK',self.sub[0],mo=1)
        if valuerot=='all':
            foolok(self.sub[0])
            cmds.parentConstraint(self.sub[0]+'_followLOK',self.sub[0],mo=1)
        if valuerot=='translate':
            foolok(self.sub)
            cmds.pointConstraint(self.sub[0]+'_followLOK',self.sub[0],mo=1)
    def bakekey2(self,*args):
        valuerot=cmds.optionMenu(self.comv,q=1,v=1)
        frFinl=self.fin
        if valuerot=='rotate':
            cmds.bakeResults(self.sub[0]+'.rotateX',self.sub[0]+'.rotateY',self.sub[0]+'.rotateZ',sampleBy=1,oversamplingRate=1,time=(self.ini,frFinl),preserveOutsideKeys=1,sparseAnimCurveBake=0)
            cmds.delete(self.sub[0]+'_followLOK')    
        if valuerot=='all':
            cmds.bakeResults(self.sub[0]+'.rotateX',self.sub[0]+'.rotateY',self.sub[0]+'.rotateZ',self.sub[0]+'.translateX',self.sub[0]+'.translateY',self.sub[0]+'.translateZ',sampleBy=1,oversamplingRate=1,time=(self.ini,frFinl),preserveOutsideKeys=1,sparseAnimCurveBake=0)
            cmds.delete(self.sub[0]+'_followLOK')
        if valuerot=='translate':
            cmds.bakeResults(self.sub[0]+'.translateX',self.sub[0]+'.translateY',self.sub[0]+'.translateZ',sampleBy=1,oversamplingRate=1,time=(self.ini,frFinl),preserveOutsideKeys=1,sparseAnimCurveBake=0)
            cmds.delete(self.sub[0]+'_followLOK')
        if self.mast==None:
            cmds.delete('masterF')
        self.mast=None
        cmds.button(self.mas,e=1,l='master')    
        cmds.button(self.ctrl,e=1,l='control')    

er=Mr_window()