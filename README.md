# Colorful-Terminal-Cellular-Automata-Conway-
My version of a cellular automaton that is intelligently colored with respect to previous and further states. Offers a simple UI with pygame and system to store drawn patterns; all you need are the requirements and a working ANSI terminal.


## USE THIS LINK TO MAKE A COMPLETE README.MD: 
[StackEditMakeAReadMe](https://stackedit.io/app#)
https://www.nytimes.com/2020/12/28/science/math-conway-game-of-life.html (MUSIC,MATH,TURING COMPLETE,DNA...)

## Showcase of initial tests
![Example1: Pattern drawn and stored](https://github.com/ChiefsBestPal/Colorful-Terminal-Cellular-Automata-Conway-/blob/master/ShowcasePattern.png)
![Example1: Simulation has started with color mode on (initial testing)](https://github.com/ChiefsBestPal/Colorful-Terminal-Cellular-Automata-Conway-/blob/master/ShowCaseGameOfLifeIntial.gif)
```python
class Symbols(Enum):
    dead = u"⬜"
    alive = u"⬛"
    newborn = u"🟩" # (I) state doesnt exist if it is specified otherwise in Cell/Board parent init
    dying = u"🟥" # " " (I)
    
class Cell(object):
  ...
  
  def __call__(self,*,useColors:bool):
      if useColors:
          self.CELL_COLOR_USED = self.cellUpdateColor # (I)
      else:
      ...
```
    
