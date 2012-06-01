var p_nodes = {};
var p_links = [];

var p_map_margin = 16;

function point_with_offset(x, y) {
    return new Point(x + p_map_margin, y + p_map_margin);
}

function p_initialize(data) {
    min_x = Math.min.apply(null, data['grid_points_x']);
    max_x = Math.max.apply(null, data['grid_points_x']);
    min_y = Math.min.apply(null, data['grid_points_y']);
    max_y = Math.max.apply(null, data['grid_points_y']);

    (new Path.Rectangle(min_x, min_y, max_x + 2 * p_map_margin, max_y + 2 * p_map_margin)).fillColor = 'black';

    for(var point_index in data['grid_points_x']) {
        (new Path.Line(point_with_offset(data['grid_points_x'][point_index], min_y), point_with_offset(data['grid_points_x'][point_index], max_y))).strokeColor = new GrayColor(.3);
    }
    for(var point_index in data['grid_points_y']) {
        (new Path.Line(point_with_offset(min_x, data['grid_points_y'][point_index]), point_with_offset(max_x, data['grid_points_y'][point_index]))).strokeColor = new GrayColor(.3);
    }

    var num_nodes = Object.keys(data['nodes']).length;
    var node_index = 0;
    for(var node_key in data['nodes']) {
        path = new Path.Circle(point_with_offset(0,0), 5);
        path.fillColor = new RgbColor(1, 0, 0);
        path.fillColor.hue += (node_index++) * 360 / num_nodes;
        p_nodes[node_key] = path;
    }
}

function draw(data) {
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
}
