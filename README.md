# MuBlog

[mublog](https://github.com/brusznicki/multi-user-blog) is an educational project for the [Udacity](https://www.udacity.com) Full Stack developer course. I build this project with my daughter to help her learn about code and blogging. The app runs on [Google Cloud](http://cloud.google.com) and [Google App Engine](https://cloud.google.com/appengine/)

Author: Chris Brusznicki

[Production(ish) mublog running on Google App Engine](https://udacity-blog-v2.appspot.com/)

# Quickstart

### Install

* Install the [Google Cloud SDK](https://cloud.google.com/sdk/downloads)
* Install the [Google App Engine for Python](https://cloud.google.com/appengine/downloads)
![Get the Python version](http://imgur.com/Y29MNjT "Python is what you want")
* Clone this repository to your development environment
* (Optional) Setup [deploying to gcloud](https://cloud.google.com/sdk/gcloud/reference/app/deploy)
* Launch the development server

#### Launch app locally
```
~ dev_appserver.py app.yaml
```
#### Deploy to gcloud
```
~ glcoud app deploy app.yaml --project udacity-blog-v2
```
Navigate to [localhost:8080](http://localhost:8080) to view the application.

`Pro-tip` You can view your [datastore](https://cloud.google.com/datastore/docs/datastore-api-tutorial) at [localhost:8000/datastore](http://localhost:8000/datastore). If you need to do caveman debugging the datastore will be superhelpful.

### Using the app

1. `mublog` comes with no content. To get started create a user account by clicking "Sign up" on the top right of the main page.
2. Create your account
3. From there create a post by clicking "new post" also found on the top right of the main page.
4. Rejoice in the simple `mublog` greatness

# Caveats

### Educational purposes only

* `mublog` was created for educational purposes. Core features must be improved before `mublog` can be considered a production level product. For example, there are no tests for this product so continues integration will be murky from here on out. These issues are outlined in future improvements below.


### Future improvements

`mublog` needs some love if it will ever compete with the likes of [Wordpress](http://www.wordpress.com) Here are those features listed by order of importance, most important first:

1. DevOps
* Write basic tests
** models including their validations and assocations
** handlers to ensure that expected permissions and behaviors are observed
** select and install a continuous integration tool [https://en.wikipedia.org/wiki/Continuous_integration](https://en.wikipedia.org/wiki/Continuous_integration). (I am partial to [Codeship](https://codeship.com/))
2. User controls
* Admin screen to control users
* User roles (admin, poster, reader)
* User CRUD
* Forgot password
* Refactor to use an open source product for authentication, O-auth, etc. It's not really that fun to write user validations, regex for passwords, etc.
3. Support more content
* We only support HTML and should support photos, etc.
* Social Media integration - if media isn't shareable, it's not discoverable
4. Integrate a front end framework such as [React](https://reactjs.net/)
* Modularize each component in the app
* Support themes


### License

`mublog` is a public domain work, dedicated using the
[MIT License](https://opensource.org/licenses/MIT). See LICENSE.md for more details.

