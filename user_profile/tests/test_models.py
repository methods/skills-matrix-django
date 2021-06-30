from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user('ss@user.com', 'userfirstname', 'usersurname', 'userteam', 'userjobrole')
        self.assertEqual(user.email, 'ss@user.com')
        self.assertEqual(user.first_name, 'userfirstname')
        self.assertEqual(user.surname, 'usersurname')
        self.assertEqual(user.team, 'userteam')
        self.assertEqual(user.job_role, 'userjobrole')
