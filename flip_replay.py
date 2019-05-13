#!/usr/bin/env python

'''
------------------------------------------------------------------------------------------------
Author: @Isaac
Last Updated: 28 Apr 2019
Contact: Message @Isaac at https://forum.c1games.com/
Copyright: CC0 - completely open to edit, share, etc

Short Description: 
This is a python script to flip a replay file so that the views and stats are switched.
------------------------------------------------------------------------------------------------

README:

This script takes an input of a replay file(s) and flips them in a new replay.

The command to run it is:
>py flip_replay.py [LIST OF FILES]
'''

import argparse
import json

def parse_args():
    ap = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('-h', '--help', action='help', help='show this help message and exit\n\n')
    ap.add_argument(
        'files',
        nargs='+',
        default=[],
        help="specify a replay file (or multiple) you'd like to analyze\n\n")
    return vars(ap.parse_args())

def flip_vert(point):
    return [27-point[0], 27-point[1]]

def flip_line(i, original):
    keywords = ['p1Units', 'p1Stats', 'player1']

    for p1key in keywords:
        p2key = p1key.replace('1', '2')

        p1index = original.find(p1key)
        p2index = original.find(p2key)

        if (p1index != -1):
            original = original[:p1index] + p2key + original[p1index + len(p2key):]
        if (p2index != -1):
            original = original[:p2index] + p1key + original[p2index + len(p1key):]

    data = json.loads(original)

    if 'events' in data.keys():
        for event_type in data['events']:
            for unit in data['events'][event_type]:
                uPos = -1 if event_type != 'death' else -2
                unit[uPos] = 1 if unit[uPos] == 2 else 2
                unit[0] = flip_vert(unit[0])
                if event_type == 'selfDestruct':
                    for u in unit[1]:
                        u = flip_vert(u)
                elif event_type == 'shield' or \
                     event_type == 'move' or \
                     event_type == 'attack':
                    unit[1] = flip_vert(unit[1])
    
    if 'p1Units' in data.keys():
        for units in data['p1Units']:
            for unit in units:
                unit[0],unit[1] = flip_vert(unit[:2])
        for units in data['p2Units']:
            for unit in units:
                unit[0],unit[1] = flip_vert(unit[:2])

    if 'endStats' in data.keys():
        data['endStats']['winner'] = 1 if data['endStats']['winner'] == 2 else 2

    return json.dumps(data, separators=(',', ':')) + '\n'

def flip_file(file, flipped_file):
    for i,line in enumerate(file):
        flipped_file.write(flip_line(i,line))

def main(args):
    for file in args['files']:
        with open(file, 'r') as f:
            with open(file[:file.find('.')] + '_flipped.replay', 'w') as new_file:
                flip_file(f, new_file)

if __name__ == "__main__":
    args = parse_args()
    main(args)
