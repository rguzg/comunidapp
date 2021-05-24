"use strict"


function showGraph() {;
    const headers = document.querySelectorAll('.loading-header');
    headers.forEach(e => e.classList.add('d-none'));
}


const createVisualization = async (endPath) => {
    const URL = `http://127.0.0.1:8000/relaciones/${endPath}/`;

    const body =  await fetch(URL);
    const data = await body.json();

    showGraph();

    // Create graph
    const width = 1050, height = 490, radius = 10;
    const svg = d3.select(`#container-${endPath}`).append('svg')
    .attr({
        width: width,
        height: height
    })
    .attr('id', `network-${endPath}`)
    .classed("animate__animated animate__fadeIn", true);
    
    // Debug
    console.log(endPath)
    console.log(svg);
    console.table(data);

    let links = [];
    data.edges.forEach((e) => { 
        // Get the source and target nodes
        let sourceNode = data.nodes.filter((n) => n.id === e.source)[0],
            targetNode = data.nodes.filter((n) => n.id === e.target)[0];

        // Add the edge to the array
        links.push({source: sourceNode, target: targetNode});
    });
    
    let force = d3.layout.force()
        .nodes(data.nodes)
        .links(links)
        .size([width, height])
        .linkDistance(20)
        .charge(-2000)
        .start();

    let edges = svg.selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .style('stroke', '#ccc')
        .style('stroke-width', 1);
    
    let nodes = svg.selectAll('g')
    .data(data.nodes)
    .enter()
    .append('g')
    .call(force.drag);

    let colors = d3.scale.category20();
    nodes.append('circle')
    .attr('r', 10)
    .attr({
    r: 10,
    fill: function(d, i) {
    return colors(i);
    },
    stroke: 'black',
    'stroke-width': 0
    })
    .call(force.drag()
    .on("dragstart", function(d) {
    d.fixed = true;
    d3.select(this).attr('stroke-width', 3);
    }))
    .on('dblclick', function(d) {
    d.fixed = false;
    d3.select(this).attr('stroke-width', 0);
    });

    nodes.append('text')
        .attr({
                dx: 12,
                dy: '.35em',
                'pointer-events': 'none'
            })
    .style('font', '10px sans-serif')
            .text(function (d) { return d.first_name });
    
    force.on('tick', () =>{
        nodes.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        nodes.attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
        .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });

        edges.each(function (d) {
            d3.select(this).attr({
                x1: d.source.x,
                y1: d.source.y,
                x2: d.target.x,
                y2: d.target.y
            });
        });
});
}

// Tabs is a collection of the elements with the class 'nav-link'.
const tabs = document.getElementsByClassName('nav-link');

tabs[0].onload = createVisualization(tabs[0].dataset.path);

for(let i = 1; i<tabs.length; i++){
    tabs[i].addEventListener('click', () => createVisualization(tabs[i].dataset.path), {once:true});
}
