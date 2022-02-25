import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess

gamePath = 'D:/Games/SteamLibrary/steamapps/common/Farming Simulator 22/'
modPath = 'C:/Users/idont/Documents/My Games/FarmingSimulator2022/mods/Empty_4K/maps/mapUS/weights/'
useMapUS = True
mapUSPath = 'data/maps/mapUS/'
useMapFR = False
mapFRPath = 'data/maps/mapFR/'
useMapAlpine = False
mapAlpinePath = 'data/maps/mapAlpine/'
mapFileName = 'map.i3d'
customFileName = ''
modFileName = 'map.i3d'

GraphicsMagick = ['gm.exe']

# XML structure
data = ET.Element('data')
layerElement = ET.SubElement(data, 'Layers')
fileElement = ET.SubElement(data, 'Files')

firstFileId = 200000 # fileId start

def getFileName(root, mapId):
	file = root.find(".//File[@fileId='" + str(mapId) + "']")
	filename = file.get('filename')
	return filename

def finLayerInModFile(layerName,root):
	layer = root.find(".//Layer[@name='" + layerName + "']")
	if layer is None:
		return False
	return True
	
def setNewFileAttributes(fileId,detailMapId,normalMapId,weightMapId,originalRoot):
	# create XML nodes for each map type
	detailMap = ET.SubElement(fileElement,'File')
	normalMap = ET.SubElement(fileElement,'File')
	weightMap = ET.SubElement(fileElement,'File')

	detailMap.set('fileId', str(fileId))
	detailMap.set('filename', getFileName(originalRoot, detailMapId))
	normalMap.set('fileId', str(fileId + 1))
	normalMap.set('filename', getFileName(originalRoot, normalMapId))
	weightMap.set('fileId', str(fileId + 2))
	weightMap.set('filename', getFileName(originalRoot, weightMapId))

def setNewLayerAttributes(name,fileId,unitSize,unitOffsetU,unitOffsetV,blendContrast,attributes):
	# create XML node for the new layer
	newLayer = ET.SubElement(layerElement,'Layer')

	newLayer.set('name', name) # setting new layer name based on the chosen map(s)
	newLayer.set('detailMapId', str(fileId))
	newLayer.set('normalMapId', str(fileId + 1))
	newLayer.set('unitSize', unitSize)
	newLayer.set('unitOffsetU', unitOffsetU)
	newLayer.set('unitOffsetV', unitOffsetV)
	newLayer.set('weightMapId', str(fileId + 2))
	newLayer.set('blendContrast', blendContrast)
	newLayer.set('attributes', attributes)

def getLayersFromMapFile():
	global firstFileId
	global mapFileName

	if bool(customFileName):
		mapFileName = customFileName

	originalMapFile = ET.parse(gamePath + mapFRPath + mapFileName)
	originalRoot = originalMapFile.getroot()
	modMapFile = ET.parse(modPath +  modFileName)
	modRoot = modMapFile.getroot()

	for layer in originalRoot.iter('Layer'):
		name = layer.get('name')
		if finLayerInModFile(name, modRoot) == False:
			unitSize = layer.get('unitSize')
			unitOffsetU = layer.get('unitOffsetU')
			unitOffsetV = layer.get('unitOffsetV')
			blendContrast = layer.get('blendContrast')
			attributes = layer.get('attributes')
			detailMapId = layer.get('detailMapId')
			normalMapId = layer.get('normalMapId')
			weightMapId = layer.get('weightMapId')
			
			setNewLayerAttributes(name,firstFileId,unitSize,unitOffsetU,unitOffsetV,blendContrast,attributes)
			setNewFileAttributes(firstFileId,detailMapId,normalMapId,weightMapId,originalRoot)
			firstFileId += 3

	xmlstr = minidom.parseString(ET.tostring(data)).toprettyxml(indent="    ")
	with open("Layers_files.xml", "w") as f:
	    f.write(xmlstr)

getLayersFromMapFile()
# subprocess.call(GraphicsMagick)