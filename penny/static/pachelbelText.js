function get_keys(obj) {
    var r = [];
    for ( var key in obj ) {
        r.push(key);
    }
    return r;
}

var a = 0;
function parse_json(data) {
    var h = "";
    h += "<table width='100%'>";
    h += "<tr><td width='24px'>#</td><td width='48px'>X</td><td width='48px'>Y</td><td width='96px'>Direction</td><td width='96px'>Speed (m/s)</td><td style='text-align: left;'>Neighbors Retrieved From Routing Tables</td></tr>";
    if ( a == 0 ) {
        a = 1;
        console.log(data);
    }
    var keys = get_keys(data).sort();
    for(var key_index in keys) {
        var key = keys[key_index];
        h += "<tr>";
        h += "<td>" + key + "</td>";
        h += "<td>" + Math.round(data[key].x) + "</td>";
        h += "<td>" + Math.round(data[key].y) + "</td>";
        h += "<td>" + data[key].direction + "</td>";
        h += "<td>" + Math.round(data[key].speed) + "</td>";
        h += "<td style='text-align: left;'>";
        for (var neighbor_index in data[key].neighbors) {
            h += data[key].neighbors[neighbor_index] + ", ";
        }
        h += "</td>";
        h += "</tr>";
    }
    h += "</table>";

    $('#text_content').html(h);
}

function pulling_loop() {
    $.getJSON('pachelbelJSON', function(data) {
        parse_json(data);
        setTimeout(pulling_loop, 500);
    });
}

$(document).ready(function(){
    pulling_loop();
});
