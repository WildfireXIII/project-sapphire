<?php
//***************************************************************************
//
//  File: index.php
//  Date created: 07/29/2018
//  Date edited: 08/09/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Home page
//
//***************************************************************************

include_once('../includes/utility.php');
include_once('../templates/header.php');
include_once('../templates/footer.php');


getHeader("Sapphire");

?>


<p><a href="feed.php">Feed</a></p>


<p><a href="https://github.com/WildfireXIII/project-sapphire">https://github.com/WildfireXIII/project-sapphire</a></p>


<h1>Server Status</h1>

<?php

// get data
$lastContentScrape = getLastContentScrape();
$lastFeedScrape = getLastFeedScrape();
$articleCount = getArticleContentCount();
$totalSpace = getSpaceUtilization();

?>
<p>Last content scrape: <?php echo($lastContentScrape); ?></p>
<p>Last feed scrape: <?php echo($lastFeedScrape); ?></p>
<p>articles: <?php echo($articleCount); ?></p>
<p>space: <?php echo($totalSpace); ?></p>



<svg id="graph" width="960", height="500"></svg>
</br>
</br>


<div id='stats_box'>
	<h2>Execution Units</h2>
	<?php 
		$units = getExecutionUnits();
		
		foreach ($units as $name => $info)
		{
			echo("<p><b>Unit '" . $name . "'</b></p>");
			echo("<ul>");
			echo("<li>Status: " . $units[$name]["status"] . "</li>");
			echo("<li>Last Schedule Poll: " . $units[$name]["lastpoll"] . "</li>");
			echo("</ul>");
		}
	?>
</div>

<script>

var svg = d3.select("#graph");
var margin = {top: 20, right: 20, bottom: 30, left: 50};
var width = +svg.attr("width") - margin.left - margin.right;
var height = +svg.attr("height") - margin.top - margin.bottom;
var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%s");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });
	
d3.csv("spacestatstimeline.php", function(d) {
	console.log(d);
	//d.date = parseTime(d.date);
	//d.content_store_dir_filecount = +d.content_store_dir_filecount;
	//return d;
	return {
		date: parseTime(d.time),
			value: +d.content_store_dir_filecount
	};

}, function(error, data) {
	if (error) throw error;	

	x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain(d3.extent(data, function(d) { return d.value; }));

	g.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr("class", "axis")
		.call(d3.axisBottom(x).tickFormat(d3.timeFormat("%-m/%-d")))
		//.select(".domain")
		.append("text")
		.attr("class", "axisLabel")
		.attr("y", 25)
		//.attr("dy", ".5em")
		.attr("x", (width / 2))
		.text("Date");
		

	g.append("g")
		.attr("class", "axis")
		.call(d3.axisLeft(y))
		.append("text")
		.attr("class", "axisLabel")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left)
		.attr("dy", "1em")
		.attr("x", 0 - (height / 2))
		.attr("text-anchor", "middle")
		.text("Article Count");

	g.append("path")
		.datum(data)
		.attr("fill", "none")
		.attr("stroke", "steelblue")
		.attr("stroke-linejoin", "round")
		.attr("stroke-linecap", "round")
		.attr("stroke-width", 1.5)
		.attr("d", line);	


	g.selectAll(".dot")
		.data(data)
		.enter().append("circle")
			.attr("class", "dot")
			.attr("cx", function(d, i) { return x(i); })
			.attr("cy", function(d) { return y(d.y); })
			.attr("r", 4);
});

</script>

<?php getFooter(); ?>
