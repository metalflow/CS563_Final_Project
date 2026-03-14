02/18/2026
Just now made the Github repo and populated the initial files: index.html, FinalProject.css
I stole some of the css and the some of the html from the "03 css" excersizes folder.
I did some very basic framing of the navbar and then I had to go make dinner.
about 30 minutes.
02/21/2026
I added some lorem ipsum and a few more div and pushed it to Github. I then tried to pubish
the page via github pages and it didn't work. I poked it for a few minutes and could get the
page to publish. Iw ll have to come back and see what's going on.
about 30 minutes.
03/01/2026
I noticed that Week9 included some work on getting the GITGUB.Io stuff to work, so I decided
to just work in LIveServer and get some basics done before I did anything fancy.
All I did today was fill out the actual text of the sections and import some pictures of myself,
my dog, and my cats. This took about an hour. Liveserver displays this webpage much like
the most basic MySpace page for the early 90's. I thought about trying to include a web assembly
of my Rust Solar system project, but initial googling suggested that it might be a bit of a
problem. I will call it for today.
03/04/2026
I thought I would add some CSS to the page today. I thought back on the CSS that we had learned
during the course, and I thought that grid would be a good place to start. I wanted the navbar
to be a horizontal bar at the top of the page. I implemented a bit of the grid, but it's
being a bit difficult to back fill the CSS. I spent about an hour on this, and I think I need
to come back to it later. The current display of the page is really wonky.
03/09/2026
I have come to accept that using Flexgrid as a primary layout tool is probably a bad idea. I am
going to delete all the previous work and use plain old CSS to lay out the primary areas of the
we page. Then I will use flex grid within those primary areas to lay out the content within. It
took me about 30 minutes to get the navbar into a fixed position and the rest of the content
to scroll independently of it. I then had to spend about 15 minutes or so googling around to
find out how to set the Z-index to keep the navbar "on top" of everything else.
03/10/2026
Time to make the pictures actually look nice. I set their width and height. I also used CSS
Grid to obviate the UL I was using and better display the images of my pets and I and to pair
the descriptive text.
03/11/2026
I cleaned up some spelling errors and expanded the text on my animals. I found out why the page
was just a little too large. It had something to do with the .Main css entry being set to
absolute. I also dressed up the section titles to be more noticeable
03/12/2026
Today's job is to populate the Projects section. Initially this is going to be links to various
Github repos that I have for previous school projects that are worth displaying. The TypeSCript
text adventure will actually be a workable link to another page, but it currently doesn't compile
on my system. I have installed the NPM tsc compiler, but I probably need to restart before it
will compile and run correctly. The RoboSnake TS was prebuilt, and thus seems to work. I have
added a few other project and given them appropraite subheaders.
03/13/2026
I transformed the navbar links into buttons and added some javascript that would cause the
individual sections to be hidded/displayed when the buttons were clicked. This proved to be
much easier said than done. The About Me section refused to be hidden. Turns out this was
the CSS value of display: grid was overriding the hidden attribute. I updated the js to
alter the display CSS attribute for the About section and it worked fine, but now I felt
like I was mixing modes in my code, so I updated all the js to alter display values.
