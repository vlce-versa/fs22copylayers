#
#
#
#

import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess

# Settings
gamePath = 'D:/Games/SteamLibrary/steamapps/common/Farming Simulator 22/'
modPath = 'C:/Users/idont/Documents/My Games/FarmingSimulator2022/mods/Empty_4K/maps/mapUS/weights/'
useMapUS = True
mapUSPath = 'data/maps/mapUS/'
useMapFR = False
mapFRPath = 'data/maps/mapFR/'
useMapAlpine = False
mapAlpinePath = 'data/maps/mapAlpine/'
mapFileName = 'map.i3d'
skipDuplicates = True # skips duplicate layers in mod map

# Filename of the map, standard is map.i3d
# use customFilename if its different from the standard file name
customFilename = ''
modFileName = 'map.i3d'

# fileId to start with
# should be higher than the highest fileId in your mod map file
firstFileId = 200000

# GraphicsMagick options
useGraphicsMagick = False
fileSize = '4096px'

# XML structure
# Layers
data = ET.Element('data')
layerElement = ET.SubElement(data, 'Layers')
fileElement = ET.SubElement(data, 'Files')

# XML structure GrapphicsMagick


# getFileName
# gets the filename attribute from the source map
def getFileName(root, mapId):
	file = root.find(".//File[@fileId='" + str(mapId) + "']")
	filename = file.get('filename')
	return filename

# findLayerInModFile
# checks if the layer to be created already exists in the mod map file
def finLayerInModFile(layerName,root):
	layer = root.find(".//Layer[@name='" + layerName + "']")
	if layer is None:
		return False
	return True

# setNewFileAttributes
# sets the file attributes 
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
	newLayer.set('weightMapId', str(fileId + 2))
	newLayer.set('unitSize', unitSize)
	newLayer.set('unitOffsetU', unitOffsetU)
	newLayer.set('unitOffsetV', unitOffsetV)
	newLayer.set('blendContrast', blendContrast)
	newLayer.set('attributes', attributes)

# getLayersFromMapFile
def getLayersFromMapFile():
	global firstFileId
	global mapFileName
	global customFilename

	if bool(customFilename):
		mapFileName = customFilename

	sourceMapFile = ET.parse(gamePath + mapFRPath + mapFileName)
	sourceRoot = sourceMapFile.getroot()
	modMapFile = ET.parse(modPath +  modFileName)
	modRoot = modMapFile.getroot()

	for layer in sourceRoot.iter('Layer'):
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
			setNewFileAttributes(firstFileId,detailMapId,normalMapId,weightMapId,sourceRoot)
			firstFileId += 3

def start():
	getLayersFromMapFile()
	xmlstr = minidom.parseString(ET.tostring(data)).toprettyxml(indent="    ")
	with open("Layer.xml", "w") as f:
	    f.write(xmlstr)

start()

subprocess.call(['gm.exe'])