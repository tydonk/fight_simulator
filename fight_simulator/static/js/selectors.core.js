// True is for red corner, False is for blue corner
// NOTE this function expects a consistent html structure
// and is based on the existance of a 'class named corner' on
// both fighter corners. updating that html may require an update
// of this function

RED_CORNER = true;
BLUE_CORNER = false;

// clear all dropdown menus in corner
function clear_fighter_selection(corner) {
  // clear gender
  var RED_CORNER = true;
  var BLUE_CORNER = false;
  
  var side = 99;
  
  if( corner === RED_CORNER ) {
  side = 0;
  } else {
  side = 1;
  }

  var _gender = 0;
  var _promotion = 1;
  var _weight = 2;
  var _fighter = 3;
  
  // clear fighter info
  var gender_sel = $('.corner')[side].getElementsByTagName('select');
  $( gender_sel[_gender] ).selectpicker('val', 'Gender');
  $( gender_sel[_promotion] ).selectpicker('val', 'Promotion');
  $( gender_sel[_weight] ).selectpicker('val', 'Weight');
  $( gender_sel[_fighter] ).selectpicker('val', 'Fighter');

  // clear the image
  $('.corner')[side].getElementsByTagName('img')[0].src = "../static/images/Body-1.png";

  var _name = 1;
  var _nickname = 3;
  var _weightclass = 5;
  var _record = 7;
  
  // clear fighter info text
  finfo_txt = $('.corner')[side].getElementsByTagName('td');
  finfo_txt[_name].innerHTML = "";
  finfo_txt[_nickname].innerHTML = "";
  finfo_txt[_weightclass].innerHTML = "";
  finfo_txt[_record].innerHTML = "";
} // end of clear_player_selection

// clear fighter info only
function clear_fighter_info(corner) {

  var RED_CORNER = true;
  var BLUE_CORNER = false;
  
  var side = 99;
  
  if( corner === RED_CORNER ) {
  side = 0;
  } else {
  side = 1;
  }

  $('.corner')[side].getElementsByTagName('img')[0].src = "../static/images/Body-1.png";

  var _name = 1;
  var _nickname = 3;
  var _weightclass = 5;
  var _record = 7;
  
  // clear fighter info text
  finfo_txt = $('.corner')[side].getElementsByTagName('td');
  finfo_txt[_name].innerHTML = "";
  finfo_txt[_nickname].innerHTML = "";
  finfo_txt[_weightclass].innerHTML = "";
  finfo_txt[_record].innerHTML = "";
}

// capture menu selection event including which corner is chosen
function which_menu(evt, corner) {

  var corner_name = corner === true ? "red corner" : "blue corner";
  var reverse_side = corner === true ? 1 : 0;

  // array default indexes
  var _gender = 0;
  var _promotion = 1;
  var _weight = 2;
  var _fighter = 3;

  reverse_sel = $('.corner')[reverse_side].getElementsByTagName('select');

  if (evt.target.classList.contains("gender_menu")) {
    console.log(corner_name + ", gender menu selected");
    // use jQuery to extract the data via selectpicker from evt.target
    // which is an object menu
    var gender_val = $(evt.target).selectpicker('val');
    var reverse_val = $(reverse_sel[_gender]).selectpicker('val');

    if (gender_val !== reverse_val && reverse_val != "") {
      // corner is just true and false, so we flip with a negation using '!'
      var ok = confirm(
        "Fighters must be the same gender. Choose 'OK' to erase the " +
        (corner === true ? "blue corner" : "red corner") +
        " selection or choose 'Cancel' to keep the current gender");

      if (true === ok) {
        // apply the filters to the current corner
        clear_fighter_selection(!corner);
        $(reverse_sel[_gender]).selectpicker('val', gender_val);
        ui_apply_gender_filter(!corner, gender_val.toLowerCase());
        ui_set_weight_by_gender(!corner, gender_val.toLowerCase());
      } else {
        clear_fighter_selection(corner);
        return;
      }
    } // end of gender_menu
    ui_apply_gender_filter(corner, gender_val.toLowerCase());
    ui_set_weight_by_gender(corner, gender_val.toLowerCase());
    return;
  }

  if (evt.target.classList.contains("promotion_menu")) {
    console.log(corner_name + ", promotion menu selected");
    return;
  } // end of promotion_menu

  if (evt.target.classList.contains("weight_menu")) {

    var RED_CORNER = true;
    var BLUE_CORNER = false;
    
    var side = 99;
    
    if( corner === RED_CORNER ) {
    side = 0;
    } else {
    side = 1;
    }

    console.log(corner_name + ", weight menu selected");
    var gender_sel = $('.corner')[side].getElementsByTagName('select');
    var gender_val = $( gender_sel[_gender] ).selectpicker('val').toLowerCase();
    var weight_val = $(evt.target).selectpicker('val');
    ui_apply_weight_filter(corner, weight_val, gender_val);
    return;
  } // end of weight_menu

  if (evt.target.classList.contains("fighter_menu")) {
    console.log(corner_name + ", fighter menu selected");

    return;
  } // end of fighter_menu

  console.log(corner_name + ", something changes, can't say what");
  return;
}

// determine which corner is being acted on
function corner_event_handler(evtData) {
  var evt = evtData;

  if (evt.currentTarget.classList.contains("red_side")) {
    // check if the target is gender
    which_menu(evt, RED_CORNER);
    return;
  }

  which_menu(evt, BLUE_CORNER);
  return;

}

// trap on change ( menu option, gender, so that it applies to both corners )

// populate fighter dropdown based on gender selection
function ui_apply_gender_filter(corner, gender) {

  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _promotion_menu = 1;
  var _weight_menu = 2;
  var _fighter_menu = 3;
  var fighters = get_fighters_by_gender(gender);

  var promotion_menu_sel = corners[side].getElementsByTagName('select')[_promotion_menu];
  var weight_menu_sel = corners[side].getElementsByTagName('select')[_weight_menu];
  var fighter_menu_sel = corners[side].getElementsByTagName('select')[_fighter_menu];
  // clean previous selections
  $(promotion_menu_sel).selectpicker('val', 'Promotion');
  $(weight_menu_sel).selectpicker('val', 'Weight');
  $(fighter_menu_sel).empty().selectpicker('refresh');

  for (var i=0; i<fighters.length; ++i) {
    full_name = fighters[i].last_name + ", " + fighters[i].first_name;
    // add new filtered data
    $(fighter_menu_sel).append('<option>' + full_name + '</option>').selectpicker('refresh');
  }
}

// set weight class based on gender selected
function ui_set_weight_by_gender(corner, gender) {

  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _weight_menu = 2;
  var weight_menu_sel = corners[side].getElementsByTagName('select')[_weight_menu];
  var weight_menu_opt = $(weight_menu_sel.options);

  if (gender === "female") {
    $(weight_menu_sel).empty().selectpicker('refresh');
    $(weight_menu_sel).append('<option>Strawweight</option>');
    $(weight_menu_sel).append('<option>Bantamweight</option>').selectpicker('refresh');
    return;
  }
  $(weight_menu_sel).empty().selectpicker('refresh');
  $(weight_menu_sel).append('<option>Flyweight</option>');
  $(weight_menu_sel).append('<option>Bantamweight</option>');
  $(weight_menu_sel).append('<option>Featherweight</option>');
  $(weight_menu_sel).append('<option>Lightweight</option>');
  $(weight_menu_sel).append('<option>Welterweight</option>');
  $(weight_menu_sel).append('<option>Middleweight</option>');
  $(weight_menu_sel).append('<option>Light Heavyweight</option>');
  $(weight_menu_sel).append('<option>Heavyweight</option>').selectpicker('refresh');
  return;
}

// populate fighers based on weight class selection
function ui_apply_weight_filter(corner, weight, gender) {

  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _fighter_menu = 3;
  var fighter_menu_sel = corners[side].getElementsByTagName('select')[_fighter_menu];
  $(fighter_menu_sel).empty().selectpicker('refresh');

  var fighters = get_fighters_by_weight(weight);

  for (var i=0; i<fighters.length; ++i) {
    if (fighters[i].gender === gender) {
      full_name = fighters[i].last_name + ", " + fighters[i].first_name;
      // add new filtered data
      $(fighter_menu_sel).append('<option>' + full_name + '</option>').selectpicker('refresh');
    }
  }  
}

// load fighter info on selection


$(document).ready(function() {
  $('.corner').change(corner_event_handler);
});