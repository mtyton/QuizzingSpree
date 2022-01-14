class BaseQuestionRenderer {

    constructor() {
        this.container_id = null;
        this.template_id = null;
        this.numberOfElements = null;
    }

    getNumberOfElements = function() {
        return this.numberOfElements;
    }

    startupClean = function() {
        //$(this.container_id).innerHtml = "";
    }

    getTemplate = function() {
        return $(this.template_id).html();
    }

    addElement = function() {
        var template = this.renderTemplate();
        $(this.container_id).append(template);
        this.numberOfElements += 1;
    }

    renderTemplate = function() {}
}

class QuestionCreatorRenderer extends BaseQuestionRenderer {
    constructor() {
        super();
        this.container_id = "#question-container";
        this.template_id = "#question_template";
        this.numberOfElements = 1;
        this.startupClean();
    }

    renderTemplate = function() {
        var template = this.getTemplate();
        template = template.replaceAll(
            "input_id", `question_${this.numberOfElements}`
        )
        template = template.replaceAll(
            'answer_container_id', `answer_container_${this.numberOfElements}`
        )
        // add answers id
        return template;
    }

}

// TODO - implement multiple answers
// class AnswerCreatorRenderer extends BaseQuestionRenderer {
//     constructor() {
//         super();
//         this.numberOfElements = 1;
//         this.numberOfParentElements = 1;
//         this.container_id = "#answer_container_1";
//         this.template_id = "#answer_template";
//         this.startupClean();
//     }
//
//     getElementId = function () {
//         return ;
//     }
//
//     addElement = function(numberOfParentElements) {
//         this.numberOfParentElements = numberOfParentElements;
//         this.container_id = `#answer_container_${numberOfParentElements}`;
//
//         // go on with rendering
//         var template = this.renderTemplate();
//         $(this.container_id).append(template);
//         this.numberOfElements += 1;
//     }
//
//     renderTemplate = function() {
//         var template = this.getTemplate();
//         template = template.replaceAll(
//             "answer_input",
//             answer_${this.numberOfParentElements}_${this.numberOfElements}_input`
//         )
//         template = template.replaceAll(
//             "answer_check",
//             answer_${this.numberOfParentElements}_${this.numberOfElements}_check`
//         )
//
//         return template;
//     }
//
// }

$(document).ready(function() {
    var questionGenerator = new QuestionCreatorRenderer();
    $("#question-add-btn").click(function() {
        questionGenerator.addElement();
    })

    //var answerGenerator = new AnswerCreatorRenderer();
    //$("#answer-add-btn").click(function() {
    //    answerGenerator.addElement(
    //        questionGenerator.getNumberOfElements()
    //    );
    //})

});
