			   ━━━━━━━━━━━━━━━━━━
				 README


			    Damien Couroussé
			   ━━━━━━━━━━━━━━━━━━


Table of Contents
─────────────────

1 Overview
2 Install
.. 2.1 dependencies
.. 2.2 Installation process
3 Configuration file
4 program output
5 mail format
.. 5.1 email subject
.. 5.2 email body
.. 5.3 email attachments
.. 5.4 Specifying contexts
.. 5.5 date keywords
.. 5.6 Specifying deadlines
.. 5.7 Specifying scheduled dates
6 example





1 Overview
══════════

  mailtom reads an email box and process its contents to a text output
  suitable for org-mode.  Each email consists in one task that will
  enter into your org-mode tasks.

  The tool is configured with a simple configuration file.  An
  configuration example is provided: example.cfg.


2 Install
═════════

2.1 dependencies
────────────────

  `mailtom' is known to work with `python-2.7'.


2.2 Installation process
────────────────────────

  To install `mailtom' locally, run:

  ╭────
  │ $ python setup install --user
  ╰────

  And add `$HOME/.local/bin' to your `PATH' environment variable.


3 Configuration file
════════════════════

  By default, mailtom looks for a configuration file `.mailtom.cfg' in
  you `$HOME' directory.  To provide another path to the configuration
  file, use the `-c' // `--config' option:
  ╭────
  │ $ ./mailtom.py -c example.cfg
  ╰────

  The command line options always take precedence over the settings of
  the configuration file.  However, currently some configuration
  settings are not available via command line options!


4 program output
════════════════

  By default, mailtom outputs the processing results to `stdout'.  The
  command line `-o' // `--output' tells mailtom to append the processing
  results to the specified file.


5 mail format
═════════════

5.1 email subject
─────────────────

  The email subject will constitute the header of the org-mode task.
  Contexts, deadlines and scheduled dates found in the email subject are
  removed from the subject, but the information is added to the metadata
  or the org-mode task.


5.2 email body
──────────────

  The email body is copied as is in the body of the org-mode task.


5.3 email attachments
─────────────────────

  Email attachments are retrieved and copied to the attachment
  destination, specified in the configuration file.


5.4 Specifying contexts
───────────────────────

  A context is a word preceded by the '@' character.
  ╭────
  │ @phone
  ╰────


5.5 date keywords
─────────────────

  Several date formats are supported:
  • date format with 8 digits, as follows: `yyyymmdd'
  • date format with 6 digits, as follows: `yymmdd'
  • n days after the email's date: `+n' or `+nd' [1]
  • n weeks after the email's date: `+nw' [1]


5.6 Specifying deadlines
────────────────────────

  A deadline is a date keyword preceded by the string "d:".

  For example, a deadline due to march the 25th, 2014:
  ╭────
  │ d:140325
  ╰────

  or within two days:
  ╭────
  │ d:+2
  ╰────


5.7 Specifying scheduled dates
──────────────────────────────

  A scheduled date is a date keyword preceded by the string "s:".

  For example, to schedule a task within three weeks:
  ╭────
  │ s:+3w
  ╰────


6 example
═════════

  The following email message:

  ╭────
  │ Date: Wed, 06 Mar 2014 22:17:25 +0100
  │ (... data filtered out)
  │ Subject: s:+3w send a mail to Tom @work
  │ 
  │ These are my notes for this important task!
  │ 
  │ -- 
  │ [Citation aléatoire]
  │ "It would seem that you have no useful skill or talent whatsoever," he said.
  │ "Have you thought of going into teaching?"
  │ -+- Terry Pratchett, Mort -+-
  ╰────

  will end into this org-mode task:

  ╭────
  │ * INACTIVE  send a mail to Tom 					      :@work:
  │   SCHEDULED: <2014-03-27 Mar.>
  │   :PROPERTIES:
  │   :CREATED: [2014-03-06 Mar. 22:17]
  │   :END:
  │    - Note taken on [2014-03-06 Mar. 22:17] \\
  │ These are my notes for this important task!
  │ 
  │ -- 
  │ [Citation aléatoire]
  │ "It would seem that you have no useful skill or talent whatsoever," he said.
  │ "Have you thought of going into teaching?"
  │ -+- Terry Pratchett, Mort -+-
  ╰────



Footnotes
─────────

[1] n is an integer number
