// TODO - refactor this module

class BaseTemplateRenderer {

    constructor() {
        var me = this;
        me.valueDict = {};
    }

    fillDictionaries = function() {

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


class QuestionTemplateRenderer extends BaseTemplateRenderer {

    fillDictionaries = function(questionNumber) {
        var me = this;
        me.valueDict = {
            'question_0': `question_${questionNumber}`,
            'questionInput_0': `questionInput_${questionNumber}`,
            'question_0_answers': `question_${questionNumber}_answers`,
            'add_answer_0': `add_answer_${questionNumber}`,
            'questions-0-question_type': `questions-${questionNumber}-question_type`,
            'questions-0-content': `questions-${questionNumber}-content`
        }
    }

}


class AnswerTemplateRenderer extends BaseTemplateRenderer {
    fillDictionaries = function(questionNumber, answerNumber) {
        var me = this,
            baseAnswerIDSuffix = `${questionNumber}_${answerNumber}`;

        me.valueDict = {
            'answer_0_0': `answer_${baseAnswerIDSuffix}`,
            'answer_input_0_0': `answer_input_${baseAnswerIDSuffix}`,
            'answer_check_0_0': `answer_check_${baseAnswerIDSuffix}`,
            'questions-0-answers-0-correct': `questions-${questionNumber}-answers-${answerNumber}-correct`,
            'questions-0-answers-0-content': `questions-${questionNumber}-answers-${answerNumber}-content`
        }
    }
}


class QuestionManager {

    constructor() {
        var me = this;
        me.questions = ["#question_0", ]
        me.answerRenderer = new AnswerTemplateRenderer();
        me.questionRenderer = new QuestionTemplateRenderer();
    }

    getCurrentQuestionNumber = function() {
        var me = this,
            number, lastID;
        lastID = me.questions[me.questions.length-1];
        number = parseInt(lastID.split("_")[1]);
        return number
    }

    addQuestion = function() {
        var me = this,
            questionWrapper, questionTemplate;

        questionWrapper = $("#question-container")
        me.questionRenderer.fillDictionaries(
            me.getCurrentQuestionNumber()
        )
        questionTemplate = me.questionRenderer.renderTemplate(
            me.questions[0]
        );
        questionWrapper.append(questionTemplate);
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
            "#answer_0_0"
        )
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

