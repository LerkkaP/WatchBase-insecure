# WatchBase-insecure
This is the insecure version of the application WatchBase which has at least five different flaws from the OWASP top ten list 

Passwords and usernames for testing:

admin: root

satoshi: nakamoto

The website is implemented with Python and Django so make sure you have them installed on your machine. The flaws are from the OWASP Top Ten 2017 list.

FLAW 1:

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/templates/login.html#L5

Flaw 1 is a Cross-Site Request Forgery (CSRF) vulnerability which appears in the app’s login process. The flaw allows tricking users into doing unwanted requests that are not intended to be performed. For instance, an attacker could create a harmful website or send a misleading link to a user who is authenticated. When a user opens this malicious website or a link, their browser may send a harmful request to the application that they are logged in, resulting in the execution of unwanted operations like logging out the user.

The flaw can be fixed by including a CSRF token in the login form as provided in this code:
https://github.com/LerkkaP/WatchBase-secure/blob/master/app/templates/registration/login.html#L5


The CSRF token is a security measure that helps ensure that the form submission is coming from a legitimate source and not from a malicious attacker trying to forge requests on behalf of the user. It is basically a large random number that is attached to the request url so the server can identify the client. By default, Django has CSRF middleware enabled and developers only need to include the CSRF token in forms that use the POST method and ensure that GET requests are side effect free. If a CSRF token is not included - provided that django.middleware.csrf.CsrfViewMiddleware is enabled - Django will abort POST requests and notify that a CSRF token is missing. To bypass that, the views.py file contains @csrf_exempt decorator in the view that handles the login functionality.

FLAW 2:

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/models.py#L4-L6

Flaw 2 is a Sensitive Data Exposure vulnerability which is prevalent in the logic how the application handles user data. The application’s custom user model stores passwords in plain text which leaves user accounts extremely vulnerable in the event of a data breach or if someone gains unauthorized access to the database.

The flaw can be fixed by implementing Django’s authentication system which provides a built-in user model for securely handling sensitive user data: https://github.com/LerkkaP/WatchBase-secure/blob/master/app/models.py#L3

The user model provided by Django’s authentication system doesn’t save passwords in plain text but enforces a one way hash function to store them in a secure manner; more specifically as a series of numbers and letters. It utilizes a PBKDF2 algorithm with a SHA256 hash for hashing the passwords so even if the database is breached, the actual passwords are not easily retrievable.

FLAW 3:

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/views.py#L16-L17

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/views.py#L37-L38

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/views.py#L72-L73

Flaw 3 is injection vulnerability which is directly related to how the application executes SQL queries. By using direct non-parameterized SQL queries constructed from the user input, one is able to introduce malicious queries into the database operations, potentially causing data loss or unauthorized access.

The flaw can be fixed by using Django’s Object-Relational Mapper (ORM) to perform
database queries. The ORM prevents SQL injection by automatically sanitizing and parameterizing queries. Notice that the flawed code in the lines L37-L38 is fixed by using Django’s authentication system’s authenticate function. It will be also covered in Flaw 4.

https://github.com/LerkkaP/WatchBase-secure/blob/master/app/views.py#L17

https://github.com/LerkkaP/WatchBase-secure/blob/master/app/views.py#L31

https://github.com/LerkkaP/WatchBase-secure/blob/master/app/views.py#L63

FLAW 4:

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/views.py#L31-L45

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/views.py#L52-L54

Flaw 4 is Broken Authentication vulnerability. The custom user model lacks proper password validation, allowing users to set weak passwords, such as "admin," which are easily guessable and may have been already compromised in different breaches. Weak passwords pose a severe security risk as they can be exploited by attackers to gain unauthorized access to user accounts. For example, they enable brute force attacks, where attackers can attempt various password combinations until they gain access to user accounts. There are multiple lists in the internet that contain compromised passwords. By utilizing these lists and brute forcing, breaching into an account with a weak password becomes relatively effortless.

The login functionality relies on custom SQL query to validate user credentials. It compares the input username and password directly against the database without proper authentication mechanisms. Besides compromising the app to SQL injection, it also ignores secure practices like password salting and hashing. Furthermore, there’s not a mechanism
that would limit the number of login attempts to prevent brute force attacks.

The flaw can be fixed by using Djangos authentication system.

https://github.com/LerkkaP/WatchBase-secure/blob/master/app/views.py#L25-L34

https://github.com/LerkkaP/WatchBase-secure/blob/master/app/views.py#L42-L44C20

Django’s authentication system prohibits the usage of weak passwords such as ‘admin’ and ‘nakamoto’. It uses secure SQL queries, stores passwords safely and provides a system agains brute force attacks by limiting the number of login attempts.

FLAW 5:

https://github.com/LerkkaP/WatchBase-insecure/blob/master/app/templates/details.html#L25

Flaw 5 is Cross-Site Scripting (XSS) vulnerability. Particularly, the application has a vulnerability that allows for stored XSS scripting attack. The application stores the watch description given by the user in the server without sanitizing the input. This allows for embedding malicious code in the description which is then executed everytime the page is loaded. For example, one can insert HTML tags in the description that steal user cookies or affect the website performance.

The flaw can be fixed by removing the template filter ‘safe’. https://github.com/LerkkaP/WatchBase-secure/blob/master/app/templates/details.html#L25

The ‘safe’ filter instructs the template rendering system to turn off escaping. This is risky, as user input should never be trusted. By not including the filter in the first place, any user-generated content will be escaped by default, ensuring that HTML tags are treated as plain text and not executed when rendering the page.
