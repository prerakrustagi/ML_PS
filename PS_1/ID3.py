from node import Node
import math

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


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

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
    else:
      subData = []
      for instance in data:
        if str(instance[bestAttrib]) == str(value):
          subData.append(instance)
      treeNode.children.append(tempChild)
      tempAvailableAttributes = availableAttributes.copy()
      tempAvailableAttributes.remove(bestAttrib)
      createTree(subData, tempAvailableAttributes, tempChild)
