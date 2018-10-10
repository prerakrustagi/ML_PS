from node import Node
import math
CLASS = "Class"

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  root = Node(None, None, None)
  attributes = getAttributesList(examples)
  buildTree(examples, default, root, attributes)
  return root

def buildTree(examples, default, parentNode, attributes):
  if not examples:
    parentNode.addChild(Node(default, default, default))
  elif isNonTrivialSplitPossible(examples) == False:
    modeClass = getModeClassLabel(examples)
    parentNode.addChild(Node(modeClass, modeClass, modeClass))
  else:
    bestAttribute = getBestAttribute(examples, attributes)
    possibleValues = getPossibleValuesForAttribute(examples, bestAttribute)
    for value in possibleValues:
      child = Node(bestAttribute, value, None)
      examplesWithBesAttributeValue = getExamplesWithBestAttributeValue(examples, bestAttribute, value)
      modeOfExampleWithBestValue = getModeClassLabel(examplesWithBesAttributeValue)
      if attributes.__contains__(bestAttribute):
        attributes.remove(bestAttribute)
      buildTree(examplesWithBesAttributeValue, modeOfExampleWithBestValue, child, attributes)
      parentNode.addChild(child)

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
  bestAttribute = None
  minEntropy = None
  for attribute in attributes:
    entropy = getInfoGainForAttribute(examples, attribute)
    if entropy is None:
      continue    
    elif minEntropy is None:
      minEntropy = entropy
      bestAttribute = attribute
    elif entropy < minEntropy:
      minEntropy = entropy
      bestAttribute = attribute
  return bestAttribute

def getInfoGainForAttribute(examples, attribute):
  '''
  1. list the possible output values for this attribute
  2. foreach attribute value: calculate P(Ai = v) * entropy of Y for Ai = v
  3. return sum of above 
  '''
  attrOutputValues = set()  # unique output values possible for this attribute
  # attributeValueOutputListMap = []
  for example in examples:
    attrOutputValues.add(example[attribute])
    # attributeValueOutputListMap.append(dict(example[attribute], example["class"]))
  if len(attrOutputValues) is 1:
    return None
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
  originalAccuracy = test(node, examples)
  


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
  tempNode = node
  while tempNode.children is not None:
    for child in tempNode.children:
      if(child.output is not None):
        return child.output
      elif example[child.attribute] == child.value:
        tempNode = child
        continue
  return None



  
