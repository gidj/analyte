I decided to go half-way between building this out completely, and just pseudocode.
This is a recent django project (version 1.10), but I didn't do anything in the settings.py
file. I created one app, called 'search', where the models that will be saved to the database,
the views that interface between the user and the models, and a couple of forms live.

I also created a 'socialapi' module, where the classes that will do the work of getting the search
data live. It's not an app per se, as the classes don't inherit from models.Model. Everything is in
socialapi.__init__.

I used class-based views and generic views when appropriate, but I could have also used function-based
views. I know we do in my current role.

A few assumptions I made:
1. The keyword is just a simple CharField. If we wanted to build out more sophisticated
query system, we could make that a ForeignKey to some sort of SocialQuery object that
would encapsulate that ability.
2. That we are using the Django authentication framework. You might not, I know we have some
specialized User classes.
3. That the user will just want the default number of records returned for their query; the ability
to add a specific number could be done fairly easily, although we might have to hit the API more
once, keeping track of pages/slices.
4. Probably more.

A few caveats:
1. The way I implemented this, a user can save a specific social media search, but they can also
edit them at a later date. I created another model that preserves the original query for each run
of a social media search, but if we were actually building this out we might make the decision
to make them uneditable once created.
2. I didn't write any tests, and did only barebones exception checking. This of course would be
done if we were really buidling out this feature.
3. This won't actually run.
4. I tried to adhere to PEP8 and add a few comments here and there, but both would have more
attention paid to them if this were actually going to be written.
