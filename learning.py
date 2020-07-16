class Node:
	def __init__(self,dataval = None):
		self.dataval = dataval
		self.nextval = None

class LinkedList:
	def __init__(self):
		self.headval = None

	def printList(self):
		printval = self.headval
		while printval is not None:
			print(printval.dataval)
			printval = printval.nextval

	def atbegin(self,newdata):
		NewNode = Node(newdata)
		NewNode.nextval  =  self.headval
		self.headval = NewNode

	def atend(self,newdata):
		NewNode = Node(newdata)
		if self.headval is None:
			self.headval = NewNode
			return
		last = self.headval
		while(last.nextval):
			last = last.nextval
		last.nextval = NewNode

	def inmiddle(self,middle_node, newdata):
		if middle_node is None:
			print("Node doesn't Exist")
			return
		NewNode = Node(newdata)
		NewNode.nextval = middle_node.nextval
		middle_node.nextval = NewNode

list1 = LinkedList()
list1.headval = Node("Mon")
e2 = Node("Tues")
e3 = Node("Thur")
e4 = Node("Fir")

list1.headval.nextval = e2
e2.nextval = e3
e3.nextval = e4

last = list1.headval
while(last.nextval):
	if(last.nextval.dataval == "Tues"):
		list1.inmiddle(last.nextval, "Wed")
		break
	last = last.nextval
# list1.inmiddle(list1.headval.nextval.nextval, "Thur")


list1.printList()