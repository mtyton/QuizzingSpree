class BaseTemplateRenderer {

    constructor() {
        var me = this;
        me.valueDict = {};
    }

    fillDictionaries = function(templateID) {

    }

    renderTemplate = function (templateID) {
        var me = this,
            template = $(templateID).html();

        for (var [key, value] of Object.entries(me.valueDict)) {
            template = template.replaceAll(key, value)
        }
        return template
    }

}


class InitialTemplateRenderer extends BaseTemplateRenderer {
    fillDictionaries = function() {
        var me = this;
        me.valueDict = {
            'question_0': 'question_template',
            'questionInput_0': 'questionInput_template',
            'question_0_answers': 'question_template_answers',
            'add_answer_0': 'add_answer_template',
            'questions-0-question_type': 'questions-template-question_type',
            'questions-0-content': 'questions-template-content',
            'answer_0_0': 'answer_template_template',
            'answer_input_0_0': 'answer_input_template_template',
            'answer_check_0_0': 'answer_check_template_template',
            'questions-0-answers-0-correct': 'questions-template-answers-template-correct',
            'questions-0-answers-0-content': 'questions-template-answers-template-content',
        }
    }
}


class QuestionTemplateRenderer extends BaseTemplateRenderer {

    fillDictionaries = function(questionNumber) {
        var me = this;
        me.valueDict = {
            'question_template': `question_${questionNumber}`,
            'questionInput_template': `questionInput_${questionNumber}`,
            'question_template_answers': `question_${questionNumber}_answers`,
            'add_answer_template': `add_answer_${questionNumber}`,
            'questions-template-question_type': `questions-${questionNumber}-question_type`,
            'questions-template-content': `questions-${questionNumber}-content`
        }
    }

}


class AnswerTemplateRenderer extends BaseTemplateRenderer {

    fillDictionaries = function(questionNumber, answerNumber) {
        var me = this,
            baseAnswerIDSuffix = `${questionNumber}_${answerNumber}`;

        me.valueDict = {
            'answer_template_template': `answer_${baseAnswerIDSuffix}`,
            'answer_input_template_template': `answer_input_${baseAnswerIDSuffix}`,
            'answer_check_template_template': `answer_check_${baseAnswerIDSuffix}`,
            'questions-template-answers-template-correct': `questions-${questionNumber}-answers-${answerNumber}-correct`,
            'questions-template-answers-template-content': `questions-${questionNumber}-answers-${answerNumber}-content`
        }
    }
}


class QuestionManager {

    #renderInitials = function() {
        var me = this,
            renderer, initialContainer, initialTemplate;

        renderer = new InitialTemplateRenderer();
        // after creating renderers we have to render initial templates,
        //which will later be used as templates for other questions/answers
        renderer.fillDictionaries();
        initialTemplate = renderer.renderTemplate("#question_0");

        initialContainer = $(me.templateQuestionID);
        initialContainer.append(initialTemplate);
    }

    constructor() {
        var me = this;
        me.questions = ["#question_0", ]
        // create renderers
        me.answerRenderer = new AnswerTemplateRenderer();
        me.questionRenderer = new QuestionTemplateRenderer();

        me.templateQuestionID = "#question-template-container"
        me.templateAnswerID = "#question_template_answers";

        me.#renderInitials();

    }

    getCurrentQuestionNumber = function() {
        var me = this,
            number, lastID;
        lastID = me.questions[me.questions.length-1];
        number = parseInt(lastID.split("_")[1]);
        return number + 1;
    }

    addQuestion = function() {
        var me = this,
            questionWrapper, questionTemplate;

        questionWrapper = $("#question-container")
        me.questionRenderer.fillDictionaries(
            me.getCurrentQuestionNumber()
        )
        questionTemplate = me.questionRenderer.renderTemplate(
            me.templateQuestionID
        );
        questionWrapper.append(questionTemplate);
        me.questions.push(`#question_${me.getCurrentQuestionNumber()}`);
    }

    addAnswerToQuestion = function(questionNumber) {
        var me = this,
            answerBlock, templateAnswer, answers;

        answerBlock = $(`#question_${questionNumber}_answers`);
        answers = answerBlock.find($(".input-group"));

        me.answerRenderer.fillDictionaries(
            questionNumber, answers.length
        )

        templateAnswer = me.answerRenderer.renderTemplate(
            me.templateAnswerID
        )
        answerBlock.append(templateAnswer);

    }

}

/**
* This method should be called each time question container changes
*/
function bindAddAnswerButtons(questionManager) {
    // first clear all buttons binded methods
    $("#question-container").find('button').unbind();
    // bind new methods for thos buttons
    $("#question-container").find('button').click(function(event) {
        var buttonID, questionNumber;
        event.preventDefault();
        // extract question number
        buttonID = this.id;
        questionNumber = buttonID.split("_")[2];
        questionManager.addAnswerToQuestion(questionNumber);
    })
}


$(document).ready(function() {
    let questionManager;
    questionManager = new QuestionManager();

    $("#question-add-btn").click(function(event) {
        event.preventDefault();
        questionManager.addQuestion();
        bindAddAnswerButtons(questionManager);
    })

    bindAddAnswerButtons(questionManager);


});




