J2ME Application Generator (2009)
==========================

This program auto-generates J2ME applications. It can be used to create a variety of lab based and business based applications. This exercise demonstrates the use of a domain specific language to generate the aforementioned application(s), and does so in a manner that is significantly more efficient than writing them directly in Java.

Small portions of the program were removed for proprietary reasons, though we are willing to provide you with that intellectual property under certain circumstances. Please contact us at one of the email addresses below if you would like the additional widgets/functionality associated with this application.

Note: the filtered lists are unusable (unless you create your own) as we have removed the data generating widget related to that functionality for proprietary reasons.

Instructions:

- Install the python library ply
- cd src/
- Write a source file using the markup illustrated in FlowVersion.genericbiz
- python run.py [FlowVersion.genericbiz] # By default it will read from FlowVersion.genericbiz, but a different file may be provided as an argument
- Copy contents of generated/ to GenericBiz/src/genericbiz
- Compile in Eclipse against J2ME
