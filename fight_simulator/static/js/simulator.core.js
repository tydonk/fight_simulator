// Simulate matchup between two fighters
// when the 'Fight' button is pressed

// array of possible outcomes
var outcomes = ["Knockout", "Technical Knockout", "Submission", 
			"Doctor Stoppage", "Unanimous Decision", 
			"Split Decision", "Majority Decision"];

var submissions = ["arm triangle", "triangle", "rear naked choke", "guillotine", "gogoplata",
			"arm bar", "kimura", "americana", "omoplata", "knee bar", "ankle lock", "heel hook",
			"toe hold", "can opener", "twister", "achilles lock", "bicep slicer", "leg slicer"];

var rounds = ["1", "2", "3"];			

// get results using random selection from outcomes
function get_random_outcome() {
	var outcome = outcomes[Math.floor(Math.random() * outcomes.length)];
	return outcome;
}

// get random submission
function get_random_submission() {
	var submission = submissions[Math.floor(Math.random() * submissions.length)];
	return submission;
}

// get random time between 0:01 and 4:59
function get_random_time() {
	var minute = Math.floor(Math.random() * ((4-0)+1) + 0);
	var second_1 = Math.floor(Math.random() * ((5-1)+1) + 1);
	var second_2 = Math.floor(Math.random() * ((9-1)+1) + 1);
	var time = (minute + ":" + second_1 + second_2);
	return time;
}

// get random round 1-3
function get_random_round() {
	var round = Math.floor(Math.random() * ((3-1)+1) + 1);
	return round;
}

function clear_results() {
	$('#win_name').html("");
	$('#win_round').html("");
	$('#win_time').html("");
	$('#win_method').html("");
}

function simulate_fight() {
	// empty results panel
	clear_results();

	// get selected fighters name from red corner
	var red_menu_sel = $('.corner')[0].getElementsByTagName('select');
	var _red_fighter = 3;
	var red_fighter_val = $(red_menu_sel[_red_fighter]).selectpicker('val');
	var red_fighter = get_fighters_by_name(red_fighter_val);

	// get selected fighters name from blue corner
	var blue_menu_sel = $('.corner')[1].getElementsByTagName('select');
	var _blue_fighter = 3;
	var blue_fighter_val = $(blue_menu_sel[_blue_fighter]).selectpicker('val');
	var blue_fighter = get_fighters_by_name(blue_fighter_val);

	// check to make sure the fighters are not the same
	if (validate_pairs(red_fighter[0].id, blue_fighter[0].id)) {
		$('#illegal_alert').show();
		console.log("fight is illegal");
		return;
	}
	console.log("fight permitted");
	$('#illegal_alert').hide();

	// calculate win percentage for each fighter
	var red_calc_perc = ((red_fighter[0].win) + (red_fighter[0].draw * .5)) / 
		(red_fighter[0].win + red_fighter[0].loss + red_fighter[0].draw);
	var red_win_percent = Math.round((red_calc_perc * 100));	

	var blue_calc_perc = ((blue_fighter[0].win) + (blue_fighter[0].draw * .5)) / 
		(blue_fighter[0].win + blue_fighter[0].loss + blue_fighter[0].draw);
	var blue_win_percent = Math.round((blue_calc_perc * 100));

	var outcome = get_random_outcome();
	var round = get_random_round();
	var time = get_random_time();
	
	if (red_win_percent > blue_win_percent) {
		console.log("RED CORNER WINS");
		$('#win_name').html(red_fighter[0].first_name + " " + red_fighter[0].last_name);
		if (outcome === "Submission") {
			$('#win_method').html(outcome + " (" + get_random_submission() + ")");
			$('#win_round').html(round);
			$('#win_time').html(time);
		} else if ( (outcome.split(" ")[1]) === "Decision" ) {
			$('#win_round').html("3");
			$('#win_time').html("5:00");
			$('#win_method').html(outcome);
		} else {
			$('#win_method').html(outcome);
			$('#win_round').html(round);
			$('#win_time').html(time);
		}		
	} else {		
		console.log("BLUE CORNER WINS");
		$('#win_name').html(blue_fighter[0].first_name + " " + blue_fighter[0].last_name);
		if (outcome === "Submission") {
			$('#win_method').html(outcome + " (" + get_random_submission() + ")");
			$('#win_round').html(round);
			$('#win_time').html(time);
		} else if ( (outcome.split(" ")[1]) === "Decision" ) {
			$('#win_round').html("3");
			$('#win_time').html("5:00");
			$('#win_method').html(outcome);
		} else {
			$('#win_method').html(outcome);
			$('#win_round').html(round);
			$('#win_time').html(time);
		}		
	}
}

$(document).ready(function() {
	$('#illegal_alert').hide();
	$('#fight').on('click', function() {	
		simulate_fight();
	});
});