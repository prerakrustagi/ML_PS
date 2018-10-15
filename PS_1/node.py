class Node:
  def __init__(self, value, attribute, output, probability = None):
    self.children = []
    self.value = value
    self.attribute = attribute
    self.output = output
    self.probability = probability

  def addChild(self, child):
    self.children.append(child)
