#!/usr/bin/env python3
import sys
sys.path.insert(0, 'api')
from main import load_ascii_ducks, DUCK_SOUNDS

ascii = load_ascii_ducks()
print(f'Loaded {len(ascii)} ASCII ducks')
print(f'Total DUCK_SOUNDS: {len(DUCK_SOUNDS)}')

if ascii:
    print('\nASCII content:')
    for sound, weight in ascii:
        print(f'  Weight {weight}: {repr(sound[:80])}...' if len(sound) > 80 else f'  Weight {weight}: {repr(sound)}')
else:
    print('\nNo ASCII ducks loaded!')
    
# Check if duck family is in there
has_family = any('🐥' in sound for sound, weight in DUCK_SOUNDS)
print(f'\nDuck family emoji present: {has_family}')

