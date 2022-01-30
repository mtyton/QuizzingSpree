
function extractNumberFromID(id) {
    // Simply extract question number from given question id
    return parseInt(id.split('-')[2])
}

function switchQuestion(change, currID) {
    /**
    Simply switches question to previous/next
    **/
    var questionID = currID,
        number = extractNumberFromID(questionID);

    number += change;

    $(questionID).addClass("visually-hidden");
    questionID = `#container-question-${number}`

    if($(questionID).length != 0) {
        $(questionID).removeClass("visually-hidden");
        $("#next-question").parent().removeClass("disabled");
        $("#summary").addClass("visually-hidden");
    }
    else {
        $("#summary").removeClass("visually-hidden");
        $("#next-question").parent().addClass("disabled");
    }

    //handle button disabling
    if(number <= 1) {
        $("#prev-question").parent().addClass("disabled");
    }
    else {
        $("#prev-question").parent().removeClass("disabled");
    }

    return questionID;

}


$(document).ready(function() {
    /**
   Binding methods, additional initial operations.
    */
    let currentQuestionID = "#container-question-0";

    currentQuestionID = switchQuestion(1, currentQuestionID);

    $("#next-question").click(
        function() {
            currentQuestionID = switchQuestion(1, currentQuestionID);
        }
    )


    $("#prev-question").click(
        function() {
            currentQuestionID = switchQuestion(-1, currentQuestionID);
        }
    )

});