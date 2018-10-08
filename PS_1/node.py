class Node:
  def __init__(self, value, attribute, output):
    self.children = []
    self.value = value
    self.attribute = attribute
    self.output = output

  def addChild(self, child):
    self.children.append(child)
