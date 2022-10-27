# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *



ModelName='Model-2'

try:
    del mdb.models[ModelName] 
except:
    pass
    
mdb.Model(modelType=STANDARD_EXPLICIT, name=ModelName)


#Create Parts
mdb.models[ModelName].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[ModelName].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[ModelName].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[ModelName].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[ModelName].sketches['__profile__'].geometry[2])
mdb.models[ModelName].sketches['__profile__'].ArcByCenterEnds(center=(0.0, 3.0)
    , direction=CLOCKWISE, point1=(0.0, 6.0), point2=(0.0, 0.0))
mdb.models[ModelName].Part(dimensionality=AXISYMMETRIC, name='indenter', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[ModelName].parts['indenter'].BaseWire(sketch=
    mdb.models[ModelName].sketches['__profile__'])
del mdb.models[ModelName].sketches['__profile__']
mdb.models[ModelName].parts['indenter'].ReferencePoint(point=
    mdb.models[ModelName].parts['indenter'].InterestingPoint(
    mdb.models[ModelName].parts['indenter'].edges[0], CENTER))
mdb.models[ModelName].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[ModelName].sketches['__profile__'].sketchOptions.setValues(
    viewStyle=AXISYM)
mdb.models[ModelName].sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -100.0), point2=(0.0, 100.0))
mdb.models[ModelName].sketches['__profile__'].FixedConstraint(entity=
    mdb.models[ModelName].sketches['__profile__'].geometry[2])
mdb.models[ModelName].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(8.0, -8.0))
mdb.models[ModelName].Part(dimensionality=AXISYMMETRIC, name='substrate', type=
    DEFORMABLE_BODY)
mdb.models[ModelName].parts['substrate'].BaseShell(sketch=
    mdb.models[ModelName].sketches['__profile__'])
del mdb.models[ModelName].sketches['__profile__']



#Materials & Sections
mdb.models[ModelName].Material(name='Material-1')
mdb.models[ModelName].materials['Material-1'].Elastic(table=((0.2, 0.3), ))
mdb.models[ModelName].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models[ModelName].parts['substrate'].Set(faces=
    mdb.models[ModelName].parts['substrate'].faces.getSequenceFromMask((
    '[#1 ]', ), ), name='Set-1')
mdb.models[ModelName].parts['substrate'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models[ModelName].parts['substrate'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)



#Assembly
mdb.models[ModelName].rootAssembly.DatumCsysByThreePoints(coordSysType=
    CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
    0.0, -1.0))
mdb.models[ModelName].rootAssembly.Instance(dependent=ON, name='indenter-1', 
    part=mdb.models[ModelName].parts['indenter'])
mdb.models[ModelName].rootAssembly.Instance(dependent=ON, name='substrate-1', 
    part=mdb.models[ModelName].parts['substrate'])


#step
mdb.models[ModelName].StaticStep(name='Step-1', nlgeom=ON, previous='Initial')


#Interaction
mdb.models[ModelName].ContactProperty('IntProp-1')
mdb.models[ModelName].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models[ModelName].rootAssembly.Surface(name='m_Surf-1', side1Edges=
    mdb.models[ModelName].rootAssembly.instances['indenter-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[ModelName].rootAssembly.Surface(name='s_Surf-1', side1Edges=
    mdb.models[ModelName].rootAssembly.instances['substrate-1'].edges.getSequenceFromMask(
    ('[#1 ]', ), ))
mdb.models[ModelName].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Step-1', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='IntProp-1', master=
    mdb.models[ModelName].rootAssembly.surfaces['m_Surf-1'], name='Int-1', 
    slave=mdb.models[ModelName].rootAssembly.surfaces['s_Surf-1'], sliding=
    FINITE, thickness=ON)
mdb.models[ModelName].rootAssembly.Set(edges=
    mdb.models[ModelName].rootAssembly.instances['substrate-1'].edges.getSequenceFromMask(
    ('[#4 ]', ), ), name='Set-1')


#Bcs
mdb.models[ModelName].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=mdb.models[ModelName].rootAssembly.sets['Set-1'], u1=UNSET, 
    u2=0.0, ur3=UNSET)
mdb.models[ModelName].rootAssembly.Set(name='Set-2', referencePoints=(
    mdb.models[ModelName].rootAssembly.instances['indenter-1'].referencePoints[2], 
    ))
mdb.models[ModelName].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-2', region=mdb.models[ModelName].rootAssembly.sets['Set-2'], u1=0.0, 
    u2=-1.5, ur3=0.0)

#Mesh
mdb.models[ModelName].parts['indenter'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.67)
mdb.models[ModelName].parts['indenter'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.3)
mdb.models[ModelName].parts['indenter'].generateMesh()
mdb.models[ModelName].parts['indenter'].setElementType(elemTypes=(ElemType(
    elemCode=RAX2, elemLibrary=STANDARD), ), regions=(
    mdb.models[ModelName].parts['indenter'].edges.getSequenceFromMask(('[#1 ]', 
    ), ), ))
mdb.models[ModelName].parts['substrate'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.8)
mdb.models[ModelName].parts['substrate'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.1)
mdb.models[ModelName].parts['substrate'].generateMesh()
mdb.models[ModelName].parts['substrate'].setElementType(elemTypes=(ElemType(
    elemCode=CAX4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
    elemCode=CAX3, elemLibrary=STANDARD)), regions=(
    mdb.models[ModelName].parts['substrate'].faces.getSequenceFromMask((
    '[#1 ]', ), ), ))
mdb.models[ModelName].rootAssembly.regenerate()


#jobs
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=ModelName, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name=ModelName, nodalOutputPrecision=
    SINGLE, numCpus=2, numDomains=2, numGPUs=1, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[ModelName].submit(consistencyChecking=OFF)


# Save by Yangkun on 2022_01_28-12.31.50; build 2020 2019_09_13-18.49.31 163176
