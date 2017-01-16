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

template['cstack'] = {
    'padding' : 1,

    'bar-styles-1' : [
        'fill=black!30',
        ],
    
    'bar-styles-2' : [
        'fill=black!5',
        'fill=black'
        ],
    
    'bar-styles-3' : [
        'fill=black!30',
        'fill=white',
        'fill=black',
        ],

    'bar-styles-4' : [
        'fill=black!10',
        'fill=black!60',
        'fill=white',
        'fill=black',
        ],

    'bar-styles-5' : [
        'fill=red!20',
        'fill=red!40',
        'fill=red!60',
        'fill=yellow',
        'fill=black',
        ],

    'bar-styles-6' : [
        'fill=red!20',
        'fill=red!40',
        'fill=red!60',
        'fill=yellow',
        'fill=black!50',
        'fill=black',
        ],

    'bar-styles-7' : [
        'fill=red!20',
        'fill=red!40',
        'fill=red!60',
        'fill=yellow',
        'fill=black!10',
        'fill=black!50',
        'fill=black',
        ],
    
    'bar-styles-12' : [
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
        'fill=black!40',
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
