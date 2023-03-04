# MoveMonitors

A little Windows only script to change the position of a secondary monitor relative to the position of the primary monitor.


### Setup

```
git clone https://github.com/Crozzers/MoveMonitors.git
pip install -r requirements.txt
```

### Usage

```
> python move_monitor.py --help
usage: move_monitor.py [-h] {list,move} ...

positional arguments:
  {list,move}
    list       List displays
    move       Move a display

options:
  -h, --help   show this help message and exit

> python move_monitor.py move --help
usage: move_monitor.py move [-h] display {top,left,bottom,right} [{top,left,bottom,right,center}]

positional arguments:
  display               The index of the display to move
  {top,left,bottom,right}
                        Move to this side of the primary display
  {top,left,bottom,right,center}
                        [optional] align to this edge of the chosen side

options:
  -h, --help            show this help message and exit
```

### Examples

Note: monitors are listed as a 0 based list, so "move 1 left" does not mean the monitor labelled "1" by Windows.
Use `python move_monitor.py list` to get the index of the monitor you want to move. In these examples, "move 1"
corresponds to the secondary monitor.

Command                                       | Result                  
----------------------------------------------|---------------------------
`python move_monitor.py move 1 left`          | ![](img/left-center.png)
`python move_monitor.py move 1 left bottom`   | ![](img/left-bottom.png)
`python move_monitor.py move 1 top right`     | ![](img/top-right.png)
`python move_monitor.py move 1 right top`     | ![](img/right-top.png)
`python move_monitor.py move 1 bottom center` | ![](img/bottom-center.png)
