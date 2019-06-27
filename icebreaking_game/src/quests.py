#!/usr/local/bin/python3
#
# Defines questions and question libraries for icebreaker.

# Define text used to define questions in configuration files

# Non data questions
QUESTION_ITEM = "question"
PENETRANCE_ITEM = "penetrance"
DIFFICULTY_ITEM = "difficulty"


class Question:
    """These are defined in the config file as
        "questions": [
            {
                "question": "Who has attended at least 3 previous GCCs",
                "penetrance": 0.05,
                "difficulty": 1.0
            },
            {
                "question": "Who has attended at least 4 previous BOSCs",
                "penetrance": 0.05,
                "difficulty": 1.0
            },


    Where
    - question is the text to use
    - penetrance is between 0 and 1 says (roughly) how frequently this
                 question should occur on question sheets.
    - difficulty is an estimate of how hard this question will be to
                 answer.  From 0 (easy) to 1 (hard)
    """
    def __init__(self, question_items):
        """
        Given a dictionary of items about a specific question, create
        a Question for it.
        """
        self.text = question_items[QUESTION_ITEM]
        self.penetrance = question_items[PENETRANCE_ITEM]
        self.difficulty = question_items[DIFFICULTY_ITEM]

        return None

    def get_penetrance(self):
        return self.penetrance


class QuestionLib:
    """A library of questions.
    """

    def __init__(self, raw_question_list):
        """Create question library for a set of questions.
        """

        self.question_list = []
        self.total_penetrance = 0.0
        self.question_count = 0

        for raw_q in raw_question_list:
            q = Question(raw_q)
            self.question_list.append(q)
            self.total_penetrance += q.penetrance
            self.question_count += 1

        return None

    def convert_and_add_data_questions(
            self, data_questions, min_2b_tractable, max_2b_interesting):
        """
        Once we have read and processed the participant info, we can
        convert data questions to regular questions and then treat them
        homogeneously.
        """
        for data_q in data_questions.question_list:
            for value, penetrance in data_q.participant_values.items():
                if (penetrance >= min_2b_tractable
                        and penetrance <= max_2b_interesting):
                    q_items = {}
                    q_items[QUESTION_ITEM] = (
                        "{0} {1}".format(data_q.output_question, value))
                    q_items[PENETRANCE_ITEM] = penetrance
                    q_items[DIFFICULTY_ITEM] = 1.0 - penetrance
                    q = Question(q_items)
                    self.question_list.append(q)
                    self.total_penetrance += penetrance
                    self.question_count += 1

        self.in_decreasing_penetrance_order = sorted(
            self.question_list,
            key=lambda quest: quest.penetrance, reverse=True)
        self.in_increasing_difficulty_order = sorted(
            self.question_list,
            key=lambda quest: quest.difficulty)

        return None
