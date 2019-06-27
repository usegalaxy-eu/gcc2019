#!/usr/local/bin/python3

import argparse
import json
import sys

import dataquests
import quests
import partis


USAGE = """
Britnev, a program for generating icebreaker questionnaires for event
participants.  Questions can be a mix of ones driven by participant
characteristics and ones that aren't.

Reads a config file to determine which questions to generate.  Both types of
questions are also defined there.

See the program's README for a full explanation of inputs and outputs.
"""


class Configuration (object):
    """
    Parses and then exposes the program configuration file.
    """
    def __init__(self, config_path):
        """
        Create a configuration by reading a config file.
        """
        config_file = open(config_path, "r")
        config_json = json.load(config_file)  # creates a dict

        for key, value in config_json.items():
            if key == "min_2b_tractable":
                self.min_2b_tractable = value
            elif key == "max_2b_interesting":
                self.max_2b_interesting = value
            elif key == "num_questions":
                self.num_questions = value
            elif key == "label_columns":
                self.label_columns = value
            elif key == "label_rows":
                self.label_rows = value
            elif key == "labels_per_person":
                self.labels_per_person = value
            elif key == "labels_fields":
                self.labels_fields = value  # list
            elif key == "questions":
                self.questions = quests.QuestionLib(value)
            elif key == "data_questions":
                self.data_questions = dataquests.DataQuestionLib(value)
            else:                         # There is a problem
                print(
                    "Unrecognized top level item in config file.",
                    file=sys.stderr)
                print("  Key: '{0}'".format(key))
                sys.exit(-1)


def allocate_questions_to_participants(particpants, questions):
    """
    Allocate out questions to participants until them participants are full.
    """

    """
    # participants * # of questions per form.

    Throw a warning if it does not.

    who still needs a question this iteration = everyone

    For each question:
      calculate how many times that question will be asked
      who has this question = {}

      who can have this question this iter = who_still_needs_a_questin_thi_iter
      While len(who has this question) < n_times_question_can be asked:
        randomly select from who can have this q this iter
        remove them from who can have this q this iter.
        remove them from who still_neeeds a q this iter.
        add them to who has this question.
        add the question to that participant

        if who still need a q this iter is empty:
          # move to next iteration
          iter += 1
          who still needs a question this iteration = everyone
          who can have this question this iter =
            who_still_needs_a_questin_thi_iter - who has this question
    """

    num_participants = particpants.get_count()
    who_still_needs_q_this_iter = {x for x in participants.participants}
    iter = 0

    for q in questions.in_increasing_difficulty_order:
        # How many times should we ask the current question?
        num_times_to_ask = int(q.penetrance * num_participants)
        who_has_this_q = set()

        who_can_have_this_q_this_iter = who_still_needs_q_this_iter.copy()
        while len(who_has_this_q) < num_times_to_ask:
            # ARBITRARILY (not random though) pick from eligible recipients
            recipient = who_can_have_this_q_this_iter.pop()
            # update our tracking
            # who_can_have_this_q_this_iter.remove(recipient)
            who_still_needs_q_this_iter.remove(recipient)
            who_has_this_q.add(recipient)
            # add the question to the recipient
            recipient.add_question(q)

            if len(who_still_needs_q_this_iter) == 0:
                # we have finished this iter.  Move to next
                iter += 1
                who_still_needs_q_this_iter = {
                    x for x in participants.participants}
                who_can_have_this_q_this_iter = (
                    who_still_needs_q_this_iter - who_has_this_q)

    return None


def get_args():
    """
    Parse and return command line arguments.  Note that this does not parse
    the configuration file.
    """

    arg_parser = argparse.ArgumentParser(description=USAGE)

    arg_parser.add_argument(
        "--configpath", required=True,
        help="Path to configuration file. Format: JSON")
    arg_parser.add_argument(
        "--participantdatapath", required=True,
        help="Path to participant data spreadsheet.  Format: TSV")
    arg_parser.add_argument(
        "--formspath", required=True,
        help="Where to put the ouput forms.  Format: HTML")
    arg_parser.add_argument(
        "--mailmergepath", required=True,
        help=(
            "Where to put the output spreadsheet to feed to mail merge.  " +
            "Format: TSV"))

    args = arg_parser.parse_args()

    return args


args = get_args()

# Read the config; this includes the question definitions.
config = Configuration(args.configpath)

questions = config.questions
data_questions = config.data_questions

# Read the participant list.  This in a spreadsheet.
participants = partis.ParticipantLib(args.participantdatapath)

# Add participant values to the data-driven questions.
data_questions.add_participant_responses(participants)

# Convert data questions to regular questions, and add them to
# the questions
questions.convert_and_add_data_questions(
    data_questions, config.min_2b_tractable, config.max_2b_interesting)

allocate_questions_to_participants(participants, questions)

# this maybe should not be in participants.
participants.generate_forms(args.formspath, config.num_questions)

# but this should
participants.generate_spreadsheet_for_mail_merge(
    args.mailmergepath, config.labels_fields,
    config.label_columns, config.label_rows,
    config.labels_per_person)
