!function(){

	var jsonfile = "ZoomableSunburst.json";

	var width = 960,
		height = 700,
		radius = (Math.min(width, height) / 2) - 10,
		text_offset = 5,
		duration = 750;

	var x = d3.scale.linear()
		.range([0, 2 * Math.PI]);
		
	var	y = d3.scale.pow()
		.exponent(1.3)
		.domain([0,1])
		.range([0, Math.min(width, height) / 2]);
	// var	y = d3.scale.sqrt()
	// 	.range([0, radius]);

	var color = d3.scale.category20c();
	// function color(d){
	// 	if(d.children){
	// 		var e = d.children.map(color),
	// 			r = d3.hsl(e[0]),
	// 			a = d3.hsl(e[1]);
	// 		return d3.hsl((r.h+a.h)/2, 1.2*r.s, r.l/1.2)
	// 	}
	// 	return d.colour||"#fff"
	// }
	function text_color(d){return .299*d.r+.587*d.g+.114*d.b;}


	var partition = d3.layout.partition()
		.sort(null)
		.value(function(d){return 5.8 - d.depth});



	var arc = d3.svg.arc()
		.startAngle(function(d){return Math.max(0,Math.min(2*Math.PI,x(d.x)));})
		.endAngle(function(d){return Math.max(0,Math.min(2*Math.PI,x(d.x+d.dx)));})
		.innerRadius(function(d){return Math.max(0,d.y?y(d.y):d.y);})
		.outerRadius(function(d){return Math.max(0,y(d.y+d.dy));});

	var svg = d3.select("#vis_text")
		.append("svg")
		.attr("width", width+2*text_offset)
		.attr("height", height+2*text_offset)
		.append("g")
			.attr("transform", "translate("+[width/2+text_offset,height/2+text_offset]+")");

	d3.json(jsonfile,function(error,root){
		if (error) throw error;

		var path = svg.selectAll("path")
			.data(partition.nodes(root));
		path.enter().append("path")
		.attr("id", function(n){return "path-"+n.name})
		.attr("d", arc)
		.attr("fill-rule", "evenodd")
		// .style("fill", color)
		.style("fill", function(d) {return color((d.children?d:d.parent).name);})
		.on("click", click);

		var text = svg.selectAll("text")
			.data(partition.nodes(root));
		var sub = text.enter().append("text")
			.style("fill-opacity", 1)
			.style("fill",function(d){return text_color(d3.rgb(color((d.children?d:d.parent).name)))<125?"#eee":"#000"})
			.attr("text-anchor",function(d){return x(d.x+d.dx/2)>Math.PI?"end":"start"})
			.attr("dy",".2em")
			.attr("transform",text_transform)
			.on("click", click)
		sub.append("tspan")
		.attr("x",0)
		.text(function(t){return t.depth?t.name.split(" ")[0]:""});
		sub.append("tspan")
		.attr("x",0)
		.attr("dy","1em")
		.text(function(t){return t.depth?t.name.split(" ")[1]||"":""})


		function click(d){
			path.transition().duration(duration)
			.attrTween("d",tw(d))
			text.transition().duration(duration)
			.attrTween("text-anchor",function(t){return function(){return x(t.x+t.dx/2)>Math.PI?"end":"start"}})
			.attrTween("transform",function(d){
				var n=(d.name||"").split(" ").length>1;
				return function(){
					var e=180*x(d.x+d.dx/2)/Math.PI-90,
						r=e+(n?-.5:0);
					return "rotate("+r+")translate("+(y(d.y)+5)+")rotate("+(e>90?-180:0)+")"
					}
			})
			.style("visibility",function(e){return t(d,e)?null:d3.select(this).style("visibility")})
			.style("fill-opacity",function(e){return t(d,e)?1:1e-6})
			.each("end",function(e){d3.select(this).style("visibility",t(d,e)?null:"hidden")})
		}
	});
	
	function tw(d){
		var xd = d3.interpolate(x.domain(),[d.x,d.x+d.dx]),
			// yd = d3.interpolate(y.domain(),[d.y,rotate(d)]),
			yd = d3.interpolate(y.domain(),[d.y,1]),
			yr = d3.interpolate(y.range(),[d.y?20:0,radius]);
		return function(d){return function(n){return x.domain(xd(n)),y.domain(yd(n)).range(yr(n)),arc(d)}}
	}

	function t(d,e){
		return d==e?!0:d.children?d.children.some(function(d){return t(d,e)}):!1;
	}

	function rotate(d){
		return d.children?Math.max.apply(Math,d.children.map(rotate)):d.y+d.dy;
	}

	function text_transform(d){
		var text_length = (d.name||"").split(" ").length,
			e = 180*x(d.x+d.dx/2)/Math.PI-90,
			r = e+(text_length>1?-.5:0);
		return "rotate("+r+")translate("+(y(d.y)+text_offset)+")rotate("+(e>90?-180:0)+")";
	}
}();