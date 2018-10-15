from node import Node
import math, copy
CLASS = "Class"

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

def getExamplesWithBestAttributeValue(examples, bestAttribute, value):
  examplesWithBestValue = []
  for example in examples:
    if example[bestAttribute] is value:
      examplesWithBestValue.append(example)
  return examplesWithBestValue

def isNonTrivialSplitPossible(examples):
  firstClassification = examples[0][CLASS]
  for example in examples:
    if(example[CLASS] != firstClassification):
      return True
  return False

def getModeClassLabel(examples):
  classCountMap = dict()
  for example in examples:
    if example[CLASS] in classCountMap:
      classCountMap[example[CLASS]] += 1
    else:
       classCountMap[example[CLASS]] = 1
  maxOccuringClassLabel = None
  maxOccuringClassCount = None
  for key, value in classCountMap.items():
    if maxOccuringClassLabel is None:
      maxOccuringClassLabel = key
      maxOccuringClassCount = value
    elif value > maxOccuringClassCount:
      maxOccuringClassCount = value
      maxOccuringClassLabel = key
  return maxOccuringClassLabel

def getAttributesList(examples):
  keys = list(examples[0].keys())
  keys.remove(CLASS)
  return keys
  
def getPossibleValuesForAttribute(examples, attribute):
  values = set()  
  for example in examples:
    values.add(example[attribute])
  return list(values)

def getBestAttribute(examples, attributes):
  '''
  calculate the Entropy for each attribute
  select the one which has the least entropy
  '''  
  if(len(attributes) is 1):
    return attributes[0]
  bestAttribute = None
  minEntropy = None
  for attribute in attributes:
    entropy = getEntropyForAttribute(examples, attribute)
    if entropy is None:
      continue    
    elif minEntropy is None:
      minEntropy = entropy
      bestAttribute = attribute
    elif entropy < minEntropy:
      minEntropy = entropy
      bestAttribute = attribute
  return bestAttribute

def getEntropyForAttribute(examples, attribute):
  '''
  1. list the possible output values for this attribute
  2. foreach attribute value: calculate P(Ai = v) * entropy of Y for Ai = v
  3. return sum of above 
  '''
  attrOutputValues = set()  # unique output values possible for this attribute
  for example in examples:
    attrOutputValues.add(example[attribute])
  if len(attrOutputValues) is 1:
    return 1
  totalEntropy = 0
  examplesCount = len(examples)

  for attrValue in attrOutputValues:
    attrValueCount = 0
    possibleClassValues = set()    
    classCountMap = dict()
    for example in examples:
      if(example[attribute] == attrValue):
        attrValueCount += 1
        possibleClassValues.add(example[CLASS])
        if(classCountMap.__contains__(example[CLASS])):
          classCountMap[example[CLASS]] +=1
        else: classCountMap[example[CLASS]] = 1
    attrValueProbability = attrValueCount / examplesCount
    classEntropyForAttrValue = 0
    classLength = len(classCountMap)
    for classValue in possibleClassValues:
      classCount = classCountMap[classValue]
      classValueProbability = classCount / classLength
      classEntropyForAttrValue += (classValueProbability) * (math.log2(classValueProbability))
  totalEntropy += attrValueProbability * classEntropyForAttrValue
  return totalEntropy

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if not examples:
    return
  originalAccuracy = test(node, examples)
  prunableNodes = []
  findPrunableNodes(node, prunableNodes)
  totalPrunableNodes = len(prunableNodes)
  nodesPruned = 0
  while nodesPruned < totalPrunableNodes:
    isNodePruned = pruneNode(node, prunableNodes[nodesPruned],originalAccuracy,examples)
    nodesPruned += 1
    if isNodePruned is True:
      originalAccuracy = test(node, examples)
      prunableNodes = []
      findPrunableNodes(node, prunableNodes)
      totalPrunableNodes = len(prunableNodes)
      nodesPruned = 0  
      isNodePruned = False
  
def pruneNode(rootNode, prunableNode, originalAccuracy, examples):
  if prunableNode.output is not None:
    return False  
  pruneOutput = getPruneOutput(prunableNode)
  pruneChildren = prunableNode.children
  prunableNode.children = []
  prunableNode.children.append(Node(None, None, pruneOutput))
  pruneAccuracy = test(rootNode, examples)
  if originalAccuracy > pruneAccuracy:
    prunableNode.children = pruneChildren
    return False
  return True

def isLeafNode(node):
  return len(node.children) == 1 and node.output == None and node.children[0].output != None


#All the children have the same attribute
#Every child of all children should have an output value
def isPrunableNode(node):  
  if not node.children:
    return False
  attribute = node.children[0].attribute
  for child in node.children:
    if child.attribute is not attribute or not child.children:
      return False
    if len(child.children) == 1 and child.children[0].output is not None:
      continue
    else: 
      return False
  return True  

def findPrunableNodes(node, prunableNodes):
  if isPrunableNode(node):
      prunableNodes.append(node)
  else:
    for child in node.children:
      findPrunableNodes(child, prunableNodes)

def getPruneOutput(node):
  output = None
  attrProb = -1
  for child in node.children:
    if attrProb < child.probability:
      attrProb = child.probability
      output = child.children[0].output
  return output   

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  totalExamples = len(examples)
  correctlyClassifiedExamplesCount = 0
  for example in examples:
    result = evaluate(node, example)
    if result == example[CLASS]:
      correctlyClassifiedExamplesCount += 1
  return correctlyClassifiedExamplesCount / totalExamples

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  ''' 
  tempNode = copy.deepcopy(node)
  childrenTraversed = 0  
  childrenLength = len(tempNode.children)
  while tempNode.children is not None and childrenTraversed <= childrenLength:
    childrenTraversed += 1
    for child in tempNode.children:      
      if(child.output is not None):
        return child.output
      elif str(example[child.attribute]) == child.value:
        tempNode = child
        continue      
  return None  

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
  bestAttributeTotal = bestAttributeInfo['_total']
  del bestAttributeInfo['_total']
  del bestAttributeInfo['_ig']

  for value in bestAttributeInfo:
    attribValueCount = bestAttributeInfo[value]['_total']

    tempChild = Node(value, bestAttrib, None, (1.0 * attribValueCount / bestAttributeTotal))
    if len(bestAttributeInfo[value].keys()) == 2:
      # I will have the leaf node
      output = list(bestAttributeInfo[value].keys())
      output.remove('_total')
      outputVal = output[0]
      try:
        outputVal = int(outputVal)
      except Exception:
        outputVal = outputVal
      tempChild.children.append(Node(None, None, outputVal))
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



  
