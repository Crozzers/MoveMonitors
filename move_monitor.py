import argparse
import ctypes
from typing import Literal, get_args

import pywintypes
import screeninfo
import win32api
import win32con
from screeninfo import Monitor

ctypes.windll.user32.SetProcessDPIAware()


Sides = Literal['top', 'left', 'bottom', 'right']


def get_monitors():
    primary = None
    monitors = []
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            primary = monitor
        else:
            monitors.append(monitor)
    monitors.sort(key=lambda a: a.name)
    monitors.insert(0, primary)
    return monitors


def flip_args(pos: Sides) -> Sides:
    flip = {
        'center': 'center',
        'top': 'bottom',
        'left': 'right'
    }
    flip.update({v: k for k, v in flip.items()})

    return flip[pos]


def calc_fuzzy_pos(base: Monitor, device: Monitor, pos: Sides, align: Sides = 'center'):
    x, y = 0, 0
    new_mode = pywintypes.DEVMODEType()
    if pos in ('top', 'bottom'):
        if align == 'left':
            x = base.x
        elif align == 'right':
            x = base.width - device.width
        else:
            x = (base.width // 2) - (device.width // 2)

        y = base.height if pos == 'bottom' else base.y - device.height
    else:
        if align == 'top':
            y = base.y
        elif align == 'bottom':
            y = base.height - device.height
        else:
            y = (base.height // 2) - (device.height // 2)

        x = base.width + base.x if pos == 'right' else base.x - device.width

    new_mode.Position_x = x
    new_mode.Position_y = y
    new_mode.Fields = win32con.DM_POSITION
    return new_mode


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='List displays')
    move_parser = sub.add_parser('move', help='Move a display')
    move_parser.add_argument(
        'display', type=int, help='The index of the display to move')
    move_parser.add_argument('side', choices=get_args(
        Sides), help='Move to this side of the primary display')
    move_parser.add_argument('align', nargs='?', default='center', choices=get_args(
        Sides) + ('center',), help='[optional] align to this edge of the chosen side')
    move_parser.add_argument('--rel-to', default=0, type=int,
                             help='move the monitor relative to the position of this one')
    args = parser.parse_args()

    # make sure primary monitor is monitor 0, then sort the rest by "\\DISPLAY1..." str
    devices = get_monitors()

    if args.command == 'list':
        for index, device in enumerate(devices):
            print(index, ':', device)
    else:
        if args.display == 0:
            # dont move the primary, it causes issues. Move the other one relative to
            # the primary instead
            choice = devices[args.rel_to]
            rel_to = devices[0]
            pos, align = flip_args(args.side), args.align
        else:
            choice = devices[args.display]
            rel_to = devices[args.rel_to]
            pos, align = args.side, args.align

        mode = calc_fuzzy_pos(rel_to, choice, pos, align)

        print(win32api.ChangeDisplaySettingsEx(
            choice.name, mode, 0))
