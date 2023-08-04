1) To start the django file

- Activate the virtual environment
	.\Scripts\activate

- Go to backend folder
	cd backend

- Start the server
	python manage.py runserver

2) To start the react file

- Go to react folder
	cd my_project

- Start the project
	npm start

After starting the django server only, the django and react would be connected and the data of django would be seen in django file.

Django administration
Username: admin
Password: admin123

Admin can also login through the website
Username: admin
Password: admin123

Admin can go to the dashboard page through the url
http://localhost:3000/admin/dashboard
 - view order in this particular page.

http://localhost:3000/admin/restaurant
 - CRUD operation of the restaurant page.
 
http://localhost:3000/admin/menu-dashboard/1
 - CRUD operation of menu of particular restaurant

Admin can
- CRUD operation of restaurant
- CRUD operation of menu
- Manage order details
- Manage reviews


Normal users can
- Search restaurant
- View home page
- View restaurant page
- View menu page
- Register an account
- Verify the email
- View reviews

Logged in users can do
- View restaurant and menu page
- add menu to cart page
- add order details
- do the payment
- visit profile page
- add and delete reviews to restaurant


* While registering a new account, certain time is needed.

* For registering new user, valid email is needed. 
 
* To login to that user, email should be verified through the link provided in the valid
  mail. After successfully verification of mail, user can now login to the website.
