class Node:
  def __init__(self, value, attribute, output, probability = 0):
    self.children = []
    self.value = value
    self.attribute = attribute
    self.output = output
    self.probability = probability

  def addChild(self, child):
    self.children.append(child)
