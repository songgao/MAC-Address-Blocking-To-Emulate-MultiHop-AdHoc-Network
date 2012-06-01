function pulling_loop() {
    $.getJSON('pachelbelJSONGeoAndTopo', function(data) {
        draw(data);
        setTimeout(pulling_loop, 200);
    });
}

function initialize() {
    $.getJSON('pachelbelJSONInfo', function(data) {
        p_initialize(data);
        pulling_loop();
    });
}

paper.install(window);
$(document).ready(function(){
    paper.setup('map_canvas');
    initialize();
});
