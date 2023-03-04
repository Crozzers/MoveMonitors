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


def calc_fuzzy_pos(devices: list[Monitor], index: int, pos: Sides, align: Sides = 'center'):
    primary = [i for i in devices if i.is_primary][0]
    x, y = 0, 0
    device: Monitor = devices[index]
    new_mode = pywintypes.DEVMODEType()
    if pos in ('top', 'bottom'):
        if align == 'left':
            x = primary.x
        elif align == 'right':
            x = primary.width - device.width
        else:
            x = (primary.width // 2) - (device.width // 2)

        y = primary.height if pos == 'bottom' else primary.y - device.height
    else:
        if align == 'top':
            y = primary.y
        elif align == 'bottom':
            y = primary.height - device.height
        else:
            y = (primary.height // 2) - (device.height // 2)

        x = primary.width if pos == 'right' else primary.x - device.width

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
    args = parser.parse_args()

    # make sure primary monitor is monitor 0, then sort the rest by "\\DISPLAY1..." str
    devices = sorted(
        sorted(screeninfo.get_monitors(), key=lambda a: a.name),
        key=lambda a: a.is_primary, reverse=True
    )

    if args.command == 'list':
        for index, device in enumerate(devices):
            print(index, ':', device)
    else:
        choice: Monitor = devices[args.display]
        mode = calc_fuzzy_pos(devices, args.display, args.side, args.align)

        print(win32api.ChangeDisplaySettingsEx(
            choice.name, mode, 0))
