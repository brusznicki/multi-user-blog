# MuBlog

![Screenshot of mublog](http://i.imgur.com/Vy97Scs.png "we never said it was pretty")
[mublog](https://github.com/brusznicki/multi-user-blog) is an educational project for the [Udacity](https://www.udacity.com) Full Stack developer course. I build this project with my daughter to help her learn about code and blogging. The app runs on [Google Cloud](http://cloud.google.com) and [Google App Engine](https://cloud.google.com/appengine/)

Author: Chris Brusznicki

[Production(ish) mublog running on Google App Engine](https://udacity-blog-v2.appspot.com/)

# Quickstart

### Install

* Install [Python 2.7](https://www.python.org/downloads/)
* Install the [Google Cloud SDK](https://cloud.google.com/sdk/downloads)
* Install the [Google App Engine for Python](https://cloud.google.com/appengine/downloads)
![Get the Python version](http://i.imgur.com/Y29MNjT.png "Python is what you want")
* Clone this repository to your development environment
```
git clone git@github.com:brusznicki/multi-user-blog.git your-directory EXAMPLE-FOLDER
```
* (Optional) Setup [deploying to gcloud](https://cloud.google.com/sdk/gcloud/reference/app/deploy)
* Launch the development server
```
~ dev_appserver.py app.yaml
```
* Deploy to gcloud
```
~ gcloud app deploy app.yaml --project udacity-blog-v2
```
* Navigate to [localhost:8080](http://localhost:8080) to view the application.

`Pro-tip` You can view your [datastore](https://cloud.google.com/datastore/docs/datastore-api-tutorial) at [localhost:8000/datastore](http://localhost:8000/datastore). If you need to do caveman debugging the datastore will be superhelpful.

### Using the app

1. `mublog` comes with no content. To get started create a user account by clicking "Sign up" on the top right of the main page.
2. Create your account
3. From there create a post by clicking "new post" also found on the top right of the main page.
4. Rejoice in the simple `mublog` greatness

### Other stuff you should know

1. See [app.yaml](https://github.com/brusznicki/multi-user-blog/blob/master/app.yaml) for more configuration details
1. The front end here is a bit of an afterthought. Most of the markup and styling is done with [Twitter Boostrap](http://www.getbootstrap.com)'s grid system and base styles.
2. We chose the DB vs. NDB client library because that's what was used in the Udacity 253. [This page](https://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) would be helpful when converting to NDB.
3. Our production datastore and server had trouble until we created an [index.yaml](https://github.com/brusznicki/multi-user-blog/blob/master/index.yaml). If your server is mysteriously failing check your [logs](https://cloud.google.com/appengine/docs/standard/python/logs/)

# Caveats

### Educational purposes only

`mublog` was created for educational purposes. Core features must be improved before `mublog` can be considered a production level product. For example, there are no tests for this product so continues integration will be murky from here on out. These issues are outlined in future improvements below.

### Things we learnt

[Python Decorators](https://wiki.python.org/moin/DecoratorPattern) are pretty helpful but we're still new to them. We found these resources helpful:

* [Codeship on Python decorators](http://thecodeship.com/patterns/guide-to-python-function-decorators/)
* [Tutoral invovling built in Django decorators](http://scottlobdell.me/2015/04/decorators-arguments-python/)

In the future we need to figure out how to elegantly match up the parameters consumed and passed by the wrapping / wrapped functions. See this psuedo code for example:

```
def user_is_god(function):
    """returns user if user is in fact god"""
    @wraps(function)
    def wrapper(self, some_param_needed_by_wrapped_function)
        user = self.user
        if self.user == God:
            return function(self,
                            some_param_needed_by_wrapped_function,
                            user)
        else:
            self.error(403)
            return self.redirect("/")


def some_func(self):
    """
    @user_is_god
    def get(self, some_param_needed_by_wrapped_function, user):
        # does some cool stuff
        return
```

It seems clunky to have to match the params in this manner and I feel like I'm missing something about the enclosing scope. You can see implementation of this pattern in [decorators.py](https://github.com/brusznicki/multi-user-blog/blob/master/helpers/decorators.py) and [delete.py](https://github.com/brusznicki/multi-user-blog/blob/master/handlers/comment/delete.py). Feedback is welcome!

### Future improvements

`mublog` needs some love if it will ever compete with the likes of [Wordpress](http://www.wordpress.com) Here are those features listed by order of importance, most important first:

1. DevOps / Tests
* models including their validations and assocations
* handlers to ensure that expected permissions and behaviors are observed
* select and install a continuous integration tool [https://en.wikipedia.org/wiki/Continuous_integration](https://en.wikipedia.org/wiki/Continuous_integration). (I am partial to [Codeship](https://codeship.com/))
* Consider installing [Flask](http://flask.pocoo.org/) to speed up the above items
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
5. Post handler / model
* Index only displays last 10, add pagination
* Add search
* Add Sort
* add index by author

### License

`mublog` is a public domain work, dedicated using the
[MIT License](https://opensource.org/licenses/MIT). See [LICENSE.md](https://github.com/brusznicki/multi-user-blog/blob/master/LICENSE.md) for more details.

