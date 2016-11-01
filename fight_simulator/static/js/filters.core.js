// players / get_players()

function get_fighters_by_gender(gender) {
  var fighters = [];
  for (var i=0; i<fighterData.length; i++) {
    if (fighterData[i].gender === gender) {    
      fighters.push(fighterData[i]);
    }
  }
  return fighters;
}

function get_fighters_by_promotion(promotion) {
  var fighters = [];
  for (var i=0; i<fighterData.length; i++) {
    if (fighterData[i].promotion === promotion) {
      fighters.push(fighterData[i]);
    }
  }
  return fighters;
}

function get_fighters_by_weight(weight) {
  var fighters = [];
  for (var i=0; i<fighterData.length; i++) {
    if ((fighterData[i].weight.split(" ")[0]) === "Women" && 
        (fighterData[i].weight.split(" ")[1]) === weight) {
      fighters.push(fighterData[i]);
    } else if (fighterData[i].weight === weight) {
      fighters.push(fighterData[i]);
    }
  }
  return fighters;
}

function get_fighters_by_name(name) {
  var fighters = [];
  for (var i=0; i<fighterData.length; i++) {
    if ((fighterData[i].last_name + ", " + fighterData[i].first_name) === name) {
      fighters.push(fighterData[i]);
    }
  }
  return fighters;
}

// ensure consistency
// this means that we have to validate if fighters can fight each other
// for instance, fighters of different genders can't fight each other
// and so on.

function validate_pairs(red_fighter, blue_fighter) {
  // returns true when it's a valid fight
  // returns false when it's an illegal fight

  // note: syntax for accessing gender field may change
  if( red_fighter === blue_fighter ) {
  return true;
  }
  
  return false;
}

function get_weight_class(fighter) {
  if( fighter.gender === "female" ) {
  return fighter.weight.split(" ")[1];
  }

  return fighter.weight;
}

function get_img_path(fighter) {
  return fighter.fighter_image;
}

function get_fighter_name(fighter) {
  return (fighter.first_name + " " + fighter.last_name);
}

function get_fighter_nickname(fighter) {
  return fighter.nickname;
}

function get_fighter_promotion(fighter) {
  return fighter.promotion;
}

function get_fighter_record(fighter) {
  return (fighter.win + "-" + fighter.loss + "-" + fighter.draw);
}