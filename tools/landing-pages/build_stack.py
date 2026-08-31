# -*- coding: utf-8 -*-
"""Parse each recipe step into a pour: what goes in the glass, and how much.

The signature element of these pages is the build — every GT drink is the same
gesture (ice, 50 ml of concentrate, top up) and the differences between 48 drinks
are differences of proportion. Drawing that proportion is more honest than a
numbered badge, and it makes sixteen cards look like sixteen drinks instead of
sixteen boxes.
"""
import re

# kind -> (swatch role, default ml when the step states none)
KINDS = {
    'ice':      ('ice',    120),
    'base':     ('base',    50),   # GT concentrate / matcha base / ube base
    'fruit':    ('fruit',   40),   # purée, juice, lychee water
    'water':    ('water',  150),
    'soda':     ('soda',   150),
    'tonic':    ('soda',   150),
    'milk':     ('milk',   150),
    'coconut':  ('milk',   150),
    'foam':     ('foam',    45),
    'espresso': ('coffee',  30),
    'syrup':    ('syrup',   15),
    'garnish':  ('garnish',  0),
}

def classify(step):
    s = step
    ml = None
    m = re.search(r'(\d+)\s*מ״ל', s)
    if m: ml = int(m.group(1))

    if s.startswith('מלאו כוס בקרח'):            k = 'ice'
    elif s.startswith('קשטו'):                    k = 'garnish'
    elif 'ערבבו' in s and 'והגישו' in s:          k = 'garnish'
    elif 'תמצית חליטת' in s or 'בסיס מאצ' in s or 'בסיס אובה' in s:  k = 'base'
    elif 'סירופ אגבה' in s:                       k = 'syrup'
    elif 'אספרסו' in s:                           k = 'espresso'
    elif 'קרם קוקוס' in s or 'מי קוקוס' in s:     k = 'coconut'
    elif 'קצף' in s:                              k = 'foam'
    elif 'חלב' in s:                              k = 'milk'
    elif 'טוניק' in s:                            k = 'tonic'
    elif 'סודה' in s:                             k = 'soda'
    elif 'לימונדה' in s:                          k = 'soda'
    elif 'מחית' in s or 'מיץ' in s or 'מי ליצ' in s: k = 'fruit'
    elif 'מים' in s:                              k = 'water'
    else:                                         k = 'water'

    role, dml = KINDS[k]
    return dict(kind=k, role=role, ml=(ml if ml is not None else dml), text=step)

def pours(steps):
    return [classify(s) for s in steps]
