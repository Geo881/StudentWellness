//creates local storage instance for each wellness type
var currentResponses = [0,0,0,0,0,0,0,0];
var previousResponses = null;
var user = null;
var resources = null;
var links = null;
var current = null;

showWheelLRG();

//sets up container and draws large wheel
function showWheelLRG(){
    am4core.ready(function(){

        //load user data; name, previous responses, resources
        user = $("#container1a").data('username');
        previousResponses = $("#container1a").data('responses');
        resources = $("#container1a").data('resources');
	links = $("#container1a").data('links');


	resources = cleanResources();
	links = cleanLinks();
        am4core.useTheme(am4themes_animated);

        //show 1a,b on start, NotSure/Sure hidden on start
        $("#buttonNotSure").hide();
        $("#buttonSure").hide();
        $("#container1a").show();
        $("#container1b").show();

        //hide 2a,b and buttons on start
        $("#container2a").hide();
        $("#container2b").hide();
        $("#containerTooltip").empty();

        //create full container
        var containsAll = am4core.create("container1a", am4core.Container);
        containsAll.width = am4core.percent(100);
        containsAll.height = am4core.percent(100);
        containsAll.layout = "vertical";

            //add container for title
            var containerTitle = containsAll.createChild(am4core.Container);
            containerTitle.width = am4core.percent(100);
            containerTitle.height = am4core.percent(5);
            containerTitle.layout = "vertical";

            //add title
            var titleWheel = containerTitle.createChild(am4core.Label);
            titleWheel.text = "Hello " + user + "! Please Select a Category of Wellness";
            //format text going to title
            titleWheel.fontWeight = 600;
            titleWheel.fill = am4core.color("white");
            titleWheel.align = "center";
            titleWheel.paddingLeft = 10;

            //create container for full wheel
            var containerWheelLRG = containsAll.createChild(am4core.Container);
            containerWheelLRG.width = am4core.percent(100);
            containerWheelLRG.height = am4core.percent(95);
            containerWheelLRG.layout = "vertical";
        //___________________________________________________________________________________________________________________________________________________________________________________

            //create large wheel, active based on which wellness type has gotten a response, based on currentResponses[], click slice redirects to smallwheel/slice
            function addPieChartLRG(data){

                //var chart = containerWheelLRG.createChild(am4charts.PieChart);
                var chart = containerWheelLRG.createChild(am4charts.PieChart3D);
                chart.data = data;

                //FORMATTING
                //var pieSeries = chart.series.push(new am4charts.PieSeries());
                var pieSeries = chart.series.push(new am4charts.PieSeries3D());
                pieSeries.dataFields.value = "part";
                pieSeries.dataFields.category = "category";
                pieSeries.slices.template.stroke = am4core.color("black");
                pieSeries.slices.template.strokeWidth = 2;
                pieSeries.slices.template.strokeOpacity = 1;
                pieSeries.slices.template.propertyFields.fill = "color";

                //Disabling labels and ticks on inner circle
                pieSeries.ticks.template.disabled = true;
                pieSeries.alignLabels = false;
                pieSeries.labels.template.text = "{category}";
                pieSeries.labels.template.radius = am4core.percent(-60);
                pieSeries.labels.template.fill = am4core.color("white");
                pieSeries.labels.template.relativeRotation = 90;

                // Disable sliding out of slices
                pieSeries.slices.template.states.getKey("active").properties.shiftRadius = 0.10;
                pieSeries.slices.template.states.getKey("hover").properties.scale = 1.1;

                //set is active
                pieSeries.slices.template.propertyFields.isActive = "pulled";

                //checks current responses to see which sectors have been answered
                for(var i = 0; i<8; i++){
                    if(currentResponses[i] != 0){
                        chart.data[i]["pulled"] = true;
                    }
                }

                //adding tooltips
                pieSeries.tooltip.label.disabled = true;
                pieSeries.slices.template.events.on("over", over);
                pieSeries.slices.template.events.on("out", out);

                    //shows tooltip on hover
                    function over(ev){
                        $("#containerTooltip").empty();
                        //sets current slice as active
                        switch(ev.target.dataItem.category){
                                case "Social":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to relate to and connect with other people.  It is the ability to establish and maintain positive relationships with family, friends and co-workers.");
                                    break;
                                case "Physical":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to maintain a healthy quality of life that allows for engaging in daily activities without undue fatigue or physical stress.  It is the ability to recognize that behaviors have a significant impact on wellness, and to adopt healthful habits while avoiding destructive behaviors.");
                                    break;
                                case "Intellectual":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to open our minds to new ideas and experiences that can be applied to personal decisions, group interaction and community improvement.  It is the desire to learn new concepts, improve skills and seek challenges in pursuit of lifelong learning.");
                                    break;
                                case "Financial":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to maintain wellness through the availability to monetary goods.  Financial wellness is a balance of the mental, spiritual, and physical aspects of money.");
                                    break;
                                case "Spiritual":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to establish peace and harmony in our own lives.  There exists congruency between values and actions, and a realization of purpose.");
                                    break;
                                case "Emotional":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The ability to cope with the challenges of life.  The ability to acknowledge and share feelings of anger, fear, sadness, or stress, as well as hope, love, joy and happiness in a productive manner.");
                                    break;
                                case "Environmental":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": The willingness to recognize our ability to make a positive impact on the quality of our environment, be it our homes, our communities or our planet.  Environmental wellness relies on having safety and security within the environment.");
                                    break;
                                case "Occupational":
                                    var displayText = $("<p></p>").text(ev.target.dataItem.category + ": To have personal fulfillment from our jobs or our endeavors while still maintaining balance in our lives.  It is a desire to attribute meaning to our endeavors, making a positive impact on the organizations we engage in.");
                                    break;
                        };
                        $("#containerTooltip").append(displayText);
                    }

                    //hides tooltip when hover ends
                    function out(ev){
                        $("#containerTooltip").empty();
                    }

                    //listens for click on slices, sets current
                pieSeries.slices.template.events.on("hit", function(ev){
                    //set current
                    current = ev.target.dataItem.category;
                    containsAll.dispose();
                    showWheelSML();
                });
            }
        //_______________________________________________________________________________________________________________

        //add large wheel
            addPieChartLRG([{
                "category": "Social",
                "part": 12.5,
                "color": am4core.color("#FD51BB"),
                "pulled": false
            }, {
                "category": "Physical",
                "part": 12.5,
                "color": am4core.color("#FA7800"),
                "pulled": false
            }, {
                "category": "Intellectual",
                "part": 12.5,
                "color": am4core.color("#FDB81E"),
                "pulled": false
            }, {
                "category": "Financial",
                "part": 12.5,
                "color": am4core.color("#00AF4B"),
                "pulled": false
            }, {
                "category": "Spiritual",
                "part": 12.5,
                "color": am4core.color("#a259f4"),
                "pulled": false
            }, {
                "category": "Emotional",
                "part": 12.5,
                "color": am4core.color("#FF1616"),
                "pulled": false
            }, {
                "category": "Environmental",
                "part": 12.5,
                "color": am4core.color("#A8641E"),
                "pulled": false
            }, {
                "category": "Occupational",
                "part": 12.5,
                "color": am4core.color("#38B6FF"),
                "pulled": false
            }]);
})}

//_____________________________________________________________________________________________________________
//sets up containers and draws small wheel, slice and next button
function showWheelSML(){
    am4core.ready(function(){
        am4core.useTheme(am4themes_animated);

        //hide other containers to start
        $("#container2a").show();
        $("#container2b").show();
        $("#container1a").hide();
        $("#container1b").hide();
        $("#buttonBack").hide();

        //create full container 2
        var containsAll2 = am4core.create("container2a", am4core.Container);
        containsAll2.width = am4core.percent(100);
        containsAll2.height = am4core.percent(100);
        containsAll2.layout = "horizontal";

            //create sub-containers
            //split the top half container
                //create top-left container, holds small wheel
                var containerTopLeft = containsAll2.createChild(am4core.Container);
                containerTopLeft.width = am4core.percent(50);
                containerTopLeft.height = am4core.percent(100);
                containerTopLeft.layout = "vertical";

                //create top-right container, holds slice and back button
                var containerTopRight = containsAll2.createChild(am4core.Container);
                containerTopRight.width = am4core.percent(50);
                containerTopRight.height = am4core.percent(100);
                containerTopRight.layout = "vertical";

                    //create container for label
                    var containerLabel = containerTopRight.createChild(am4core.Container);
                    containerLabel.width = am4core.percent(100);
                    containerLabel.height = am4core.percent(10);
                    containerLabel.layout = "vertical";

		    //add title
		    var titleSlice = containerLabel.createChild(am4core.Label);
		    titleSlice.text = "";
		    titleSlice.fontweight = 600;
		    titleSlice.align = "right";
    		    titleSlice.paddingLeft = 10;

                    //create container for slice and indicator
                    var containerSlice = containerTopRight.createChild(am4core.Container);
                    containerSlice.width = am4core.percent(100);
                    containerSlice.height = am4core.percent(80);
                    containerSlice.layout = "horizontal";
                    //create container for next button
                    var containerNext = containerTopRight.createChild(am4core.Container);
                    containerNext.width = am4core.percent(100);
                    containerNext.height = am4core.percent(10);
                    containerNext.layout = "vertical";
//___________________________________________________________________________________________________________________________________________________________________________________
        //create small wheel, slice click goes back to large wheel, active based on current wellness type
        function addPieChartSML(data){

            var chart = containerTopLeft.createChild(am4charts.PieChart);
            chart.data = data;

            //FORMATTING
            var pieSeries = chart.series.push(new am4charts.PieSeries());
            pieSeries.dataFields.value = "part";
            pieSeries.dataFields.category = "category";
            pieSeries.slices.template.stroke = am4core.color("black");
            pieSeries.slices.template.strokeWidth = 2;
            pieSeries.slices.template.strokeOpacity = 1;
            pieSeries.slices.template.propertyFields.fill = "color";

            // Disabling labels and ticks on inner circle
            pieSeries.ticks.template.disabled = true;
            pieSeries.tooltip.label.disabled = true;
            pieSeries.alignLabels = false;
            pieSeries.labels.template.text = "{category}";
            pieSeries.labels.template.radius = am4core.percent(-72);
            pieSeries.labels.template.fill = am4core.color("white");
            pieSeries.labels.template.relativeRotation = 90;

            // Disable sliding out of slices
            pieSeries.slices.template.states.getKey("hover").properties.shiftRadius = 0;
            pieSeries.slices.template.states.getKey("hover").properties.scale = 1;

            //set is active
            pieSeries.slices.template.propertyFields.isActive = "pulled";

            //sets current slice as active
            switch(current){
                    case "Social":
                        chart.data[0]["pulled"] = true;
                        break;
                    case "Physical":
                        chart.data[1]["pulled"] = true;
                        break;
                    case "Intellectual":
                        chart.data[2]["pulled"] = true;
                        break;
                    case "Financial":
                        chart.data[3]["pulled"] = true;
                        break;
                    case "Spiritual":
                        chart.data[4]["pulled"] = true;
                        break;
                    case "Emotional":
                        chart.data[5]["pulled"] = true;
                        break;
                    case "Environmental":
                        chart.data[6]["pulled"] = true;
                        break;
                    case "Occupational":
                        chart.data[7]["pulled"] = true;
                        break;
            };

            //listens for click on slices, show large wheel
            pieSeries.slices.template.events.on("hit", function(ev){
                containsAll2.dispose();
		$("#container2a").css("pointer-events", "auto");
		$("#containerResources").empty();
                showWheelLRG();
            });
        }
        
        //creates small wheel and slice
        addPieChartSML([{
              "category": "Social",
              "part": 12.5,
                "color": am4core.color("#FD51BB"),
                "pulled": false
        }, {
              "category": "Physical",
              "part": 12.5,
                "color": am4core.color("#FA7800"),
                "pulled": false
        }, {
              "category": "Intellectual",
              "part": 12.5,
                "color": am4core.color("#FDB81E"),
                "pulled": false
        }, {
              "category": "Financial",
              "part": 12.5,
                "color": am4core.color("#00AF4B"),
                "pulled": false
        }, {
              "category": "Spiritual",
              "part": 12.5,
                "color": am4core.color("#a259f4"),
                "pulled": false
        }, {
              "category": "Emotional",
              "part": 12.5,
                "color": am4core.color("#FF1616"),
                "pulled": false
        }, {
              "category": "Environmental",
              "part": 12.5,
                "color": am4core.color("#A8641E"),
                "pulled": false
        }, {
              "category": "Occupational",
              "part": 12.5,
                "color": am4core.color("#38B6FF"),
                "pulled": false
        }]);
//_______________________________________________________________________________________________________________
        //create slice, changes color based on current, clicking segments chnages current response for current wellness type
        function addSlice(data){

            var chart = containerSlice.createChild(am4charts.SlicedChart)
            chart.data = data;

            //formatting
            var series = chart.series.push(new am4charts.PyramidSeries());
            series.dataFields.value = "value";
            series.dataFields.category = "name";
            series.alignLabels = true;
            series.valueIs = "height";
            series.ticks.template.disabled = true;
            series.labels.template.disabled = true;
            series.tooltip.label.disabled = true;
            series.slices.template.propertyFields.fill = "color";
            series.slices.template.stroke = am4core.color("#000");
            series.bottomWidth = am4core.percent(50);

            //adding tooltips
            series.tooltip.label.disabled = true;
            series.slices.template.events.on("over", over);
            series.slices.template.events.on("out", out);

            //shows tooltip on hover
            function over(ev){
                $("#containerResources").empty();
                switch(current){
                    case "Social":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I have friends and prioritize being social to have a balanced personal wellness.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I have a few close friends, but I am looking to expand my social circle and am not sure how to.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I have little to no friends and/or do not prioritize socializing.");
                        }
                        break;
                    case "Physical":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am happy with how I maintain my physical wellness through a balance of nutrition, exercise, and sleep.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I make efforts to physically care for myself via my nutrition, sleep, and/or exercise, but would like to learn more.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am not satisfied with how I physically take care of my body via nutrition, exercise, and/or sleep.");
                        }
                        break;
                    case "Intellectual":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am happy with my academic performance and feel that my current study habits set me up for success.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I do alright by my academics, but I feel I could be doing more or would like more resources.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am struggling in my academics, but do not know where to start.");
                        }
                        break;
                    case "Financial":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I have developed good spending/saving habits, and currently feel secure in my financial wellness.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am okay with finances, but I want to build better spending/saving habits.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am struggling with finances and do not know how to build better financial habits.");
                        }
                        break;
                    case "Spiritual":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am at peace with my spirituality and engage with resources to connect with my community.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am somewhat or not spiritual but would like to learn more.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am at odds with my spirituality, causing unrest.");
                        }
                        break;
                    case "Emotional":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am emotionally well and am in touch with my own emotional needs and resources.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": My emotional wellness is okay, but I’d like to continue to grow.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I feel that my emotional wellness is struggling, and would like a better understanding of resources.");
                        }
                        break;
                    case "Environmental":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": My environment supports my personal wellness and goals the majority of the time.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": Sometimes my environment supports my personal wellness and goals.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I do not feel my environment supports my overall personal wellness.");
                        }
                        break;
                    case "Occupational":
                        if(ev.target.dataItem.category == "Well"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am fulfilled professionally and personally by my occupation and outside activities.");
                        }
                        else if(ev.target.dataItem.category == "Neutral"){
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I like where I am at professionally, but I’d like to continue to grow in my outside activities.");
                        }
                        else{
                        var displayText = $("<p></p>").text(ev.target.dataItem.category + ": I am not happy or fulfilled by my current position or my activities outside of work.");
                        }
                        break;
                }
                $("#containerResources").append(displayText);
            }

            //hides tooltip when hover ends
            function out(ev){
                $("#containerResources").empty();
            }

            //define string for title
            var currString = " ";

            //check if current has been changed, user modified responses this visit
            var curr = parseCurrent();
            if(curr == 3){
                currString = "Not Well";
                titleSlice.text = current + ": You recently chose " + currString;
            }
            else if(curr == 2){
                currString = "Neutral";
                titleSlice.text = current + ": You recently chose " + currString;
            }
            else if(curr == 1){
                currString = "Well";
                titleSlice.text = current + ": You recently chose " + currString;
            }
            else{

                //user has not given responses this visit
                var prev = parsePrevious();
                if(prev == 1){
                    currString = "Well";
                    titleSlice.text = current + ": Your previous response was " + currString;
                }
                else if(prev == 2){
                    currString = "Neutral";
                    titleSlice.text = current + ": Your previous response was " + currString;
                }
                else if(prev == 3){
                    currString = "Not Well";
                    titleSlice.text = current + ": Your previous response was " + currString;
                }
                else{
                    currString = "No Previous Response";
                    titleSlice.text = "No previous selection for this category";
                }
            }

            //format text going to title
            titleSlice.fontWeight = 600;
            titleSlice.align = "left";
            titleSlice.fill = am4core.color("white");
            titleSlice.paddingLeft = 10;

            //change slice color based on current selected slice
            switch(current){
                    case "Social":
                        chart.data[0]["color"] = am4core.color("#fecdeb");
                        chart.data[1]["color"] = am4core.color("#fe9ad8");
                        chart.data[2]["color"] = am4core.color("#FD51BB");
                        break;
                    case "Physical":
                        chart.data[0]["color"] = am4core.color("#ffd7b3");
                        chart.data[1]["color"] = am4core.color("#ffa34d");
                        chart.data[2]["color"] = am4core.color("#FA7800");
                        break;
                    case "Intellectual":
                        chart.data[0]["color"] = am4core.color("#feffb3");
                        chart.data[1]["color"] = am4core.color("#fcff66");
                        chart.data[2]["color"] = am4core.color("#F8FD00");
                        break;
                    case "Financial":
                        chart.data[0]["color"] = am4core.color("#99ffc5");
                        chart.data[1]["color"] = am4core.color("#00ff6e");
                        chart.data[2]["color"] = am4core.color("#00AF4B");
                        break;
                    case "Spiritual":
                        chart.data[0]["color"] = am4core.color("#e4cffc");
                        chart.data[1]["color"] = am4core.color("#c99ff9");
                        chart.data[2]["color"] = am4core.color("#A259F4");
                        break;
                    case "Emotional":
                        chart.data[0]["color"] = am4core.color("#ffb3b3");
                        chart.data[1]["color"] = am4core.color("#ff6666");
                        chart.data[2]["color"] = am4core.color("#FF1616");
                        break;
                    case "Environmental":
                        chart.data[0]["color"] = am4core.color("#e8b37d");
                        chart.data[1]["color"] = am4core.color("#d98026");
                        chart.data[2]["color"] = am4core.color("#A8641E");
                        break;
                    case "Occupational":
                        chart.data[0]["color"] = am4core.color("#ccecff");
                        chart.data[1]["color"] = am4core.color("#80d0ff");
                        chart.data[2]["color"] = am4core.color("#38B6FF");
                        break;
            }

            //sets listener for click
            series.slices.template.events.on("hit", function(ev){

                //create variable to convert slice value to int
                var category = ev.target.dataItem.category;

                if (category == "Well"){
                    var answer = 1;
                }
                else if (category == "Neutral"){
                    var answer = 2;
                }
                else if (category == "Not Well"){
                    var answer = 3;
                }
                else{
                    console.out("something is wrong");
                    var answer = 0;
                }

                //change saved value depending on currently selected slice
                switch(current){
                    case "Social":
                        currentResponses[0] = answer;
                        break;
                    case "Physical":
                        currentResponses[1] = answer;
                        break;
                    case "Intellectual":
                        currentResponses[2] = answer;
                        break;
                    case "Financial":
                        currentResponses[3] = answer;
                        break;
                    case "Spiritual":
                        currentResponses[4] = answer;
                        break;
                    case "Emotional":
                        currentResponses[5] = answer;
                        break;
                    case "Environmental":
                        currentResponses[6] = answer;
                        break;
                    case "Occupational":
                        currentResponses[7] = answer;
                        break;
                }
            });

                //create labels for slice
                //label for Good
                var labelGood = chart.createChild(am4core.Label);
                labelGood.text = "Well";
                labelGood.x = am4core.percent(50);
                labelGood.y = am4core.percent(18);
                labelGood.align = "center";
                //labelGood.fill = am4core.color("white");
                labelGood.horizontalCenter = "middle";
                labelGood.isMeasured = false;

                //label for Neutral
                var labelNeutral = chart.createChild(am4core.Label);
                labelNeutral.text = "Neutral";
                labelNeutral.x = am4core.percent(50);
                labelNeutral.y = am4core.percent(50);
                labelNeutral.isMeasured = false;
                labelNeutral.align = "center";
                //labelNeutral.fill = am4core.color("white");
                labelNeutral.horizontalCenter = "middle";

                //label for Bad
                var labelBad = chart.createChild(am4core.Label);
                labelBad.text = "Not Well";
                labelBad.x = am4core.percent(50);
                labelBad.y = am4core.percent(81);
                labelBad.align = "center";
                //labelBad.fill = am4core.color("white");
                labelBad.horizontalCenter = "middle";
                labelBad.isMeasured = false;
            }
        //add slice
        addSlice([{
                "name": "Well",
                "value": 300,
                "color": am4core.color("#FFFFFF"),
                "pulled": false
            }, {
                "name": "Neutral",
                "value": 300,
                "color": am4core.color("#FFFFFF"),
                "pulled": false
            }, {
                "name": "Not Well",
                "value": 300,
                "color": am4core.color("#FFFFFF"),
                "pulled": false
            }]);
//_______________________________________________________________________________________________________________
            //create next button, under slice, returns resources based on input
            //Query resources/videos from database
            function addNextButton(text){
                var button = containerNext.createChild(am4core.Button);
                button.fill = am4core.color("red");
                button.label.text = text;
                button.align = "center";
                button.marginTop = 5;

                button.events.on("hit", function(){
		    var secondVideo;
                    switch(current){
                        case "Social":
                            if (currentResponses[0] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/VPE9CqRUp54" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[0] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/VPE9CqRUp54" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[0] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/VPE9CqRUp54" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Physical":
                            if (currentResponses[1] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
                            	var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/AEPnYII8uSI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[1] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
                            	var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/AEPnYII8uSI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[1] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
                            	var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/AEPnYII8uSI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
			    }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Intellectual":
                            if (currentResponses[2] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px;"width="400" height="200" src="https://www.youtube.com/embed/c7qSoCoM9i8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[2] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px;"width="400" height="200" src="https://www.youtube.com/embed/c7qSoCoM9i8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[2] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px;"width="400" height="200" src="https://www.youtube.com/embed/c7qSoCoM9i8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Financial":
                            if (currentResponses[3] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/4t5XVFUrljQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[3] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/4t5XVFUrljQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[3] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/4t5XVFUrljQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Spiritual":
                            if (currentResponses[4] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/8gZ_JbDgERs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[4] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/8gZ_JbDgERs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[4] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/8gZ_JbDgERs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Emotional":
                            if (currentResponses[5] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
                            	var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/PAestsXAWsw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[5] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
                            	var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/PAestsXAWsw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[5] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
                            	var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/PAestsXAWsw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
			    }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Environmental":
                            if (currentResponses[6] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/HcXHxSdhpgo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[6] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/HcXHxSdhpgo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[6] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px" width="400" height="200" src="https://www.youtube.com/embed/HcXHxSdhpgo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                        case "Occupational":
                            if (currentResponses[7] == 1){
				titleSlice.text = "Saved response for " + current + ": Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/xSYf8I7j0Cw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[7] == 2){
				titleSlice.text = "Saved response for " + current + ": Neutral";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/xSYf8I7j0Cw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else if (currentResponses[7] == 3){
				titleSlice.text = "Saved response for " + current + ": Not Well";
				var video = $('<div><iframe style="margin-left:850px"width="400" height="200" src="https://www.youtube.com/embed/xSYf8I7j0Cw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
                            }
                            else{
                                var displayText = $("<p></p>").text("Please select a level of wellness. Return to the main wheel and try again.");
                            }
                            break;
                    }
		    $("#container2a").css("pointer-events", "none");
                    printResources();
		    printLinks();
		    $("#containerResources").append(video);
                    $("#buttonBack").show();

                    button.clickable=false;
		   // $("#container2a").css({"pointer-events": "none"});
                });
            }
            //add next button
            addNextButton("Next");
})}

//_______________________________________________________________________________________________________________
            ////parse previous Responses, returns value of currently selected wellness type
            function parsePrevious(){
                var prevResponse = 0;
                switch(current){
                        case "Social":
                            prevResponse = previousResponses[0];
                            break;
                        case "Physical":
                            prevResponse = previousResponses[1];
                            break;
                        case "Intellectual":
                            prevResponse = previousResponses[2];
                            break;
                        case "Financial":
                            prevResponse = previousResponses[3];
                            break;
                        case "Spiritual":
                            prevResponse = previousResponses[4];
                            break;
                        case "Emotional":
                            prevResponse = previousResponses[5];
                            break;
                        case "Environmental":
                            prevResponse = previousResponses[6];
                            break;
                        case "Occupational":
                            prevResponse = previousResponses[7];
                            break;
                    }
                return prevResponse;
            }
//_______________________________________________________________________________________________________________
            //parse current Responses, returns value of currently selected wellness type
            function parseCurrent(){
                var currResponse = 0;
                switch(current){
                        case "Social":
                            currResponse = currentResponses[0];
                            break;
                        case "Physical":
                            currResponse = currentResponses[1];
                            break;
                        case "Intellectual":
                            currResponse = currentResponses[2];
                            break;
                        case "Financial":
                            currResponse = currentResponses[3];
                            break;
                        case "Spiritual":
                            currResponse = currentResponses[4];
                            break;
                        case "Emotional":
                            currResponse = currentResponses[5];
                            break;
                        case "Environmental":
                            currResponse = currentResponses[6];
                            break;
                        case "Occupational":
                            currResponse = currentResponses[7];
                            break;
                    }
                return currResponse;
            }
//_______________________________________________________________________________________________________________
            //for back button, goes back to large wheel
            function goBack(){
                // needs containsAll2.dispose();
                $("#containerResources").empty();
		$("#container2a").css("pointer-events", "auto");
                showWheelLRG();
            }
//_______________________________________________________________________________________________________________
            //checks current responses against last responses
            function firstSubmit(){
                $("#container1a").css({"pointer-events": "none"});
                for(var i = 0; i<8; i++){
                        if(currentResponses[i] == 0){
                            var displayText = $("<p></p>").text("It looks like you didn't give responses for some wellness types. Would you like to go back and give responses before you submit?");
                            break;
                        }
                        else{
                            var displayText = $("<p></p>").text("You've submitted responses for all types of welllness. Are you sure you would like to submit?");
                        }
                    }
                $("#containerTooltip").append(displayText);
                $("#buttonSub").hide();
                $("#buttonSure").show();
                $("#buttonNotSure").show();
                $("#buttonSure").val(currentResponses);
                console.log($("#buttonSure").val());
            }
//___________________________________________________________________________________________
            //allows access back to wheel
            function notSure(){
                    $("#buttonSub").show();
                    $("#buttonSure").hide();
                    $("#buttonNotSure").hide();
                    $("#containerTooltip").empty();
                    $("#container1a").css({"pointer-events": "auto"});
                    var displayText = $("<p></p>").text("Take your time!");
            }
//_____________________________________________________________________
	//cleans resource query, removes extra characters and column names
	    function cleanResources(){
		    resources = $("#container1a").data('resources');
        	    resources = resources.replace(new RegExp("'wellness_type':", "g"), "");
	            resources = resources.replace(new RegExp("'response':", "g"), "");
        	    resources = resources.replace(new RegExp("'message':", "g"), "");
	            resources = resources.replace(new RegExp("{", "g"), "");
		    resources = resources.replace("})", "");
        	    resources = resources.replace("(",  "");
	            resources = resources.replace(")", "");

	            resources = resources.split("},");
	  	    return resources;
	    }

//_______________________________________________________________
	//cleans link query
	    function cleanLinks(){
		    links = $("#container1a").data('links');
		    links = links.replace(new RegExp("'resource_type':", "g"), "");
		    links = links.replace(new RegExp("'label':", "g"), "");
		    links = links.replace(new RegExp("'resource_links':", "g"), "");
                    links = links.replace(new RegExp("{", "g"), "");

		    links = links.split("},");
		    return links;
	    }
//____________________________________________________________________
	//prints resources to resource container
	    function printResources(){

	    	strApost = "'";
                fixCurrent = current.charAt(0).toLowerCase() + current.slice(1);
                strCurrent = strApost + fixCurrent + strApost;

                for(i = 0; i<resources.length; i++){
                       if(resources[i].includes(strCurrent)){
                           thisRes = resources[i].split("',");
                           thisRes[1] = thisRes[1].replace("'", "");
                           thisRes[2] = thisRes[2].replace(new RegExp("'" , "g" ), "");
                           var displayResp = $("<p></p>").text(thisRes[1] + ":");
                           var displayRec = $("<p></p>").text(thisRes[2]);
                            $("#containerResources").append(displayResp, displayRec);
                        }
                }

	    }
//__________________________________________________________________________________
	//prints links
	    function printLinks(){
		strApost = "'";
		fixCurrent = current.charAt(0).toLowerCase() + current.slice(1);
		strCurrent = strApost + fixCurrent + strApost;
		var printWord = $("<p></p>").text("Resource Links:");
		$("#containerResources").append(printWord);
		for(i = 0; i<links.length; i++){
			if(links[i].includes(strCurrent)){
				thisLink = links[i].split("',");
				thisLink[1] = thisLink[1].replace("'", "");
				thisLink[2] = thisLink[2].replace(new RegExp("'","g"), "");
				console.log("thisLink[2]: " + thisLink[2]);
				$("#containerResources").append('<a href = "' + thisLink[2] + '"target = "_blank">' + thisLink[1] + '</a>'); 
			}
		}

	    }
