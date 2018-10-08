
import math
from node import Node

data1 = [
  dict(a= 1, b= 0, c= 1, Class= 'B'),
  dict(a= 0, b= 1, c= 0, Class= 'A'),
  dict(a= 1, b= 1, c= 1, Class= 'A'),
  dict(a= 1, b= 1, c= 0, Class= 'B'),
  dict(a= 0, b= 1, c= 1, Class= 'A')
]

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  id3Tree = Node(None, 'root', None)
  columnArray = list(examples[0].keys())
  columnArray.remove('Class')
  createTree(examples, columnArray, id3Tree)
  return id3Tree


def findBestAttribute(data, availableLabels):
  attribMap = dict()
  bestAttribName = ''
  bestAttribValue = 1
  for label in availableLabels:
    attribMap[label] = dict()

  for row in data:
    for key in row:
      if key != 'Class' and key in availableLabels:
        if not '_total' in attribMap[key]:
          attribMap[key]['_total'] = 0
        attribMap[key]['_total'] += 1
        if not str(row[key]) in attribMap[key]:
          attribMap[key][str(row[key])] = dict()
          attribMap[key][str(row[key])]['_total'] = 0
        if not str(row['Class']) in attribMap[key][str(row[key])]:
          attribMap[key][str(row[key])][str(row['Class'])] = 0
        attribMap[key][str(row[key])][str(row['Class'])] += 1
        attribMap[key][str(row[key])]['_total'] += 1

  for attrib in attribMap:
    attribGain = 0
    attribTotal = attribMap[attrib]['_total']
    for key in attribMap[attrib]:
      if key != '_total':
        keyTotal = attribMap[attrib][key]['_total']
        for subKey in attribMap[attrib][key]:
          if subKey != '_total':
            attribGain += ((1.0 * keyTotal) / attribTotal) * ((-1) * ( ((1.0 * attribMap[attrib][key][subKey]) / keyTotal) * math.log(((1.0 * attribMap[attrib][key][subKey]) / keyTotal)) ) )

    attribMap[attrib]['_ig'] = attribGain
    if bestAttribValue > attribGain:
      bestAttribValue = attribGain
      bestAttribName = attrib

  returnMap = dict()
  returnMap[bestAttribName] = attribMap[bestAttribName]
  return returnMap


def createTree(data, availableAttributes, treeNode):
  bestAttributeInfo = findBestAttribute(data, availableAttributes)
  bestAttrib = next(iter(bestAttributeInfo))
  bestAttributeInfo = bestAttributeInfo[bestAttrib]
  del bestAttributeInfo['_total']
  del bestAttributeInfo['_ig']

  for value in bestAttributeInfo:
    tempChild = Node(value, bestAttrib, None)
    if len(bestAttributeInfo[value].keys()) == 2:
      output = list(bestAttributeInfo[value].keys())
      output.remove('_total')
      tempChild.output = output[0]
      treeNode.children.append(tempChild)
      print('-----------')
      print(tempChild.attribute)
      print(tempChild.value)
      print(tempChild.output)
      print('-----------')
    else:
      subData = []
      for instance in data:
        if str(instance[bestAttrib]) == str(value):
          subData.append(instance)
      treeNode.children.append(tempChild)
      print('-----------')
      print(tempChild.attribute)
      print(tempChild.value)
      print(tempChild.output)
      print('-----------')
      tempAvailableAttributes = availableAttributes.copy()
      tempAvailableAttributes.remove(bestAttrib)
      createTree(subData, tempAvailableAttributes, tempChild)

ID3(data1, 0)
