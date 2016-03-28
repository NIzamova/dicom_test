/**
* Copyright 2012-2016, Plotly, Inc.
* All rights reserved.
*
* This source code is licensed under the MIT license found in the
* LICENSE file in the root directory of this source tree.
*/

'use strict';

var arraysToCalcdata = require('../scatter/arrays_to_calcdata');
var calcMarkerColorscale = require('../scatter/marker_colorscale_calc');


/**
 * This is a kludge to put the array attributes into
 * calcdata the way Scatter.plot does, so that legends and
 * popovers know what to do with them.
 */
module.exports = function calc(gd, trace) {
    var cd = [{x: false, y: false, trace: trace, t: {}}];

    arraysToCalcdata(cd);
    calcMarkerColorscale(trace);

    return cd;
};
