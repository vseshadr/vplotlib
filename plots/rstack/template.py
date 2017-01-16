from plots.base.template import template as base_template
from copy import deepcopy

template = deepcopy(base_template)

template['xtics']['help-lines'] = False

template['legend']['size'] = 2
template['legend']['symbol-yshift'] = 0
template['legend']['symbol-xshift'] = 1
template['legend']['hpadding'] = 1
template['legend']['relative'] = 'inside'
template['legend']['location'] = 'north west'
template['legend']['arrange'] = 'horizontal'

template['rstack'] = {
    'padding' : 1,

    'bar-styles-2' : [
        'pattern=north east lines',
        'fill=black'
        ],
    
    'bar-styles-3' : [
        'fill=black!40',
        'fill=black!5',
        'fill=black',
        ],

    'bar-styles-4' : [
        'pattern=north east lines',
        'pattern=crosshatch dots',
        'fill=black!70',
        'fill=black',
        ],

    'bar-styles-5' : [
        'fill=black!20',
        'pattern=north east lines',
        'fill=black!60',
        'pattern=crosshatch dots',
        'fill=black',
        ],

    'bar-styles-6' : [
        'fill=white',
        'fill=black!20',
        'pattern=north east lines',
        'fill=black!60',
        'pattern=crosshatch dots',
        'fill=black',
        ],

    'bar-styles-n' : [
        'pattern=crosshatch dots',
        'fill=black!20',
        'pattern=north west lines',
        'fill=black!60',
        'pattern=north east lines',
        'fill=white',
        'fill=black',
        ], 
    }
