# Welcome to Blaze social media!
Blaze is a social media network similar to Twitter and developed using the Django framework.

## features:

-   A  personalized user profile including first and last names, email, username, profile picture, bio, and location.
-   The ability to view other users profiles and follow/unfollow them.
-   Posts with titles, contents, and categorized tags.
-   The ability to like, dislike, and comment on posts.
-   The ability to archive posts.

## Applications
- ### core
includes some common features among all apps.
- ### users
handles user-related functionality in the application. It provides the necessary models and views for user registration, authentication, and user profile management. Users can sign up, log in, update their profile information, and perform actions such as following other users and sending messages. The User model extends Django's AbstractUser model to add custom fields such as bio, location, and picture. The app also includes models for managing user relationships like followers and blocked users.
- ### posts
handles the creation and management of posts in the application. It includes models for Post, Comment, Reaction, and Image, allowing users to create posts, add comments, react to posts (like or dislike), and attach images. Posts can be associated with multiple tags for better organization and categorization. The app provides views for creating posts, displaying post details, and managing post-related actions such as adding comments and reactions. Users can also view posts in the feed and interact with them, such as liking or disliking a post.

These two apps work together to enable users to create and manage their posts, interact with other users, and build a social network-like environment within the application.

## Installation and Usage
To use this repository, you can clone it using the following command and run the project:
```
git clone git@github.com:MahsaRah99/SocialMedia_Blaze.git
```
```
cd Social_Media
```
Now config your virtual environment and activate it. then:
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```

