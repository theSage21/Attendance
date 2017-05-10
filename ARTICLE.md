Attendance
==========

Author: Arjoonn Sharma
Designation: Research Engineer- Machine Learning (CLAP Research)


While doing my Masters in Computational Sciences, we faced an inefficiency in
the way our lectures operated. The university demanded that we keep an
attendance record of the students in class. While this was a monstrosity in the
eyes of the students and often in the eyes of the professor, it was a monster
mandated by the University and so had to be brought into the halls of learning.
This is often the case in schools and colleges (perhaps even some government
offices) across the nation.

This is a problem plagued by false positives (we all loved those proxy
friends), false negatives (the one person who fell asleep) and, perhaps the
biggest pain of all being that the time needed to tabulate these things grows
linearly with the number of people in class often taking a full 15-20 minutes
of precious time simply to record who was here and who wasn't. At IIITM Kerala,
we were quiet frustrated with the efficiency killing nature of this task and so
when the Special Interest Group for Machine Learning was formed, we took this
up as our first challenge. The effort that my colleagues and I spent in those
days not only solved the problem we were facing, but was cheap and easy to
implement too. We finally gave it one last look and let it rest in peace. After
all, why try to fix something that is not broken? A few weeks past, I realized
that a lot more institutes could benefit from the use of this software and so
added some more things to it. The end result was `Attendance`. A software that
you can run on a machine which provides automated class attendance. In case you
don't want to go through the setup and other things, the software is also
running on our college's servers. You can use that, though you will be limited
to about 100 classes a day.

So far I haven't mentioned how this works. Let's begin by seeing how you
interact with it. For all intents and purposes, this software is a website. You
can run your own copy of this website on a machine near you. For now we will
assume that it's a website available through the Internet. 

The participants in our system are one of two kinds. The first takes
attendance, the second is the person whose attendance is being measured. In
simpler terms, the class teacher and the student respectively. Both of them
sign up for accounts on the site and register themselves as student/teacher.
The student then proceeds to upload photos of themselves, with a minimum of 1
photo. The student then sends a request to the class teacher to be accepted
into their class via the website. The class teacher approves the student
requests to join their class and that's it.

Every day, whenever there is a class the class teacher simply has to click one
or more pictures of the class. This set of pictures are then uploaded to the
site by them. The procedure to mark attendance ends here for the teacher. In
case a student discovers that his/her attendance has been missed they go online
and look up the required date-class combination and request the photos of that
day. If their face is clearly visible in any of the photos, they mark it and
submit for review with the class teacher. The teacher resolves the issue on their end.

To avoid repeated requests for review, the system learns from it's mistakes and
gets better over time. Attendance is available online for anyone who is a
stakeholder in it. Besides, any time the teacher wants they can download an
Excel Spreadsheet of the attendance till date. This makes it a powerful tool
for teachers in schools where they would have digital proof of attendance along
with nice Spreadsheets to work with.

The system itself is quiet a beautiful thing, leveraging recent publications in
the area of Deep Learning with Random Forests. This means that if you choose to
use a local machine to run this software you do not need to have a GPU to get
desirable performance.
