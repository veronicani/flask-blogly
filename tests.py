import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


from app import app, db
from unittest import TestCase
from models import DEFAULT_IMAGE_URL, User



# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# print("Printing Test db url: ", app.config["DATABASE_URL"])
print("Printing Test db url: ", app.config["SQLALCHEMY_DATABASE_URI"])

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_handle_new_user(self):
        with app.test_client() as c:
            resp = c.post(
                "/users/new",
                data={
                    "first_name": "Bob",
                    "last_name": "Test",
                    "image_url": ""
                },
                follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Bob", html)

    def test_show_user_detail_page(self):
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}")

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertIn("Edit", html)
    # TODO: test to make sure that the fields are prepopulated
    # html <inputvalue = 
    def test_show_user_edit_form(self):
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}/edit")

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Delete", html)
            self.assertIn("Save", html)

    def test_handle_user_edit_form(self):
        with app.test_client() as c:
            resp = c.post(
                "/users/new",
                data={
                    "first_name": "Bob-2",
                    "last_name": "Test",
                    "image_url": ""
                },
                follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Bob-2", html)
            #TODO: test that the last name is also "Test"

    def test_handle_delete_user(self):
        with app.test_client() as c:
            resp = c.post(
                f"/users/{self.user_id}/delete",
                data={
                    "user_id": f"{self.user_id}"
                },
                follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
