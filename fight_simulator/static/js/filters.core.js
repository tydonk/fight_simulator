// Functions to get fighters by different properties

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
