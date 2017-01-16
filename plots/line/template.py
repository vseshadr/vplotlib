from plots.base.template import template as base_template
from copy import deepcopy

template = deepcopy(base_template)

template['xtics']['help-lines'] = False
template['xtics']['label-shift'] = 0.5

template['xlabel']['yshift'] = 1

template['legend']['size'] = 4
template['legend']['symbol-yshift'] = 0.75
template['legend']['symbol-xshift'] = 1
template['legend']['hpadding'] = 1
template['legend']['relative'] = 'inside'
template['legend']['location'] = 'north west'
template['legend']['arrange'] = 'horizontal'

template['line'] = {
    'padding' : 1,

    'line-styles-2' : [
        'semithick',
        'densely dashed,semithick'
        ],
    
    'line-styles-3' : [
        'semithick,black!80',
        'densely dotted,very thick',
        'very thick',
        ],

    'line-styles-4' : [
        'semithick,black!80',
        'densely dashed,semithick',
        'densely dotted,very thick',
        'very thick',
        ],

    'line-styles-5' : [
        'semithick,black!40',
        'densely dotted,thick',
        'thick',
        'densely dashed,thick',
        'ultra thick',
        ],

    'line-styles-6' : [
        'semithick,black!40',
        'semithick,black!70,densely dashed',
        'thick',
        'semithick,black!60,densely dashed',
        'semithick,black!20',
        'semithick,black!80',
        ],

    'line-styles-7' : [
        'densely dashed,very thick',
        'semithick,black!40',
        'black!70,densely dashed',
        'very thick',
        'black!60,densely dashed',
        'semithick,black!20',
        'black!80',
        ],

    'line-styles-8' : [
        'semithick,black!40',
        'densely dotted,thick',
        'very thick',
        'dashed,very thick',
        'dotted,thick',
        'densely dashed,thick',
        'ultra thick',
        ],

    'line-styles-n' : [
        'semithick,black!40',
        'densely dotted,thick',
        'thick',
        'densely dashed,thick',
        'ultra thick',
    ],
    
}

template['marker'] = {
    'display' : True,
    
    'marker-styles' : [
        '*',
        '*',
        '*',
        '*',
        '*',
    ]
}
