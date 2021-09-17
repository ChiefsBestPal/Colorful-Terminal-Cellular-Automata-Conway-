import re
import itertools as it
import statistics as stats
from collections.abc import Mapping,Container
from collections import deque
from queue import *
import sys #getsizeof,maxvalues
from typing import Deque, Generator, Iterable, TypeVar,Generic,List,Sequence,get_args,get_type_hints,get_origin
from functools import wraps
from copy import deepcopy
import multiprocessing#!sys.path.append(r'C:/Users/Antoine/Desktop/Coding+/DataStructuresInPy')



#!
#!External function, to get memory and garbage collector management of nested datastructures
#!
class MemoryManagement(object):
    def deep_getsizeof(obj=object(), ids = set()):
        """Find the memory footprint of obj
    
        This is a recursive function that drills down a Python object graph
        in order to deepcopy even nested structures
    
        sys.getsizeof function is shallow. It counts each
        object inside defined container without looking inside
        >>> This does just that : deep_mem_allocated
        """
        deep = MemoryManagement.deep_getsizeof#?TO BE CONCISE
        if id(obj) in ids:
            return 0
    
        recur_mem = sys.getsizeof(obj)
        ids.add(id(obj)) #stuff recursively added here
        
        if isinstance(obj, str): #TODOor isinstance(0, Unicode):
            return recur_mem
    
        if isinstance(obj, Mapping):#dict
            return recur_mem + sum(deep(key, ids) + deep(values, ids) for key, values in obj.iteritems()) #recusion
    
        if isinstance(obj, Container):#Abstract base class
            return recur_mem + sum(deep(x, ids) for x in obj) #recursion
    
        return recur_mem
    @staticmethod
    def recursion_limit() -> None:
        print(sys.getrecursionlimit(),sep="",end=" : Current Maximum recusion depth\n")


def DefaultObjectMethod(DOC=True,DEBUG=False):#TODO generalization and debugging
    def DefaultObjectMethod_decorator(func):#! THIS IS CALLED A CLOSURE
        @wraps(func) #*avoid getting some attributes overriden!
        def func_wrapper(*args,**kwargs):

            if DOC:#!print DOCSTRING
                print(func.__doc__,end="\n\n") 

            return func(*args,**kwargs)

        return func_wrapper #?default
    return DefaultObjectMethod_decorator


Python_Primitives = [int,float,str,bool]
T = TypeVar('T')#template, simulating static typed programming

class StackSizeError(Exception):
    pass

class Stack(Generic[T]): #TODO eventually, will be metaclass of something
    StackMethod = deepcopy(DefaultObjectMethod)
    assert callable(StackMethod)
    @staticmethod
    def format_iter(iterable)->Deque[T]:
        """ format input iterable to proper universal list
        Nested structures will be absolutely flattened into single byte elements"""

        if not isinstance(iterable,Iterable):
            raise TypeError

        if type(iterable) == dict:
            iterable = iterable.values()
        iterable = list(iterable) #!next iter not suitable, so we use this O(n)solution
        try:
            first_el = iterable[0]
            supposed_static_type = type(first_el)#all elements are supposed to be same type
        except (IndexError,StopIteration) as iterableEmpty:
            print(iterableEmpty)
            return deque([])

        if all(isinstance(el, supposed_static_type) for el in iterable):
            #*Nd to 1d with weird python casting
            flattened = ' '.join(filter(str.isalnum, str(iterable))).replace(r'_',r'')#! Unknown space and time complexity

            supposed_static_type = str if supposed_static_type not in Python_Primitives else supposed_static_type#if not a primitive, cast as string for safety
            return deque(map(str, flattened.split(' ')))
        else:
            raise TypeError   
    
    top = -1
    #*default constructor    
    def __init__(self,max_size = sys.maxsize,items=deque(maxlen= sys.maxsize)):
        assert max_size >= 0
        self.max_size = max_size
        
        self.items = items #! Using Deque to implement Stack for efficiency
    
    @classmethod
    def from_iter(cls,iterable=[]):
        """ transform any iter to stack, where iter[-1] is top"""
        items,max_size = Stack.format_iter(iterable),2**16
        return cls(max_size,items)
    @classmethod
    def from_values(cls,*values):
        """ transform all entered values to stack, where iter[-1] is top """
        generator,max_size = (el for el in values),2**16
        items = Stack.format_iter(generator)
        return cls(max_size,items)

    @property
    def stack(self):
        return self._items #!  _ = PROTECTED
    @stack.deleter
    def stack(self) -> None: 
        self.items.clear()#deque method
    @stack.setter
    def stack(self,newStack) -> None:
        self.items = Stack.format_iter(newStack)


    def __repr__(self): return r"WIP: ALL INFO RELATED TO THIS CLASS, DEPENDENCIES,ETC"
    def __iter__(self): return iter(self.items)#default: next will stop when StopIteration is raised
    def __len__(self): return len(self.items)

    def __str__(self):#visual getter...
        return str(list(self.items))

    @StackMethod(DOC=False)
    def size(self)->int:
        supposed__len__ = len(self.items)
        if abs(supposed__len__) != supposed__len__:
            raise StackSizeError

        return int(supposed__len__)

    @StackMethod(DOC=True)
    def empty(self) -> bool:
        return not bool(self.size() > 0)

    @StackMethod(DOC=True)
    def push(self,element) -> None:
        """ >>> add element to top of stack """
        if self.max_size & self.size() - max(self.max_size,self.size()) <= 0:#can it handle the size before and after the push
            raise StackSizeError(r"STACK OVERFLOW")
        try:
            if not isinstance(element,type(self.items[self.top])) or type(element) == T.__class__: #TODO DEBUG
                raise TypeError
        except IndexError as stackEmptyorNotInitialized:
            pass
        finally:
            self.items.append(element)
            
        

    @StackMethod(DOC=True)
    def pop(self) -> T:
        """ >>> remove element from top of stack and return the element  """ 
        if self.max_size & self.size() - max(self.max_size,self.size()) <= 0:#can it handle the size before and after the pop
            raise StackSizeError(r"STACK UNDERFLOW")
        elif self.empty():
            raise IndexError
        else:
            return self.items.pop()#remove from deque and return

    @StackMethod(DOC=True)
    def peek(self):
        """ >>> return element from top of stack """
        if self.empty():
            return Empty
        return self.items[self.top]

    @StackMethod(DOC=True)
    def search(self,element) -> Generator:
        """ search occurences of element in stack
            >>> return position(s) based from the top of the stack [-1]
            >>> pos(1) is top of stack ([-1]), pos 2 is [-2],etc"""
        try:
            size = len(self.items)
            indices = [index for index,el in enumerate(self.items) if el == element]
        except:
            pass
        if not bool(indices):
            return None
        position_formula = lambda ix: size - ix
        
        for ix in indices:
            yield position_formula(ix)


#!---------------------------------------------------
import operator as op
import threading

from queue import LifoQueue
operators = {
    "+": 1,#?op.__add__,
    "-": 1,#?op.__sub__,
    "*": 2,#?op.__mul__,
    "/": 2,#?op.__truediv__,
    "^": 3,#?op.__pow__,
}

isOperator = lambda char: bool(char in operators.keys())
isOperand = lambda char: char.isalnum()
def precedence(char):
    res = operators.get(char)
    assert res != None
    return res

def infixToPostFix(expression):
    """ Parse infix notation expressions into
        Postfix/Reverse polish notation with 
        my stack custom class """
    stack = Stack[str].from_values("(")
    expression = expression.replace(" ","") + ")" #?assures stack will be empty before infix expr
    RES,char = str(),""

    while not stack.empty():
        char = expression[0]

        if isOperand(char):
            RES += char # add operand to postfix expr
        elif isOperator(char):
            try:
                while isOperator(stack.peek()) and precedence(stack.peek()) >= precedence(char):

                    if set(stack.peek()).intersection(set(char)) == {"^"}: #!SPECIAL RULE: NO LEFT ASSOCIATIVITY FOR EXPONENTS
                        break

                    RES += stack.pop() # add operators from stack with right precedence to postfix expr
                    print(RES)
            except (Empty,AssertionError):
                print("Empty Stack not caught ?")
                continue

            stack.push(char) #Push current operator to stack
        elif char == "(":
            stack.push(char) # Push left parenthesis to stack

        elif char == ")":
            try:
                char = stack.pop() #!USE DO WHILE LOOP TO AVOID THIS DECLARATION
                while char != "(": 
                    RES += char # add elements (operators) of stack until left parenthesis
                    
                    char = stack.pop() # Remove left parenthesis from stack


            except (IndexError,StackSizeError) as UnderFlow:
                
                print(UnderFlow,end=" ... \n")
                break
        else:
            raise Exception("InvalidCharacterOrDigitTooLarge")
        
        expression = expression[1:] 

    return RES

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data
class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

#?------------------------------------------------------------------

#! TREE, NON LINEAR DATA STRUCTURES !
#* Last nodes of a tree are leaves they dont have children nodes
#* Height of a tree:  Longest path to ANY leaf
#* Depth of a node : Length of path to the root
#Binary tree is a tree whose nodes have 0,1 or 2 children

#! This leads us to tree trasversal, i.e. : BFS AND DFS 
#! Traversal/Search options : 
#* DFS-> Explore root to leaf, then backtrack and repeat 
#*BFS-> work by layers so go to neigbour nodes, then next layer 
class BinaryTree:

    format_iter = staticmethod(Stack().format_iter)

    

    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        
    #!__str__; https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    # def __str__(self):
    #     isLeftPresent = bool(self.left_child != None)
    #     isRightPresent = bool(self.right_child != None)

    #     if not (isLeftPresent or isRightPresent):
    #         return "()"
    #     s = ""
    #     if isLeftPresent:
    #         s += str(self.left_child) + " "
    #     s += self.value
    #     if isRightPresent:
    #         s += " " + str(self.right_child)
    #     return "(" + s + ")"

    def insert_left(self, value):
        if self.left_child == None:
            self.left_child = BinaryTree(value)
        else:
            new_node = BinaryTree(value)
            new_node.left_child = self.left_child
            self.left_child = new_node
    def insert_right(self, value):
        if self.right_child == None:
            self.right_child = BinaryTree(value)
        else:
            new_node = BinaryTree(value)
            new_node.right_child = self.right_child
            self.right_child = new_node
    
    nodes_arr = list()
    def clear_nodes_arr(self): 
        self.nodes_arr.clear()
    
    def pre_order(self):
        self.nodes_arr.append(self.value)

        if self.left_child:
            self.left_child.pre_order()

        if self.right_child:
            self.right_child.pre_order()
        
    def in_order(self):
        if self.left_child:
            self.left_child.in_order()

        self.nodes_arr.append(self.value)

        if self.right_child:
            self.right_child.in_order()
            
    def post_order(self):
        if self.left_child:
            self.left_child.post_order()

        if self.right_child:
            self.right_child.post_order()

        self.nodes_arr.append(self.value)
    def bfs(self):
        queue = Queue()
        queue.put(self)

        while not queue.empty():
            current_node = queue.get()
            print(current_node.value)

            if current_node.left_child:
                queue.put(current_node.left_child)

            if current_node.right_child:
                queue.put(current_node.right_child)



#root      
a_node = BinaryTree('a = 10')
a_node.insert_left('b = 5')
#a_node.insert_right('c = 5')

#parent nodes and leafs
b_node = a_node.left_child
b_node.insert_left('c = 3')
b_node.insert_right('d = 7')


c_node = b_node.left_child
c_node.insert_left('e = 1')
c_node.insert_right('f = 4')
f_node = c_node.left_child
f_node.insert_right('g = 2')

d_node = b_node.right_child
d_node.insert_left('h = 6')
d_node.insert_right('i = 9')
i_node = d_node.right_child
i_node.insert_left('j = 8')

#a_node.pre_order()
#print(a_node.nodes_arr)
#print(vars(a_node.left_child))
test_pipes = [u"├──", u"└──", u"│"]
test2_pipes = [u"┌",u""]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
prev,prev_side = None,None
def getLevelUtil(tree_node, value, level=1):
    if (tree_node == None):
        return 0
 
    if (tree_node.value == value):
        return level
 
    downlevel = getLevelUtil(tree_node.left_child,
                             value, level + 1)
    if (downlevel != 0):
        return downlevel
 
    downlevel = getLevelUtil(tree_node.right_child,
                             value, level + 1)
    return downlevel
# Function to print binary tree in 2D 
# It does reverse inorder traversal 
def print2DUtil(root, space=1) :
  
    # Base case 
    if (root == None) :
        return
  
    # Increase distance between levels 
    space += 10
  
    # Process right child first 
    print2DUtil(root.right_child, space) 
  
    # Print current node after space 
    # count 
    print() 
    for i in range(10, space):
        print(end = " ") 
    print(root.value) 
  
    # Process left child 
    print2DUtil(root.left_child, space) 

print2DUtil(a_node)

def _printTree(tree:BinaryTree,ROOT):
    global prev,prev_side
    isLeftPresent = bool(tree.left_child != None)
    isRightPresent = bool(tree.right_child != None)
    if not (isLeftPresent or isRightPresent):#leafs
        
        to_print= f"\033[1m{tree.value} is leaf at level:{getLevelUtil(ROOT,tree.value)}\033[0m and a {prev_side}_CHILD"
        print(to_print)
        prev = tree.value
        return tree.value

    if isLeftPresent:
        # if tree.left_child != BinaryTree:#leaf
        #     new_left = tree.left_child
        # else:
        prev_side = "LEFT"
        new_left = _printTree(tree.left_child,ROOT)
    else:
        new_left = None
    if isRightPresent:
        # if tree.right_child != type(tree):#leaf
        #     new_right = tree.right_child
        # else:
        prev_side = "RIGHT"
        new_right = _printTree(tree.right_child,ROOT)
    else:
        new_right = None
    to_print= f"\033[1m{tree.value} is parent_node at level:{getLevelUtil(ROOT,tree.value)}\033[0m"
    print(to_print)
    prev = tree.value
    return {tree.value : f"({new_left},{new_right})"}

def printTree(initial_root):
    return _printTree(initial_root,ROOT=initial_root)

D = printTree(a_node)

#x[0] = _printTree(x[0])
print(D)


NODE_SIZE = 5#print(int(sum(map(len,list_of_names))/len(list_of_names)))#*stats
resize = lambda word: word.center(NODE_SIZE) if len(word) < NODE_SIZE else word[:NODE_SIZE]#*FOR BUBBLES PRINT

class Tree:

    tree_iterable = []
    def __init__(self, value):
        self.value = value
        #self.current_child = None


    def setNodes(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, Tree(value))

import re
numbers = list(map(str,[1,2,3,4,5,6,7,8,9,10]))
root = dict()
string_repr = "((((1 (2)) 3 (4)) 5 ((6) 7 ((8) 9))) 10)"
split_array = list(re.split(r"\d{2,}|\d+",string_repr[1:-1]))
print(split_array)
for count,i in enumerate(numbers):
    split_array.insert(2*count+1,i)

print(split_array)
new_split = split_array.copy()

for string_ix,string in enumerate(split_array):
    z = re.match(r"\d+",string)
    if z:
        try:
            _prev = split_array[string_ix-1]
            _next = split_array[string_ix+1]
            if _prev[-1] == "(" and _next[0] == ")":
                new_split[string_ix] = "(" + z.group() + ")"
                new_split[string_ix-1] = _prev[:-1]
                new_split[string_ix+1] = _next[1:]
        except IndexError:
            print("Skip")
print(new_split)
split_array = new_split.copy()

for string_ix,string in enumerate(split_array):
    pass
if __name__ == "__main__":
    pass
#     test2 = Stack[int].from_values(32,234,23,3,343,3)

#     print(get_args(test2))
#     print(test2)
#     #dir(Stack)
#     exit()
    #TODO finish reading https://www.freecodecamp.org/news/all-you-need-to-know-about-tree-data-structures-bceacb85490c/



