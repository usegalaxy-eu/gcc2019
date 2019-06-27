#!/usr/local/bin/python3
#
# Defines data-driven questions and question libraries for icebreaker.

# Define text used to define data driven questions in configuration files

INPUT_ITEM = "input_item"
INPUT_ARITY_ITEM = "input_arity"
OUTPUT_QUESTION_ITEM = "output_question"

# What values can ARITY have?

INPUT_ARITY_SINGLETON = "Singleton"
INPUT_ARITY_LIST = "List"


class DataQuestion:
    """These are defined in the config file as
        "data_questions": [
            {
                "input_item": "City",
                "input_arity": "Singleton",
                "output_question": "Someone from"
            },
            {
                "input_item": "State",
                "input_arity": "Singleton",
                "output_question": "Someone from"
            },

    Where
    - input_item identifies a column in the participant spreadsheet that
                 will be used to generate this question.
    - input_arity Does this item have one value, or multiple values?
    - output_question The starting text of the question. The value from
                 the input_item column will become the end of the question.
    """
    def __init__(self, question_items):
        """
        Given a dictionary of items about a specific question, create
        a DataQuestion for it.
        """
        self.input_item = question_items[INPUT_ITEM]
        self.input_arity = question_items[INPUT_ARITY_ITEM]
        self.output_question = question_items[OUTPUT_QUESTION_ITEM]

        # after reading in participant data, we'll summarize the
        # participant responses for this question.  This will be
        # basically an array of values that participants have for
        # this question, followed by count / percentage of participants
        # with that value.
        self.participant_values = {}

        return None

    def get_penetrance(self, value):
        """
        penetrance for data questions is calculated and is based on
        how popular a given value was.
        """
        return self.participant_values[value]


class DataQuestionLib:
    """A library of questions that are driven by information
    from the participants.
    """

    def __init__(self, raw_question_list):
        """Create question library for a set of data driven questions.
        """
        self.question_list = []

        # keep track of which items from participants we will need to
        # gather data for.
        self.participant_items = []

        for raw_q in raw_question_list:
            q = DataQuestion(raw_q)
            self.question_list.append(q)
            self.participant_items.append(q.input_item)

        return None

    def add_participant_responses(self, participants):
        """
        These are data driven questions!  Gather the information for each
        question from all the participants.  This information will then
        determine how often each question is asked.
        """
        for participant in participants:
            for question in self.question_list:
                values = []
                value = participant.get_value(question.input_item)
                if value != "":
                    if question.input_arity == INPUT_ARITY_LIST:
                        # need to split up value into multiple values
                        vals = value.split(", ")
                        print(vals)
                        for val in vals:
                            values.append(val)
                    else:
                        values.append(value)
                # values now contains each value for current question
                # from current participant.
                for value in values:
                    if value not in question.participant_values:
                        question.participant_values[value] = 0
                    question.participant_values[value] += 1

        # We are done gathering participant information
        # convert counts to percentages
        participant_count = participants.get_count()

        for question in self.question_list:
            for value in question.participant_values:
                question.participant_values[value] = (
                    question.participant_values[value] / participant_count)
                # print("Value: '{0}' %: {1}".format(
                #     value, question.participant_values[value]))

        return
