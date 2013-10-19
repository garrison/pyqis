import json

import numpy as np

from IPython.core.display import Javascript

urls = {
    "mathjs": "https://raw.github.com/josdejong/mathjs/e656ec0fb4489ca3a7c951401d59efac10ad5633/math.min.js",
    "raphael": "https://raw.github.com/DmitryBaranovskiy/raphael/52bff469f60988f1391e8b3d7cb5349163df8ba1/raphael.js",
    "jsqis-core": "https://raw.github.com/garrison/jsqis/master/jsqis-core.js",
    "jsqis-view": "https://raw.github.com/garrison/jsqis/master/jsqis-view.js",
    "jsqis-view.css": "https://raw.github.com/garrison/jsqis/master/jsqis-view.css",
}

def realize_array(v):
    return np.vstack((np.real(v), np.imag(v))).flatten(order="F")

def json_realize_array(v):
    return json.dumps(list(realize_array(v)))

_is_initialized = False

def show_state(state):
    # javascript libraries
    jsqis_lib = (
        urls["mathjs"],
        urls["jsqis-core"],
    )
    jsqis_css = (
        urls["jsqis-view.css"],
    )

    # prepare the json representation of the state
    json_state = json_realize_array(state.state)

    # javascript code
    code = """
    window.olddefine = window.define;
    window.define = undefined;
    $.getScript({{{ RAPHAEL_URL }}}, function () {
    $.getScript({{{ JSQIS_VIEW_URL }}}, function () {

    // import the json representation of the state
    var jsonState = {{{ JSON_STATE }}};

    // convert the json representation to an amplitude list of mathjs complex numbers
    var amplitudeList = [];
    var i, e = jsonState.length;
    for (i = 0; i < e; i += 2) {
        amplitudeList.push(math.complex(jsonState[i], jsonState[i + 1]));
    }

    // determine the number of qubits
    var nQubits = 0, basisSize = 1;
    while (basisSize < jsonState.length) {
        nQubits += 1;
        basisSize *= 2;
    }

    // use the state to construct a jsqis QuantumBitMachine object
    var machine = new jsqis.QuantumBitMachine(nQubits);
    machine.amplitudeList = amplitudeList;

    // use jsqis-view to display the QuantumBitMachine
    var machineView = new jsqis.QuantumBitMachineView(element[0], machine);
    container.show();

    window.define = window.olddefine;
    });
    });
    """.replace("{{{ JSON_STATE }}}", json_state).replace("{{{ RAPHAEL_URL }}}", repr(urls["raphael"])).replace("{{{ JSQIS_VIEW_URL }}}", repr(urls["jsqis-view"]))

    return Javascript(code, lib=jsqis_lib, css=jsqis_css)
