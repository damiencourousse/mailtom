

gtdToMail is a simple program that reads a xml file and sends its contents to a mail address.

Initially this tool was developed for GTD: I used ThinkingRock to track my GTD
projects, and was looking for a simple way to synchronize my list of live
actions with a mail client on my smartphone.

To push my tasks, I extracted the list of actions from ThinkingRock (menu
Fichier >> Exporter >> Actions), and then would grab the xml file, give it to
gtdToMail so that it sends the list of tasks to a mail box somewhere in the
cloud (did I say 'cloud'?).

The tool is configured with a simple configuration file.
An configuration example is provided: example.cfg.

You also need another configuration file for the logging facilities (did I say
'facilities'?) that come with gtdToMail: logging.cfg.

Configuration file
==================

By default, gtdToMail looks for a configuration file .gtdToMail.cfg in $HOME.
To provide another path to the configuration file, use the '-c' // '--config' option:
$ ./gtdToMail.py -c example.cfg

The command line options always take precedence over the settings of the configuration file.


Mail options
============

You have three possibilities:
 - the default mailer, using smtp
 - the SSLMailer, with smtp over SSL
 - the nullMailer, which outputs the contents of what should be sent by mail to
   stdout.


Using the default mailer
------------------------

In your configuration file: set type = simple in the smtp section.

Using SSL
---------

In your configuration file: set type = ssl in the smtp section.


Using the null mailer
---------------------

 - In your configuration file: set type = null in the smtp section.
 - or invocate gtdToMail with: options -t // --test

$ ./gtdToMail.py -t -c example.cfg -f actions.xml


TODO list
=========

* update this documentation
* update this TODO list with the TODO and FIXME items from source code :)
