***********************
***********************
**** FINAL PROJECT ****
***********************
***********************

I chose to do "Project Option 2: Blog Application". I also completed some extra credit
options. You can read about those below.

***********************
***********************
***** Instructions ****
***********************
***********************

This web app was made to interact with the .db file contained in the root directory.
If the app does not find that file present before running the server, it will create a
new one.

This means that if you want to start over again, simply delete the .db file and the app
will create a fresh copy for you at next launch.

Also, the /posts/<pid> pages will render any HTML in the blog post. However, in the
/dashboard page it will show the HTML string escaped. This is to prevent the HTML
in the blog post from breaking the table layout in /dashboard.

To run the app, use the command 'python app.py' or equivalent for your environment. 

***********************
***********************
***** Solution ********
***********************
***********************

My solution to the blog prompt was to create an index page at the '/' route to show
the blog to the public. Anyone can view this page and all it does it selects all of
the posts in the sqlite3 database and shows them in reverse order. You can click on
each of the posts to read them in full HTML format.

The '/' page has a login button and a dashboard button. All routes that render anything
that is sensitive will redirect to '/login' if the user is not logged in. I have 4 usernames
and passwords that you are able to use to login. 

Once the user logs in they are redirected to the '/dashboard' page where they can create
new posts, edit old posts and delete existing posts. They can also view the posts from that
page in case they want to see a preview of the post. Clicking 'delete' will remove the post
from the database and refresh the dashboard. Clicking 'edit' will take the user to a page
where they can edit their post. I chose to pre-populate the form inputs with the values
that are already part of the post and update the post with all changes made on that page. 
That seemed like the easiest and most reliable way to do editing. 

Posts are created with a unique permalink. To accomplish this I used the title of the 
post and replaced all spaces with dashes. Then I added this to a '/posts/' route and
added that route with the permalink as an input such as: '/posts/<permalink_url>'. 
Then I take that '<permalink_url>' and search the database for the post that has that
unique link and show that to the user on that page so they can view the post. 

For the multiple logins I added in a Users table to the database which contained all the
users for the app and their passwords. In theory, I could add permission levels to only 
allow a user with admin permissions to perform edits etc... But I did the best I could
to follow the prompt.

I hope this fully explains the core functionality and the 2 pieces of extra credit. 

***********************
***********************
***** Usernames &  ****
***** Passwords *******
***********************
***********************

+----+--------------+------------------+
| ID |   username   |     password     |
+----+--------------+------------------+
|  1 | admin        | password         |
|  2 | johndoe      | password2        |
|  3 | janedoe      | password3        |
|  4 | marcoskruger | hal0wars4uditor3 |
+----+--------------+------------------+


***********************
***********************
***** Extra Credit ****
***********************
***********************

- Completed permalinks extra credit
- Completed multiple users extra credit
