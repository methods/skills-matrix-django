from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user('test@user.com', 'userfirstname', 'usersurname', 'userteam', 'userjobrole',
                                      'userpassword')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.first_name, 'userfirstname')
        self.assertEqual(user.surname, 'usersurname')
        self.assertEqual(user.team, 'userteam')
        self.assertEqual(user.job_role, 'userjobrole')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(email = '', first_name='user_firstname', surname = 'user_surname', team = 'user_team', job_role='user_jobrole',
                                      password='user_password',is_superuser=False)

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser('superuser@superuser.com', 'superuserfirstname', 'superusersurname', 'superuserteam', 'superuserjobrole',
                                      'superuserpassword')
        self.assertEqual(super_user.email, 'superuser@superuser.com')
        self.assertEqual(super_user.first_name, 'superuserfirstname')
        self.assertEqual(super_user.surname, 'superusersurname')
        self.assertEqual(super_user.team, 'superuserteam')
        self.assertEqual(super_user.job_role, 'superuserjobrole')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertIn('superuser@superuser.com',str(super_user))
        self.assertTrue(super_user.has_perm('user_profile.newuser'))
        self.assertTrue(super_user.has_module_perms('user_profile.newuser'))

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email = 'superuser@superuser.com', first_name='superuser_firstname', surname = 'superuser_surname', team = 'superuser_team', job_role='superuser_jobrole',
                                      password='superuserpassword', is_superuser=False)
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email = 'superuser@superuser.com', first_name='superuserfirstname', surname = 'superusersurname', team = 'superuserteam', job_role='superuserjobrole',
                                      password='superuserpassword', is_staff=False)
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email = 'super@super.com', first_name='super_firstname', surname = 'super_surname', team = 'super_team', job_role='super_jobrole',
                                      password='password', is_admin=False)
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email = '', first_name='superuserfirstname', surname = 'superusersurname', team = 'superuserteam', job_role='superuserjobrole',
                                      password='superuserpassword',is_superuser=False)