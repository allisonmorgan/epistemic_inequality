const svg = d3.select("#svg");

const lightUp = '#2b2b2b';
const lightEdge = '#444444';
const sourceCol = '#af002d';
const edgeCol = 'lightGrey';
const mstEdgeCol = 'rgb(170, 170, 170)';

const fadeIn = 300;
const fraction = 3.9;

let globalNodes, globalEdges, globalEpidemics;
const highPrestigeSchool = "Stanford University";
const midPrestigeSchool = "University of Colorado at Boulder";
const lowPrestigeSchool = "University of Nebraska at Lincoln";

const parseNodes = new Promise(function(resolve, reject) {
	d3.text("spanningTree/nodes.csv", nodes => {
		resolve(d3.csvParseRows(nodes));
	});
});

const parseLines = new Promise(function(resolve, reject) {
	d3.text("spanningTree/lines2.csv", lines => {
		resolve(d3.csvParseRows(lines));
	});
});

const parseJSON = new Promise(function(resolve, reject) {
	d3.text("spanningTree/CS_SI_timeline3.json", json => {
		resolve(JSON.parse(json));
	});
});

const schoolToCoords = new Map();

window.addEventListener("resize", () => {
	draw(true);
});

Promise.all([parseNodes, parseLines, parseJSON]).then(function([nodes, edges, epidemics]) {
	globalNodes = nodes;
	globalEdges = edges;
	globalEpidemics = epidemics;

	const highPrestigeEdges = svg.append('g').attr('id', 'high-prestige-edges');
    const highPrestigeNodes = svg.append('g').attr('id', 'high-prestige-nodes');

    const midPrestigeEdges = svg.append('g').attr('id', 'mid-prestige-edges');
    const midPrestigeNodes = svg.append('g').attr('id', 'mid-prestige-nodes');

    const lowPrestigeEdges = svg.append('g').attr('id', 'low-prestige-edges');
    const lowPrestigeNodes = svg.append('g').attr('id', 'low-prestige-nodes');

    for (let i = 1; i < nodes.length; i++) {
    	node = nodes[i];
    	schoolToCoords.set(fixSchoolName(node[0]), [node[1], node[2]]);
    }

    const networkWidth = document.body.clientWidth / fraction;
	const diff = (document.body.clientWidth / 3) - networkWidth;

	svg.style('height', networkWidth + 70);

	const r = networkWidth * .0125;
	console.log(r)

	const mapX = d3.scaleLinear().domain([154, 677]).range([20, networkWidth]);
	const mapY = d3.scaleLinear().domain([141, 665]).range([20, networkWidth]);

    nodes.shift();
    edges.shift();

    // Left side. 
    highPrestigeNodes.selectAll('circle')
					 .data(nodes, n => n[0])
					 .enter()
					 .append('circle')
					 .attr('id', node => fixSchoolName(node[0]))
					 .attr('cx', node => mapX(parseFloat(node[1])))
					 .attr('cy', node => mapY(parseFloat(node[2])))
					 .attr('r', node => node[0] == highPrestigeSchool ? r + (r/6) : r)
					 .attr('fill', node => node[0] == highPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .attr('stroke', node => node[0] == highPrestigeSchool ? 'white' : 'dimGrey')
					 .attr('stroke-width', node => node[0] == highPrestigeSchool ? .7 : .85);

	highPrestigeEdges.selectAll('line')
					 .data(edges, e => e)
					 .enter()
					 .append('line')
					 .attr('id', edge => fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6]))
					 .attr('x1', edge => mapX(parseFloat(edge[0])))
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])))
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .attr('stroke', edge => edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .attr('stroke-width', edge => edge[4] == 1 ? 1.25 : .5)

	// Right side.
    midPrestigeNodes.selectAll('circle')
					 .data(nodes, n => n[0])
					 .enter()
					 .append('circle')
					 .attr('id', node => fixSchoolName(node[0]))
					 .attr('cx', node => mapX(parseFloat(node[1])) + diff + networkWidth)
					 .attr('cy', node => mapY(parseFloat(node[2])))
					 .attr('r', node => node[0] == midPrestigeSchool ? r + (r/6) : r)
					 .attr('fill', node => node[0] == midPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .attr('stroke', node => node[0] == midPrestigeSchool ? 'white' : 'dimGrey')
					 .attr('stroke-width', node => node[0] == midPrestigeSchool ? .7 : .85);

	midPrestigeEdges.selectAll('line')
					 .data(edges, e => e)
					 .enter()
					 .append('line')
					 .attr('id', edge => fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6]))
					 .attr('x1', edge => mapX(parseFloat(edge[0])) + diff + networkWidth)
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])) + diff + networkWidth)
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .attr('stroke', edge => edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .attr('stroke-width', edge => edge[4] == 1 ? 1.25 : .5)

	// Right side.
    lowPrestigeNodes.selectAll('circle')
					 .data(nodes, n => n[0])
					 .enter()
					 .append('circle')
					 .attr('id', node => fixSchoolName(node[0]))
					 .attr('cx', node => mapX(parseFloat(node[1])) + (diff * 2) + (networkWidth * 2))
					 .attr('cy', node => mapY(parseFloat(node[2])))
					 .attr('r', node => node[0] == lowPrestigeSchool ?  r + (r/6) : r)
					 .attr('fill', node => node[0] == lowPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .attr('stroke', node => node[0] == lowPrestigeSchool ? 'white' : 'dimGrey')
					 .attr('stroke-width', node => node[0] == lowPrestigeSchool ? .7 : .85);

	lowPrestigeEdges.selectAll('line')
					 .data(edges, e => e)
					 .enter()
					 .append('line')
					 .attr('id', edge => fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6]))
					 .attr('x1', edge => mapX(parseFloat(edge[0])) + (diff * 2) + (networkWidth * 2))
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])) + (diff * 2) + (networkWidth * 2))
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .attr('stroke', edge => edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .attr('stroke-width', edge => edge[4] == 1 ? 1.25 : .5);

	const key = svg.append('g');

    key.append('circle')
       .attr('id', 'sourceCircle')
       .attr('fill', sourceCol)
       .attr('r', 5.5)
       .attr('cx', networkWidth * 1.4)
       .attr('cy', networkWidth + 40);

    key.append('text')
       .attr('id', 'sourceText')
       .attr('x',  networkWidth * 1.4 + 15)
       .attr('y', networkWidth + 45)
       .style('font-family', 'Helvetica')
       .style('font-size', 14)
       .text('Source institution');

    key.append('circle')
       .attr('id', 'infectedCircle')
       .attr('fill', '#2b2b2b')
       .attr('r', 5.5)
       .attr('cx', networkWidth * 2.2 - 10)
       .attr('cy', networkWidth + 40);

    key.append('text')
       .attr('id', 'infectedText')
       .attr('x', networkWidth * 2.2 + 5)
       .attr('y', networkWidth + 45)
       .style('font-family', 'Helvetica')
       .style('font-size', 14)
       .text('Infected universities');

	setTimeout(() => {
		animateEpidemic(epidemics);
	}, 250);

});

function draw(redraw) {
	nodes = globalNodes;
	edges = globalEdges;
	epidemics = globalEpidemics;

	const networkWidth = document.body.clientWidth / fraction;
	const diff = (document.body.clientWidth / 3) - networkWidth;
	const r = networkWidth * .0125;

	svg.style('height', networkWidth + 70);

	const mapX = d3.scaleLinear().domain([154, 677]).range([20, networkWidth]);
	const mapY = d3.scaleLinear().domain([141, 665]).range([20, networkWidth]);

    nodes.shift();
    edges.shift();

    const highPrestigeEdges = svg.select('#high-prestige-edges');
    const highPrestigeNodes = svg.select('#high-prestige-nodes');

    const midPrestigeEdges = svg.select('#mid-prestige-edges');
    const midPrestigeNodes = svg.select('#mid-prestige-nodes');

    const lowPrestigeEdges = svg.select('#low-prestige-edges');
    const lowPrestigeNodes = svg.select('#low-prestige-nodes');

    // Left side. 
    highPrestigeNodes.selectAll('circle')
					 .data([])
					 .exit()
					 .style('cx', node => mapX(parseFloat(node[1])))
					 .style('cy', node => mapY(parseFloat(node[2])))
					 .style('r', node => node[0] == highPrestigeSchool ? r + (r/6) : r)
					 .style('fill', node => redraw ? highPrestigeNodes.select('#' + fixSchoolName(node[0])).style('fill') : 
					 								 node[0] == highPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .style('stroke', node => redraw ? highPrestigeNodes.select('#' + fixSchoolName(node[0])).style('stroke') :
					 						  node[0] == highPrestigeSchool ? 'white' : 'dimGrey')
					 .style('stroke-width', node => node[0] == highPrestigeSchool ? .7 : .85);

	highPrestigeEdges.selectAll('line')
					 .data([])
					 .exit()
					 .attr('x1', edge => mapX(parseFloat(edge[0])))
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])))
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .style('stroke', edge => redraw ? highPrestigeEdges.select('#' + fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6])).style('stroke') :
					 				  	      edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .style('stroke-width', edge => edge[4] == 1 ? 1.25 : .5)

	// Right side.
    midPrestigeNodes.selectAll('circle')
					 .data([])
					 .exit()
					 .style('cx', node => mapX(parseFloat(node[1])) + diff + networkWidth)
					 .style('cy', node => mapY(parseFloat(node[2])))
					 .style('r', node => node[0] == midPrestigeSchool ? r + (r/6) : r)
					 .style('fill', node => redraw ? midPrestigeNodes.select('#' + fixSchoolName(node[0])).style('fill') : 
					 								 node[0] == midPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .style('stroke', node => redraw ? midPrestigeNodes.select('#' + fixSchoolName(node[0])).style('stroke') :
					 						  node[0] == midPrestigeSchool ? 'white' : 'dimGrey')
					 .style('stroke-width', node => node[0] == midPrestigeSchool ? .7 : .85);

	midPrestigeEdges.selectAll('line')
					 .data([])
					 .exit()
					 .attr('x1', edge => mapX(parseFloat(edge[0])) + diff + networkWidth)
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])) + diff + networkWidth)
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .style('stroke', edge => redraw ? midPrestigeEdges.select('#' + fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6])).style('stroke') :
					 				  	      edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .style('stroke-width', edge => edge[4] == 1 ? 1.25 : .5)

	// Right side.
    lowPrestigeNodes.selectAll('circle')
					 .data([])
					 .exit()
					 .style('cx', node => mapX(parseFloat(node[1])) + (diff * 2) + (networkWidth * 2))
					 .style('cy', node => mapY(parseFloat(node[2])))
					 .style('r', node => node[0] == lowPrestigeSchool ?  r + (r/6) : r)
					 .style('fill', node => redraw ? lowPrestigeNodes.select('#' + fixSchoolName(node[0])).style('fill') : 
					 								 node[0] == lowPrestigeSchool ? sourceCol : 'rgb(250, 250, 250)')
					 .style('stroke', node => redraw ? lowPrestigeNodes.select('#' + fixSchoolName(node[0])).style('stroke') :
					 						  node[0] == lowPrestigeSchool ? 'white' : 'dimGrey')
					 .style('stroke-width', node => node[0] == lowPrestigeSchool ? .7 : .85);

	lowPrestigeEdges.selectAll('line')
					 .data([])
					 .exit()
					 .attr('x1', edge => mapX(parseFloat(edge[0])) + (diff * 2) + (networkWidth * 2))
					 .attr('y1', edge => mapY(parseFloat(edge[1])))
					 .attr('x2', edge => mapX(parseFloat(edge[2])) + (diff * 2) + (networkWidth * 2))
					 .attr('y2', edge => mapY(parseFloat(edge[3])))
					 .style('stroke', edge => redraw ? lowPrestigeEdges.select('#' + fixSchoolName(edge[5]) + '-' + fixSchoolName(edge[6])).style('stroke') :
					 				  	      edge[4] == 1 ? mstEdgeCol : edgeCol)
					 .style('stroke-width', edge => edge[4] == 1 ? 1.25 : .5);

	svg.select('#sourceCircle')
       .style('cx', networkWidth * 1.4)
       .style('cy', networkWidth + 40);

    svg.select('#sourceText')
       .attr('x',  networkWidth * 1.4 + 15)
       .attr('y', networkWidth + 45);

    svg.select('#infectedCircle')
       .style('cx', networkWidth * 2.2 - 10)
       .style('cy', networkWidth + 40);

    svg.select('#infectedText')
       .attr('x', networkWidth * 2.2 + 5)
       .attr('y', networkWidth + 45);

	if(!redraw) {
		setTimeout(() => {
			animateEpidemic(epidemics);
		}, 250);
	}
}

function animateEpidemic(epidemics) {
	let highPrestigeEpidemic, midPrestigeEpidemic, lowPrestigeEpidemic;
	const p = .075;

	for (let i = 0; i < epidemics.length; i++) { 
		const epidemic = epidemics[i];
		if (epidemic.p == p && epidemic.source_inst == highPrestigeSchool) {
			highPrestigeEpidemic = epidemic;
		}
		else if (epidemic.p == p && epidemic.source_inst == midPrestigeSchool) {
			midPrestigeEpidemic = epidemic;
		}
		else if (epidemic.p == p && epidemic.source_inst == lowPrestigeSchool) {
			lowPrestigeEpidemic = epidemic;
		}
	}

	const highPrestigeEdges = svg.select('#high-prestige-edges');
    const highPrestigeNodes = svg.select('#high-prestige-nodes');

    const midPrestigeEdges = svg.select('#mid-prestige-edges');
    const midPrestigeNodes = svg.select('#mid-prestige-nodes');

    const lowPrestigeEdges = svg.select('#low-prestige-edges');
    const lowPrestigeNodes = svg.select('#low-prestige-nodes');

    for (let i = -1; i < 5; i++) {
    	setTimeout(() => {
    		if (i >= 0) {
	    		for (let j = 0; j < highPrestigeEpidemic.path.length; j++) {
	    			entry = highPrestigeEpidemic.path[j];
	    			if (entry.timestep == i && entry.source != null) {
	    				const src = fixSchoolName(entry.source);
	    				const target = fixSchoolName(entry.target);

	    				highPrestigeNodes.select('#' + target)
	    								 .transition()
	    								 .duration(fadeIn)
			 							 .ease(d3.easeLinear)
	    								 .style('fill', entry.target == highPrestigeSchool ? sourceCol : lightUp)
	    								 .style('stroke', 'white');

	    				const edge = highPrestigeEdges.select('#' + src + '-' + target);
	    				edge.moveToFront();
	    				const totalLength = dist(schoolToCoords.get(src)[0], schoolToCoords.get(src)[1],
	    										 schoolToCoords.get(target)[0], schoolToCoords.get(target)[1]);

	    				edge.style("stroke-dasharray", totalLength + " " + totalLength)
  							.style("stroke-dashoffset", totalLength)
  							.style('stroke', lightEdge)
	    					.style('stroke-width', .6)
							.transition()
							.duration(fadeIn + 200)
							.ease(d3.easeLinear)
	    					.style("stroke-dashoffset", 0);

	    			}
	    		}
	    		for (let j = 0; j < midPrestigeEpidemic.path.length; j++) {
	    			entry = midPrestigeEpidemic.path[j];
	    			if (entry.timestep == i && entry.source != null) {
	    				const src = fixSchoolName(entry.source);
	    				const target = fixSchoolName(entry.target);

	    				midPrestigeNodes.select('#' + fixSchoolName(entry.target))
	    								.transition()
	    								.duration(fadeIn)
			 							.ease(d3.easeLinear)
	    								.style('fill', entry.target == midPrestigeSchool ? sourceCol : lightUp)
	    								.style('stroke', 'white');

	    				const edge = midPrestigeEdges.select('#' + src + '-' + target);
	    				edge.moveToFront();
	    				const totalLength = dist(schoolToCoords.get(src)[0], schoolToCoords.get(src)[1],
	    										 schoolToCoords.get(target)[0], schoolToCoords.get(target)[1]);

	    				edge.style("stroke-dasharray", totalLength + " " + totalLength)
  							.style("stroke-dashoffset", totalLength)
  							.style('stroke', lightEdge)
	    					.style('stroke-width', .6)
							.transition()
							.duration(fadeIn + 200)
							.ease(d3.easeLinear)
	    					.style("stroke-dashoffset", 0);

	    			}
	    		}
	    		for (let j = 0; j < lowPrestigeEpidemic.path.length; j++) {
	    			entry = lowPrestigeEpidemic.path[j];
	    			if (entry.timestep == i && entry.source != null) {
	    				const src = fixSchoolName(entry.source);
	    				const target = fixSchoolName(entry.target);

	    				lowPrestigeNodes.select('#' + fixSchoolName(entry.target))
	    								.transition()
	    								.duration(fadeIn)
			 							.ease(d3.easeLinear)
	    								.style('fill', entry.target == lowPrestigeSchool ? sourceCol : lightUp)
	    								.style('stroke', 'white');

	    				const edge = lowPrestigeEdges.select('#' + src + '-' + target);
	    				edge.moveToFront();
	    				const totalLength = dist(schoolToCoords.get(src)[0], schoolToCoords.get(src)[1],
	    										 schoolToCoords.get(target)[0], schoolToCoords.get(target)[1]);

	    				edge.style("stroke-dasharray", totalLength + " " + totalLength)
  							.style("stroke-dashoffset", totalLength)
  							.style('stroke', lightEdge)
	    					.style('stroke-width', .6)
							.transition()
							.duration(fadeIn + 200)
							.ease(d3.easeLinear)
	    					.style("stroke-dashoffset", 0);
	    			}
	    		}
	    	}
    	}, (i+1) * 1200);

    	if (i == 4) {
    		setTimeout(() => {
    			draw(false);
    		}, (i+2) * 1200);
    	}
    }
}

function getNode(name) {
	for (let i = 0; i < globalNodes.length; i++) {
		const node = globalNodes[i];
		if (node[0] == name) {
			return node;
		}
	}
}


d3.selection.prototype.moveToFront = function() {
	return this.each(function(){
		this.parentNode.appendChild(this);
	});
};

function fixSchoolName(school) {
	if (school == null) {
		return '';
	}
	return replaceAll(replaceAll(replaceAll(school, ' ', ''), '&', ''), ',', '');
}

function replaceAll(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function diff (num1, num2) {
  if (num1 > num2) {
    return (num1 - num2);
  } else {
    return (num2 - num1);
  }
};

function dist (x1, y1, x2, y2) {
  var deltaX = diff(x1, x2);
  var deltaY = diff(y1, y2);
  var dist = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));
  return (dist);
};