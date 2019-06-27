#!/usr/local/bin/python3
#
# Defines the list of participants attending, and all their characteristics.

import csv
import math

import htmlforms


class Participant:
    """Participant information arrives as a row in a spreadsheet.  This
    code does not particularly care about all the columns in the spreadsheet,
    only that the columns specified in the data-driven questions exist.
    """
    def __init__(self, participant_info):
        """
        Given a dictionary of items about a specific participant, create
        a Participant for it.
        """
        self._participant_info = participant_info

        self.questions = []

        return None

    def get_value(self, item_name):
        """Given an attribute name, get the value of that attribute for this
        participant.
        """
        return(self._participant_info[item_name])

    def add_question(self, question):
        self.questions.append(question)

        return None


class ParticipantLib:
    """A library of participants and their information.
    """

    def __init__(self, participant_file_path):
        """Given the path to a spreadsheet file containing participant info,
        read it into a new participant library. This only provides serial
        access to individual records, and to summary information.
        """
        self.participants = []

        fp = open(participant_file_path, "r")
        participant_reader = csv.DictReader(fp, delimiter='\t')
        for participant_cols in participant_reader:
            self.participants.append(Participant(participant_cols))

        return None

    def __iter__(self):
        self.iter_pos = -1
        return self

    def __next__(self):
        if self.iter_pos >= len(self.participants) - 1:
            raise StopIteration
        self.iter_pos += 1
        return self.participants[self.iter_pos]

    def get_count(self):
        return len(self.participants)

    def generate_forms(self, forms_path, num_questions):
        """
        Generate a form for each participant.  Limit number of
        questions to num_questions max.
        """
        fp = open(forms_path, "w")
        doc = htmlforms.Forms(num_questions)

        for p in self.participants:
            doc.add_new_form(p.questions)

        fp.write(doc.to_html())
        fp.close()

        return None

    def generate_spreadsheet_for_mail_merge(
            self, mail_merge_path, labels_fields,
            label_columns, label_rows, labels_per_person):
        """
        create a spreadsheet that will be fed to a mail merge program in the
        future. This method is told about the dimensions of the label sheet
        that will be used

        Most mail merges populate labels from left to right, before moving
        on to the next row of labels.  We want the same labels in the same
        column, not the same row, this generates a list of entries with
        label_columns - 1 other names in between.  That way, when it gets
        printed, the same person is stacked in each column.
        """
        n_participants = len(self.participants)
        n_sheets = math.ceil(n_participants / label_columns)
        n_labels_per_sheet = label_columns * label_rows
        labels_to_be = [None] * (n_sheets * n_labels_per_sheet)

        sorted_participants = sorted(
            self.participants,
            key=lambda p: (
                p._participant_info["name"]
                + " " + p._participant_info["firstname"]))

        sheet_start_i = 0
        column_i = 0
        for p in sorted_participants:
            for row_i in range(0, labels_per_person):
                pos = sheet_start_i + column_i + row_i * label_columns
                labels_to_be[pos] = {}
                for field in labels_fields:
                    labels_to_be[pos][field] = p._participant_info[field]
            column_i += 1
            if column_i == label_columns:
                # time to move to next sheet
                sheet_start_i += n_labels_per_sheet
                column_i = 0

        # We be done, now write it out as a csv
        labels_file = open(mail_merge_path, "w")
        labels_writer = csv.DictWriter(
            labels_file, fieldnames=labels_fields)
        labels_writer.writeheader()
        for label in labels_to_be:
            if label:
                labels_writer.writerow(label)

        labels_file.close()

        return None

    def generate_forms_orig(self):

        min_hard = 100.0
        max_hard = 0.0
        for p in self.participants:

            print("Find someone:")
            print()
            i = 1
            hardness = 0.0
            for q in p.questions:
                print("{0}. {1}".format(i, q.text))
                print("     Difficulty: {0}".format(q.difficulty))
                print()
                i += 1
                hardness += q.difficulty

            print("Total difficulty: {0}".format(hardness))
            print()
            print("============ PAGE BREAK ==============")
            print()

            if hardness > max_hard:
                max_hard = hardness
            if hardness < min_hard:
                min_hard = hardness

        print("Min Difficulty: {0}".format(min_hard))
        print("Max Difficulty: {0}".format(max_hard))

        return None
