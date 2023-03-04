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
    list       list available displays
    move       move a display

options:
  -h, --help   show this help message and exit

> python move_monitor.py move --help
usage: move_monitor.py move [-h] [-a {top,left,bottom,right,center}] [--rel-to REL_TO] display {top,left,bottom,right}

positional arguments:
  display               the display to move (1 being primary)
  {top,left,bottom,right}
                        Move to this side of the primary display

options:
  -h, --help            show this help message and exit
  -a {top,left,bottom,right,center}, --align {top,left,bottom,right,center}
                        align to this edge of the chosen side
  --rel-to REL_TO       move the monitor relative to the position of this one. Defaults to primary or secondary monitor, whichever is NOT being moved
```

### Examples

Command                                              | Result
-----------------------------------------------------|---------------------------
`python move_monitor.py move 1 right`                | ![](img/left-center.png)
`python move_monitor.py move 2 left --align bottom`  | ![](img/left-bottom.png)
`python move_monitor.py move 1 bottom --align right` | ![](img/top-right.png)
`python move_monitor.py move 2 right --align top`    | ![](img/right-top.png)
`python move_monitor.py move 2 bottom`               | ![](img/bottom-center.png)
