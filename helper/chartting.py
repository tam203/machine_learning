import json
import os
import uuid

TMPLT_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(TMPLT_DIR, '..', 'tmp')


def surface_data(xdata, ydata, zfunc, title="Chart", xlabel="X", ylabel="Y",opacity=1):
    return {
        'z': [[zfunc(x, y) for x in xdata] for y in ydata],
        'y': ydata,
        'x': xdata,
        'type': 'surface',
        'opacity':opacity
    }


def make_chart(data, title="Chart", xlabel="x", ylabel="y" ,zlabel="z", filepath=None):

    file_path = os.path.abspath(os.path.join(OUT_DIR, str(uuid.uuid4()) + '.html')) if filepath is None else filepath
    with open(os.path.join(TMPLT_DIR, "template.html")) as infile:
        with open(file_path, 'w') as outfile:
            template = infile.read()
            template = template.replace("%DATA%", json.dumps(data))
            template = template.replace("%TITLE%", title)
            template = template.replace("%YTITLE%", ylabel)
            template = template.replace("%XTITLE%", xlabel)
            template = template.replace("%ZTITLE%", zlabel)
            outfile.write(template)

    return file_path


def line3d(x, y, z, name=''):

    series = {
        'line': {
            'color': '#00CC00',
            'width': 10
        },
        'mode':'lines',
        'type':'scatter3d',
        'x':x,
        'y':y,
        'z':z
    }
    if name:
        series['name'] = str(name)
    return series

def line2d(*args, **kwargs):
    series = scatter2d(*args, **kwargs)
    series['mode'] = 'line'
    return series

def scatter2d(x,y,name=None):
    series =  {
        'x':x,
        'y':y,
        'mode':'markers',
        'type':'scatter'
    }
    if name:
        series['name'] = str(name)
    return series


def open_chart(chart):
    """Opens a `chart` (a url) in the default browser"""
    print("Opening %s" % chart)
    # This line probably doesn't work on linux. Changing "start" to "xdg-open" might.
    # Else comment out and open manually.
    os.system("start %s" % chart)
