// True is for red corner, False is for blue corner
// NOTE this function expects a consistent html structure
// and is based on the existance of a 'class named corner' on
// both fighter corners. updating that html may require an update
// of this function

RED_CORNER = true;
BLUE_CORNER = false;

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
    clear_fighter_info(corner);
    // use jQuery to extract the data via selectpicker from evt.target
    // which is an object menu
    var gender_val = $(evt.target).selectpicker('val');
    var reverse_val = $(reverse_sel[_gender]).selectpicker('val');

    // gender menu
    if ((gender_val !== reverse_val && reverse_val != "") &&
      (gender_val != "Gender" && reverse_val != "Gender")) {
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
        ui_set_promotion_by_gender(!corner, gender_val.toLowerCase());
      } else {
        clear_fighter_selection(corner);
        return;
      }
    } // end of gender_menu
    
    ui_apply_gender_filter(corner, gender_val.toLowerCase());
    ui_set_promotion_by_gender(corner, gender_val.toLowerCase());
    return;
  }

  // promotion menu
  if (evt.target.classList.contains("promotion_menu")) {
    console.log(corner_name + ", promotion menu selected");

    var side = 99;
    
    if( corner === RED_CORNER ) {
    side = 0;
    } else {
    side = 1;
    }

    var gender_sel = $('.corner')[side].getElementsByTagName('select');
    var gender_val = $( gender_sel[_gender] ).selectpicker('val').toLowerCase();

    clear_fighter_info(corner);

    var gender_sel = $('.corner')[side].getElementsByTagName('select');
    var gender_val = $( gender_sel[_gender] ).selectpicker('val').toLowerCase();    
    var promotion_val = $(evt.target).selectpicker('val');
    ui_apply_promotion_filter(corner, promotion_val, gender_val);
    ui_set_weight_by_promotion(corner, promotion_val, gender_val);
    return;
  } // end of promotion_menu

  // weight menu
  if (evt.target.classList.contains("weight_menu")) {
    console.log(corner_name + ", weight menu selected");

    clear_fighter_info(corner);
 
    var side = 99;
    
    if( corner === RED_CORNER ) {
    side = 0;
    } else {
    side = 1;
    }

    var gender_sel = $('.corner')[side].getElementsByTagName('select');
    var gender_val = $( gender_sel[_gender] ).selectpicker('val').toLowerCase();
    var weight_val = $(evt.target).selectpicker('val');
    var promotion_sel = $('.corner')[side].getElementsByTagName('select');
    var promotion_val = $( promotion_sel[_promotion] ).selectpicker('val');    
    ui_apply_weight_filter(corner, weight_val, gender_val, promotion_val);
    return;
  } // end of weight_menu

  // fighter menu
  if (evt.target.classList.contains("fighter_menu")) {
    console.log(corner_name + ", fighter menu selected");

    var fighter_val = $(evt.target).selectpicker('val');
    ui_load_fighter_info(corner, fighter_val);
    return;
  } // end of fighter_menu

  // error catch in case above code fails or doesn't work properly
  console.log(corner_name + ", something changes, can't say what");
  return;
}

// clear all dropdown menus in corner
function clear_fighter_selection(corner) {
  // clear gender
 
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
  
  // reset menus
  var gender_sel = $('.corner')[side].getElementsByTagName('select');
  $( gender_sel[_gender] ).selectpicker('val', '');
  $( gender_sel[_promotion] ).selectpicker('val', 'Promotion');
  $( gender_sel[_promotion] ).empty().selectpicker('refresh');
  $( gender_sel[_weight] ).selectpicker('val', 'Weight');
  $( gender_sel[_weight] ).empty().selectpicker('refresh');
  $( gender_sel[_fighter] ).selectpicker('val', 'Fighter');
  $( gender_sel[_fighter] ).empty().selectpicker('refresh');

  clear_fighter_info(corner);
} // end of clear_player_selection

// clear fighter info only
function clear_fighter_info(corner) {
  
  var side = 99;
  
  if( corner === RED_CORNER ) {
  side = 0;
  } else {
  side = 1;
  }

  $('.corner')[side].getElementsByTagName('img')[0].src = "../static/images/Body-1.png";

  var _name = 1;
  var _nickname = 3;
  var _promotion = 5;
  var _weightclass = 7;
  var _record = 9;
  
  // clear fighter info text
  finfo_txt = $('.corner')[side].getElementsByTagName('td');
  finfo_txt[_name].innerHTML = "";
  finfo_txt[_nickname].innerHTML = "";
  finfo_txt[_promotion].innerHTML = "";
  finfo_txt[_weightclass].innerHTML = "";
  finfo_txt[_record].innerHTML = "";
  return;
}

// clear all menus by corner
function reset_corner() {
  $('#red_reset').click(function() {
    clear_fighter_selection(RED_CORNER);
  });
  $('#blue_reset').click(function() {
    clear_fighter_selection(BLUE_CORNER);
  });
}

// clear results panel
function clear_results() {
  var _name = 1;
  var _round = 3;
  var _time = 5;
  var _method = 7;
  result_info = $('#results')[0].getElementsByTagName('td');
  result_info[_name].innerHTML = "";
  result_info[_round].innerHTML = "";
  result_info[_time].innerHTML = "";
  result_info[_method].innerHTML = "";
  return;
}

// clear all menus when reset button is clicked
function reset_all_menus() {
  $('#reset_btn').click(function() {
    clear_fighter_selection(RED_CORNER);
    clear_fighter_selection(BLUE_CORNER);
    clear_results();
  });
}

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
  $(weight_menu_sel).empty().selectpicker('refresh');
  $(weight_menu_sel).selectpicker('val', 'Weight');
  $(fighter_menu_sel).empty().selectpicker('refresh');

  for (var i=0; i<fighters.length; ++i) {
    full_name = fighters[i].last_name + ", " + fighters[i].first_name;
    var opt = document.createElement('option');
    opt.text = full_name;
    opt.setAttribute('data-subtext', fighters[i].weight);
    // add new filtered data
    $(fighter_menu_sel).append(opt).selectpicker('refresh');
  }
}

// populate fighter dropdown based on promotion selection
function ui_apply_promotion_filter(corner, promotion, gender) {

  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _weight_menu = 2;
  var _fighter_menu = 3;
  var fighters = get_fighters_by_promotion(promotion);

  var weight_menu_sel = corners[side].getElementsByTagName('select')[_weight_menu];
  var fighter_menu_sel = corners[side].getElementsByTagName('select')[_fighter_menu]; 
  // clean previous selections
  $(weight_menu_sel).empty();
  $(weight_menu_sel).selectpicker('val', 'Weight');
  $(fighter_menu_sel).empty().selectpicker('refresh');

  for (var i=0; i<fighters.length; ++i) {
    if (promotion === fighters[i].promotion && gender === fighters[i].gender) {
      full_name = fighters[i].last_name + ", " + fighters[i].first_name;
      var opt = document.createElement('option');
      opt.text = full_name;
      opt.setAttribute('data-subtext', fighters[i].weight);
      // add new filtered data
      $(fighter_menu_sel).append(opt).selectpicker('refresh');
    }    
  }
}

// populate fighers based on weight class selection
function ui_apply_weight_filter(corner, weight, gender, promotion) {

  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _fighter_menu = 3;
  var fighter_menu_sel = corners[side].getElementsByTagName('select')[_fighter_menu];
  $(fighter_menu_sel).empty().selectpicker('refresh');

  var fighters = get_fighters_by_weight(weight);

  for (var i=0; i<fighters.length; ++i) {
    if ((fighters[i].gender === gender) && (fighters[i].promotion === promotion)) {
      full_name = fighters[i].last_name + ", " + fighters[i].first_name;
      var opt = document.createElement('option');
      opt.text = full_name;
      opt.setAttribute('data-subtext', fighters[i].weight);
      // add new filtered data
      $(fighter_menu_sel).append(opt).selectpicker('refresh');
    }
  }
}

// set promotions based on gender selection
function ui_set_promotion_by_gender(corner, gender) {
  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _promotion_menu = 1;
  var promotion_sel = corners[side].getElementsByTagName('select')[_promotion_menu];

  var promotions = ["UFC", "Bellator", "One Championship", "World Series of Fighting"];
  var has_wmma = ["UFC", "Bellator", "One Championship"];

  if (gender === "female") {
    $(promotion_sel).empty().selectpicker('refresh');
    for (var i=0; i<has_wmma.length; ++i) {
      $(promotion_sel).append('<option>' + has_wmma[i] + '</option>').selectpicker('refresh');
    }
  } else {
    $(promotion_sel).empty().selectpicker('refresh');
    for (var i=0; i<promotions.length; ++i) {
      $(promotion_sel).append('<option>' + promotions[i] + '</option>').selectpicker('refresh');
    }
  }
}

// set weight classes based on promotion selection
function ui_set_weight_by_promotion(corner, promotion, gender) {
  var corners = $('.corner');
  // 0 is red, 1 is blue
  var side = corner === true ? 0 : 1;
  var _weight_menu = 2;
  var weight_sel = corners[side].getElementsByTagName('select')[_weight_menu];

  var ufc_fweights = ["Strawweight", "Bantamweight"];
  var ufc_mweights = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", 
      "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"];
  var bellator_fweights = ["Strawweight", "Flyweight", "Bantamweight", "Featherweight"];
  var bellator_mweights = ["Bantamweight", "Featherweight", "Lightweight", 
      "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"];
  var onechamp_fweights = ["Atomweight", "Strawweight", "Flyweight", "Bantamweight"];
  var onechamp_mweights = ["Strawweight", "Flyweight", "Bantamweight", "Featherweight", 
      "Lightweight", "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"];
  var wsof_mweights = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", 
      "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"];          

  if (promotion === "Bellator" && gender === "female") {
    for (var i=0; i<bellator_fweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + bellator_fweights[i] + '</option>').selectpicker('refresh');
    }    
  } else if (promotion === "Bellator" && gender === "male") {
    for (var i=0; i<bellator_mweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + bellator_mweights[i] + '</option>').selectpicker('refresh');
    }
  } else if (promotion === "UFC" && gender === "female") {
    for (var i=0; i<ufc_fweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + ufc_fweights[i] + '</option>').selectpicker('refresh');
    }
  } else if (promotion === "UFC" && gender === "male") {
    for (var i=0; i<ufc_mweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + ufc_mweights[i] + '</option>').selectpicker('refresh');
    }
  } else if (promotion === "One Championship" && gender === "female") {
    for (var i=0; i<onechamp_fweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + onechamp_fweights[i] + '</option>').selectpicker('refresh');
    }
  } else if (promotion === "One Championship" && gender === "male") {
    for (var i=0; i<onechamp_mweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + onechamp_mweights[i] + '</option>').selectpicker('refresh');
    }
  } else if (promotion === "World Series of Fighting" && gender === "male") {
    for (var i=0; i<wsof_mweights.length; ++i) {
      // add new filtered data
      $(weight_sel).append('<option>' + wsof_mweights[i] + '</option>').selectpicker('refresh');
    }
  }
}

// load fighter info on selection
function ui_load_fighter_info(corner, name) {

  var side = 99;
  
  if( corner === RED_CORNER ) {
  side = 0;
  } else {
  side = 1;
  }

  $('.corner')[side].getElementsByTagName('img')[0].src = "../static/images/Body-1.png";

  var _name = 1;
  var _nickname = 3;
  var _promotion = 5
  var _weightclass = 7;
  var _record = 9;
  
  var fighters = get_fighters_by_name(name);
  for (var i=0; i<fighters.length; ++i) {
    full_name = fighters[i].last_name + ", " + fighters[i].first_name;
    if (full_name === name) {
      var fighter = fighters[i];
      
      $('.corner')[side].getElementsByTagName('img')[0].src = get_img_path(fighter);
      finfo_txt = $('.corner')[side].getElementsByTagName('td');
      finfo_txt[_name].innerHTML = get_fighter_name(fighter);
      finfo_txt[_nickname].innerHTML = get_fighter_nickname(fighter);
      finfo_txt[_promotion].innerHTML = get_fighter_promotion(fighter);
      finfo_txt[_weightclass].innerHTML = get_weight_class(fighter);
      finfo_txt[_record].innerHTML = get_fighter_record(fighter);
    }
  }
} 
  
$(document).ready(function() {
  $('.corner').change(corner_event_handler);
  reset_all_menus();
  reset_corner();
});