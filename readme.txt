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
4 Program output
.. 4.1 command-line configuration
.. 4.2 file configuration
5 Email settings
6 Email format
.. 6.1 email subject
.. 6.2 email body
.. 6.3 email attachments
.. 6.4 Specifying contexts
.. 6.5 Dates
..... 6.5.1 Date keywords
..... 6.5.2 Specifying deadlines
..... 6.5.3 Specifying scheduled dates
7 example
8 development notes
.. 8.1 pytools git-subtree
9 legal stuff
10 footnotes





1 Overview
══════════

  `mailtom' reads an email box and processes its contents to a text
  output suitable for org-mode.  Each email consists in one task that
  will enter into your org-mode tasks.

  The tool is configured with a simple configuration file.  An
  configuration example is provided: example.cfg.

  This document is the minimalist, provided as-is, documentation for
  `mailtom' version `v0.2-17-gf976'.


2 Install
═════════

2.1 dependencies
────────────────

  `mailtom' is known to work with `python-2.7'.  It also needs the
  html2text python module.

  ╭────
  │ ii  python                                              2.7.5-5                            amd64        interactive high-level object-oriented language (default version)
  ╰────

  ╭────
  │ ii  python-html2text                                    3.200.3-2                          all          Python module for converting HTML to Markdown text
  ╰────


2.2 Installation process
────────────────────────

  To install `mailtom' locally, run:

  ╭────
  │ $ python setup install --user
  ╰────

  And add `$HOME/.local/bin' to your `PATH' environment variable.


3 Configuration file
════════════════════

  By default, `mailtom' looks for a configuration file `.mailtom.cfg' in
  you `$HOME' directory.  To provide another path to the configuration
  file, use the `-c' // `--config' option:
  ╭────
  │ $ ./mailtom.py -c example.cfg
  ╰────

  The command line options always take precedence over the settings of
  the configuration file.  However, currently some configuration
  settings are not available via command line options!


4 Program output
════════════════

  By default, `mailtom' outputs the processing results to `stdout'.


4.1 command-line configuration
──────────────────────────────

  The command line `-o' // `--output' tells `mailtom' to append the
  processing results to the specified file.


4.2 file configuration
──────────────────────

  In the section `global': parameter `output'.


5 Email settings
════════════════

  Email settings are defined in the `mail' section of the configuration
  file:

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   param name    default value  use                                                       
  ────────────────────────────────────────────────────────────────────────────────────────
   `server'      `localhost'    name of the email server                                  
   `user'        -              login used for connection to the email server             
   `passwd'      -              login password, in clear text                             
   `savedir'     `/tmp'         A path directory for saving email attachments             
   `delete_msg'  `False'        If true, `mailtom' deletes the email read from the server 
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


6 Email format
══════════════

6.1 email subject
─────────────────

  The email subject will constitute the header of the org-mode task.
  Contexts, deadlines and scheduled dates found in the email subject are
  removed from the subject, but the information is added to the metadata
  or the org-mode task.

  Subject prefixes such as 'Re: ' or 'Fwd: ' are filtered out from the
  generated task header.


6.2 email body
──────────────

  The email body is copied as is in the body of the org-mode task.


6.3 email attachments
─────────────────────

  Email attachments are retrieved and copied to the attachment
  destination, specified in the configuration file.


6.4 Specifying contexts
───────────────────────

  A context is a word preceded by the '@' character.
  ╭────
  │ @phone
  ╰────


6.5 Dates
─────────

6.5.1 Date keywords
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Several date formats are supported:
  • date format with 8 digits, as follows: `yyyymmdd'
  • date format with 6 digits, as follows: `yymmdd'
  • date format with 3 or 4 digits, as follows: `mmdd'. In this case,
    the month string `mm' is /always/ considered to be 2-digits long.
  • date format with 1 or 2 digits, as follows: `dd'
  • n days after the email's date: `+n' or `+nd' [1]
  • n weeks after the email's date: `+nw' [1]

  The date specified with the keywords `mmdd' and `dd' are computed from
  the today's year, and today's month for `dd'.


6.5.2 Specifying deadlines
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  A deadline is a date keyword preceded by the string "d:".

  For example, a deadline due to march the 25th, 2014:
  ╭────
  │ d:140325
  ╰────

  or within two days:
  ╭────
  │ d:+2
  ╰────

  If today is march the 22nd, 2014, `d:25' will specify a deadline for
  the 25th of the same month, i.e. March; `d:03' will /also/ speficy a
  deadline for the same month, even if the deadline is already passed.


6.5.3 Specifying scheduled dates
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  A scheduled date is a date keyword preceded by the string "s:".

  For example, to schedule a task within three weeks:
  ╭────
  │ s:+3w
  ╰────


7 example
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


8 development notes
═══════════════════

8.1 pytools git-subtree
───────────────────────

  Updatin the subtree:

  ╭────
  │ $ git fetch pytools
  │ $ git subtree pull --prefix mailtomlib/pytools -m '[subtree] update pytools' pytools master
  ╰────


9 legal stuff
═════════════

  Most of the code is written by Damien Couroussé. (Please provide
  patches so that can change.)

  The code is covered by the GNU General Public License, version 3 or
  later.

  Copyright (C) 2014 Damien Couroussé

  This file is part of mailtom.

  mailtom is free software: you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the
  Free Software Foundation, either version 3 of the License, or (at your
  option) any later version.

  mailtom is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
  for more details.

  You should have received a copy of the GNU General Public License
  along with mailtom.  If not, see [http://www.gnu.org/licenses/].


10 footnotes
════════════



Footnotes
─────────

[1] n is an integer number
