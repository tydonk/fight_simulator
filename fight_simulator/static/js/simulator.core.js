// Simulate matchup between two fighters
// when the 'Fight' button is pressed

function simulate_fight() {
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

	if (validate_pairs(red_fighter[0].id, blue_fighter[0].id)) {
		$('#illegal_alert').show();
		console.log("fight is illegal");
		return;
	}
	console.log("fight permitted");
	$('#illegal_alert').hide();

	var red_calc_perc = ((red_fighter[0].win) + (red_fighter[0].draw * .5)) / 
		(red_fighter[0].win + red_fighter[0].loss + red_fighter[0].draw);
	var red_win_percent = Math.round((red_calc_perc * 100));	


	var blue_calc_perc = ((blue_fighter[0].win) + (blue_fighter[0].draw * .5)) / 
		(blue_fighter[0].win + blue_fighter[0].loss + blue_fighter[0].draw);
	var blue_win_percent = Math.round((blue_calc_perc * 100));

	if (red_win_percent > blue_win_percent) {
		console.log("RED CORNER WINS");
		$('#win_name').html(red_fighter[0].first_name + " " + red_fighter[0].last_name);
	} else {
		console.log("BLUE CORNER WINS");
		$('#win_name').html(blue_fighter[0].first_name + " " + blue_fighter[0].last_name);
	}
}

$(document).ready(function() {
	$('#illegal_alert').hide();
	$('#fight').on('click', function() {	
		simulate_fight();
	});
});