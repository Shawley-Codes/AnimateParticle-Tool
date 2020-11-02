"""
    Scott Hawley    
    
    Animate Particle Tool
    
    Instuctions: To animate particles, either by parenting or by motion path,
    select an option parent or path and then select either the object or curve
    (based on which option) and click execute.
    
    Motion Path: Selecting the motion path option will require you to input the desired
    frames for which to animate from and too. Please select a curve to be turned into a motion
    path for which to animate the object along. 
    
    Parent: Selecting the object will spawn and position the particle emitter on a section of
    the geometry. It can be moved after creation to the desired location. 
   
    v.1.0: Tool is functional, additional functionality can be added, especially setting default values on the n-particles lifespan  
    v.005: changes made to animateCurve to make it function properly, previosly on rendering one time node
           changes made to parentParticle to make it function properly, previosly parenting backwards
    v.004: added move functionality to parent, as well as parenting properly
    v.003: added UI Implementation
    v.002: added parent funtionality
"""
import maya.cmds as mc
#from OptionsWindowBaseClass import OptionsWindow
from OptionsWindowBaseClass import OptionsWindow

#create function calls based on selected options in the ui
def animateCurve(start, finish):
    """
        This function will create an emitter and attach it to a curve 
        with a start and finish animation point.
    """
    #start = mc.intFieldGrp(strnfin,query=True,value1=True)
    #finish = mc.intFieldGrp(strnfin,query=True,value2=True)
    curvetoAnimate = mc.ls(selection=True)
    emitterforAnimation = createEmitter()
    #mc.select(emitterforAnimation, curvetoAnimate)
    mc.select(emitterforAnimation, add=True)
    mc.select(curvetoAnimate, add=True)
    mc.pathAnimation(stu = start,etu = finish)
    
def parentParticles():
    """
        This function will create an emitter and parent it to selected geometry.
        It will then move it to a default position inside the object.
        The particle emitter can still be moved afterwards.
    """ 
    objectToParent = mc.ls(selection=True)
    parentX = mc.getAttr("%s.translateX" % objectToParent[0])
    parentY = mc.getAttr("%s.translateY" % objectToParent[0])
    parentZ = mc.getAttr("%s.translateZ" % objectToParent[0])
    emitterforAnimation = createEmitter()
    mc.move(parentX,parentY,parentZ)
    mc.select(objectToParent, add=True)
    print("about to parent")
    mc.parent()
    print("parented")    


def createEmitter():
    """
        This function creates an emitter and returns it to the caller.
    """
    return mc.NCreateEmitter()
    
#create UI
class particleUI (OptionsWindow):
    def __init__(self):
        self.window = "ParticleWindow"
        self.title = "Particle Tool"
        self.size = (546,350)
        self.actionName = "Apply & Close"
        self.applyName = "Apply"
        super(particleUI, self).__init__()
        
    def actionCmd(self, *args):#override callback group
        """
            When action is called, check radio button selection, the pass any of the important values into the correct
            function
        """
        selected = mc.radioButtonGrp(self.radios, query=True, sl=True)
        print(selected)
        if selected == 1:
            parentParticles()
        elif selected == 2:
            start = mc.intFieldGrp(self.strnfin,query=True,value1=True)
            finish = mc.intFieldGrp(self.strnfin,query=True,value2=True)
            animateCurve(start,finish)
        mc.deleteUI(self.window,window=True)
    
    def applyBtnCmd(self,*args):#does same thing as above
        """
            When action is called, check radio button selection, the pass any of the important values into the correct
            function
        """
        selected = mc.radioButtonGrp(self.radios, query=True, sl=True)
        print(selected)
        if selected == 1:
            parentParticles()
        elif selected == 2:
            start = mc.intFieldGrp(self.strnfin,query=True,value1=True)
            finish = mc.intFieldGrp(self.strnfin,query=True,value2=True)
            animateCurve(start,finish)
    
    def displayOptions(self):
        self.col = mc.columnLayout(adjustableColumn = True)
        self.radios = mc.radioButtonGrp(label="TYPe of Function", labelArray2=["Parent","MotionPath"], numberOfRadioButtons=2)
        self.strnfin = mc.intFieldGrp(numberOfFields = 2, label = "Start & Finish Frames", value1 = 0, value2 = 120)

    
def main():
    #particleUI.create()
    menu1 = particleUI()
    menu1.create()
    
#tool deploy
def AnimateParticleTool():
    main()
    
#testing
#main()
    