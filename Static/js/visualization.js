"use strict"


function showGraph() {;
    const headers = document.querySelectorAll('.loading-header');
    headers.forEach(e => e.classList.add('d-none'));
}


const createVisualization = async (endPath) => {
    const URL = `https://comuniuaq.herokuapp.com/relaciones/${endPath}/`;

    const body =  await fetch(URL);
    const data = await body.json();

    showGraph();

    // Create graph
    const radius = 10;
    const WIDTH = document.getElementById(`container-${endPath}`).offsetWidth, HEIGHT = document.getElementById(`container-${endPath}`).offsetHeight;
    // console.log(WIDTH);
    // console.log(HEIGHT);
    const svg = d3.select(`#container-${endPath}`).append('svg')
    .attr({
        width: WIDTH,
        height: HEIGHT
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
    
    let tooltip = d3.select('body').append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0);


    let force = d3.layout.force()
        .nodes(data.nodes)
        .links(links)
        .size([WIDTH, HEIGHT])
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
    })
    .on("mouseover", function(d) {		
        tooltip.transition()		
            .duration(400)		
            .style("opacity", 1);		
        tooltip.append('p').text(() => {if(d.last_name === null){return `Nombre: ${d.first_name}`}else{return `Nombre: ${d.first_name}  ${d.last_name}`} } );
        tooltip.append('p').text(() => {if(d.clave === null){return `Clave: N/A`}else{return `Clave: ${d.clave}`} } );
        tooltip.append('p').text(() => {if(d.facultad.length === 0 ){
            return `Facultad: N/A`
            }else{
                let facultys = [];
                for(let i = 0; i <d.facultad.length;i++){
                    facultys.push(d.facultad[i].nombre);
                }
                return `Facultades: ${facultys.join(', ')}`
            }});
        tooltip.append('p').text(() => {if(d.lineas_investigacion.length === 0){
            return `Líneas de Investigación: N/A`
            }else{
                let researchAreas = [];
                for(let i = 0; i <d.lineas_investigacion.length;i++){
                    researchAreas.push(d.lineas_investigacion[i].nombre);
                }
                return `Lineas de Investigación: ${researchAreas.join(', ')}`
            }});
        	
        tooltip.style("left", (d3.event.pageX) + "px")		
        .style("top", (d3.event.pageY-160) + "px");	
        })				
    .on("mouseout", function(d) {		
        tooltip.transition()		
            .duration(100)		
            .style("opacity", 0)
        .selectAll('p').remove();
    });

    nodes.append('text')
    .attr({
        dx: 12,
        dy: '.35em',
    }) 
    .append('a')
    .attr("xlink:href", function (d) {
        if(d.user === null){
            return '#' 
        }else{
            return `https://comuniuaq.herokuapp.com/user/${d.user}`;
        }
    })
    .attr('target', '_blank')
    .style('font', '10px sans-serif')
    .text(function (d) { return d.first_name });
     
    force.on('tick', () =>{
        nodes.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        nodes.attr("cx", function(d) { return d.x = Math.max(radius, Math.min(WIDTH - radius, d.x)); })
        .attr("cy", function(d) { return d.y = Math.max(radius, Math.min(HEIGHT - radius, d.y)); });

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

const renderVisualization = () =>{
// Tabs is a collection of the elements with the class 'nav-link'.
const tabs = document.getElementsByClassName('nav-link');

tabs[0].onload = createVisualization(tabs[0].dataset.path);

for(let i = 1; i<tabs.length; i++){
    tabs[i].addEventListener('click', () => createVisualization(tabs[i].dataset.path), {once:true});
}
}
renderVisualization();


