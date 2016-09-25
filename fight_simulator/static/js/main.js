$('#example1').cascadingDropdown('fight'}{

	usePost: true,
	source: '/fights',
	paramName: 'fighter_menu',

    selectBoxes: [
        {
            selector: '.step1',
            selected: '4.3'
        },
        {
            selector: '.step2',
            requires: ['.step1']
        },
        {
            selector: '.step3',
            requires: ['.step1'],
            onChange: function(event, value, requiredValues) {
                // do stuff
 
                // event is the change event object for the current dropdown
                // value is the current dropdown value
                // requiredValues is an object with required dropdown values
                // requirementsMet is a boolean value to indicate if all requirements (including current dropdown having a value) have been met
            }
        }
    ]
});