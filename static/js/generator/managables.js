
class BaseManagable {
    constructor(itemID) {
        var me = this;
        me.itemID = itemID
    }
}


class Question extends BaseManagable {
    constructor(itemID) {
        super(itemID);
        var me = this;
        me.answerBlockID = `${me.itemID}_answers`
    }

}

class Answer extends BaseManagable {

}

