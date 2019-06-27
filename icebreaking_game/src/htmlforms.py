#!/usr/local/bin/python3
#
# Question list / form in HTML Format.
#

# Instructions should be printed on the back of each page.

# 1.75" x 0.666 Probable label size?
DOCUMENT_HEADER = """
<html>
<head>
<style>
  * {
   font-family: Helvetica, sans-serif;
  }
  h2 {
    text-align: center;
    margin: 0;
  }
  .answer-box {
    height: 0.72in;
    width: 2.5in;
    border: 1px solid grey;
  }
  .question {
    border: none;
    text-align: right;
  }
  table {
    width: 100%;
  }
  td {
    vertical-align: top;
    font-size: 12pt;
    padding: 0.5em 1em;
  }
  table {
    border-spacing: 0;
  }
  @media print {
    footer {page-break-after: always;}
  }
</style>
</head>
<body>
"""

PAGE_BREAK = """
<footer></footer>
"""

QUESTION_PAGE_HEADER = """
<table style="width:100%; font-size: larger;">
 <tr>
   <td>Your name</td>
 </tr>
</table>
"""

INSTRUCTIONS = """
<div style='font-size: larger'>
<h2>Break Some Ice @ GCC 2019</h2>
<br />
<p>GCC will be larger than any GCC before it. This is good
 because it will create more opportunities to learn from each other and
 to create collaborations. However, it can also be daunting: The bigger
 the meeting, the harder it is to maintain the interactive and collaborative
 feel that past GCCs have successfully cultivated. So, to address
 this...</p>
<br />
<h2>We are pleased to offer the GCC Icebreaker</h2>
</div>
<h2>Instructions</h2>
<ol>
<li> Find a different person for each question in your list. </li>
<li> Convince them to write their names in the specific field. You may have to trade
  your name, or information, or engage in outright bribery.</li>
<li> You cannot answer one of your own questions.</li>
<li> <em>You lose major style points if you engage with someone, and the
 only thing you get is their names.</em>  Engage! Find out what
 they do, what their challenges are, ... </li>
<li> Sponsors and conference organizers are <em>not eligible</em> for the
 prize. </li>
<li> <strong>Have fun, meet people, build new collaborations, expand your
 network, and go outside your comfort zone!</strong></li>
</ol>
<br />
<h2>The Drawing</h2>
<p>There will be a drawing for the prize during the last session of the
 conference on Thursday.</p>
<p> Things to know:
<ol>
<li> <strong>Your form needs to be turned in to the conference desk no
 later than Thursday morning (10:00 am)</strong>.
 Forms turned in after that will not be eligible. </li>
<li> Forms will be reviewed by the organizers.</li>
<li> All forms with the maximum number of correct answers (whatever the
 maximum number is) will be entered in the prize drawing. </li>
<li> The prize drawing will happen at the last session of the conference on Thursday.</li>
<li><strong> You must be present at the drawing to win.</strong>
</ol>
<br />


"""


class QuestionPage:
    """
    Defines pages that list the questions.
    """

    def __init__(self, question_list):
        """Given a question list, create a QuestionPage.
        Later this will be rendered.
        """
        self.questions = question_list

        return None

    def to_html(self, question_limit):
        """
        Render this question page as HTML and return the text as text.
        Generate no more than question_limit questions per page.

        Pages consist of
          Header section
          question list
          Closing section

        This does not generate the surrounding HTML document.
        It does generate a page break at the end.
        """
        html = []                         # converted to 1 string at end
        html.append("<h2>Break Some Ice @ GCC 2019</h2>")
        html.append("<hr />")

        html.append("<p>Find someone who...<br /></p>")
        html.append("<table>")
        i = 1
        for q in self.questions:
            html.append(" <tr>")
            html.append("  <td> {0}.</td>".format(i))
            html.append("  <td class='question'> {0}</td>".format(q.text))
            html.append("  <td class='answer-box'> </td>")
            html.append(" </tr>")
            i += 1
            if i > question_limit:
                break

        html.append("</table>")
        html.append("<hr />")
        html.append("<h3>Your Name:</h3>")

        html.append(PAGE_BREAK)

        return("\n".join(html))


class Forms:
    """
    The output document.
    """

    def __init__(self, num_questions):
        """
        Create a document that is ready to have forms and instructions
        added to it.  Limit the number of questions on each form to
        num_questions max.
        """
        self.question_pages = []
        self.question_limit = num_questions
        return None

    def add_new_form(self, question_list):
        """
        Add a new form, complete with questions and instructions to
        the document.

        """
        self.question_pages.append(QuestionPage(question_list))
        return None

    def to_html(self):
        """
        Convert the form document to HTML.
        """
        self.html = []
        self.html.append(DOCUMENT_HEADER)
        for qp in self.question_pages:
            self.html.append(qp.to_html(self.question_limit))
            self.html.append(INSTRUCTIONS)
            self.html.append(PAGE_BREAK)

        return("\n".join(self.html))
