var p_nodes = {};
var p_links = [];
var info = {};
var current_data;
var current_legend = "";

var p_map_margin = 16;

function getScale() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    if ('scale' in vars) {
        return vars['scale'];
    }
    else {
        return 1;
    }
}

function point_with_offset(x, y) {
    return new Point(x * getScale() + p_map_margin, y * getScale() + p_map_margin);
}

function p_initialize(data) {
    min_x = Math.min.apply(null, data['grid_points_x']);
    max_x = Math.max.apply(null, data['grid_points_x']);
    min_y = Math.min.apply(null, data['grid_points_y']);
    max_y = Math.max.apply(null, data['grid_points_y']);

    (new Path.Rectangle(0, 0, max_x * getScale() + 2 * p_map_margin, max_y * getScale() + 2 * p_map_margin)).fillColor = 'black';

    info = data;

    for(var point_index in data['grid_points_x']) {
        (new Path.Line(point_with_offset(data['grid_points_x'][point_index], min_y), point_with_offset(data['grid_points_x'][point_index], max_y))).strokeColor = new GrayColor(.3);
    }
    for(var point_index in data['grid_points_y']) {
        (new Path.Line(point_with_offset(min_x, data['grid_points_y'][point_index]), point_with_offset(max_x, data['grid_points_y'][point_index]))).strokeColor = new GrayColor(.3);
    }

    var num_nodes = Object.keys(data['nodes']).length;
    var node_index = 0;
    for(var node_key in data['nodes']) {
        path = new Path.Circle(point_with_offset(0,0), 5 * getScale());
        path.fillColor = new RgbColor(1, 0, 0);
        path.fillColor.hue += (node_index++) * 360 / num_nodes;
        p_nodes[node_key] = path;
    }
    var tool = new Tool();
    tool.onMouseUp = onMouseUp;
    tool.activate();
}

function links_to_string(neighbors) {
    var r = "";
    for(var i in neighbors)
        r += neighbors[i] + " ";
    return r;
}

function onMouseUp(event) {
    for(var node_key in p_nodes) {
        if(event.point.isInside(p_nodes[node_key].strokeBounds)) {
            current_legend = node_key;
            break;
        }
    }
    fill_legend();
}

function fill_legend() {
    if(current_legend in p_nodes)
        $("#legend").html(
                "<div>" + "Node ID: " + current_legend + ";  Color: <span style='color:" + p_nodes[current_legend].fillColor.toCssString() + ";'> &#9608; </span>" + "</div>"
                + "<div>" + "Location: " + Math.round(current_data[current_legend].x) + ", " + Math.round(current_data[current_legend].y) + "</div>"
                + "<div>" + "links: " + links_to_string(current_data[current_legend].neighbors) + "</div>"
                );
}

function draw(data) {
    current_data = data;
    for(var link_index in p_links) {
        p_links[link_index].remove();
    }
    p_links = [];
    for(var node_key in p_nodes) {
        p_nodes[node_key].position = point_with_offset(data[node_key].x, data[node_key].y);
        for(var neighbor_index in data[node_key].neighbors) {
            neighbor_key = data[node_key].neighbors[neighbor_index];
            if(data[neighbor_key].neighbors.indexOf(node_key) != -1) {
                link = new Path.Line(point_with_offset(data[node_key].x, data[node_key].y), point_with_offset(data[neighbor_key].x, data[neighbor_key].y));
                link.strokeColor = 'white';
                p_links.push(link);
            }
        }
    }

    view.draw();
    fill_legend();
}
