
class QuestionManager {

    constructor() {
        var me = this;
        me.questions = [new Question("#question_0")]
    }

    getAndRenderQuestionTemplate = function() {
        var me = this,
            template, questionNumber;

        // we should always download first question, because
        // it should be always visible
        template = $(me.questions[0].itemID).html();

        // TODO - change this if we want to allow question deletion
        questionNumber = me.questions.length + 1;
        template = template.replaceAll(
            'question_0', `question_${questionNumber}`
        )
        template = template.replaceAll(
            'questionInput_0', `questionInput_${questionNumber}`
        )
        template = template.replaceAll(
            'question_0_answers', `question_${questionNumber}_answers`
        )
        template = template.replaceAll(
            'add_answer_0', `add_answer_${questionNumber}`
        )
        return template;
    }

    addQuestion = function() {
        var me = this,
            questionWrapper, questionTemplate;

        questionWrapper = $("#question-container")
        questionTemplate = me.getAndRenderQuestionTemplate();
        questionWrapper.append(questionTemplate);
    }

    getAndRenderAnswerTemplate = function (questionNumber, answerBlock) {
        var me = this,
            template, answers, baseAnswerIDSuffix;
        template = $(`#answer_0_0`).html();
        // get block size
        answers = answerBlock.find($(".input-group"));

        // let's create basic answer ID suffix
        baseAnswerIDSuffix = `${questionNumber}_${answers.length+1}`;

        template = template.replaceAll(
            'answer_0_0', `answer_${baseAnswerIDSuffix}`
        )
        template = template.replaceAll(
            'answer_input_0_0', `answer_input_${baseAnswerIDSuffix}`
        )
        template = template.replaceAll(
            'answer_check_0_0', `answer_check_${baseAnswerIDSuffix}`
        )
        return template;
    }

    addAnswerToQuestion = function(questionNumber) {
        var me = this,
            answerBlockID, answerBlock, templateAnswer;

        answerBlockID = `#question_${questionNumber}_answers`;
        answerBlock = $(answerBlockID);
        templateAnswer = me.getAndRenderAnswerTemplate(
            questionNumber, answerBlock
        );
        answerBlock.append(templateAnswer);

    }

}


$(document).ready(function() {
    let questionManager;

    questionManager = new QuestionManager();

    $("#question-add-btn").click(function(event) {
        event.preventDefault();
        questionManager.addQuestion();
    })

    $("#question-container").find('button').click(function(event) {
        var buttonID, questionNumber;
        event.preventDefault();
        // extract question number
        buttonID = this.id;
        questionNumber = buttonID.split("_")[2];
        questionManager.addAnswerToQuestion(questionNumber);
    })


});

