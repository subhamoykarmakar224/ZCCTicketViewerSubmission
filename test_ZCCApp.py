try:
    import bottle, unittest
    from boddle import boddle
    import unittest, os, json
    from os.path import join, dirname
    import ZCCApp as App
    import Helper as helper
    from urllib.parse import urlparse
    from Constants import *
    import random, string
except Exception as e:
    print('Some Modules are missing {} '.format(e))


class ZccAppTest(unittest.TestCase):
    def test_if_path_exists(self):
        path = join(dirname(__file__), 'test_ZCCApp.py')
        self.assertTrue(helper.if_path_exists(path))

    def test_if_path_exists_not(self):
        path = join(dirname(__file__), 'test_ZCC.py')
        self.assertFalse(helper.if_path_exists(path))

    def test_data_cleaning_ticket(self):
        data = {'tickets': [{'url': 'asd', 'id': 101, 'external_id': None,
                             'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}},
                             'created_at': '2021-11-22T15:20:17Z', 'updated_at': '2021-11-22T15:20:17Z', 'type': None,
                             'subject': 'in nostrud occaecat consectetur aliquip',
                             'raw_subject': 'in nostrud occaecat consectetur aliquip',
                             'description': 'Esse esse quis ut esse nisi tempor sunt. Proident officia incididunt cupidatat laborum ipsum duis. Labore qui labore elit consequat.\n\nDo id nisi qui et fugiat culpa veniam consequat ad amet ut nisi ipsum. Culpa exercitation consectetur adipisicing sunt reprehenderit. Deserunt consequat aliquip tempor anim officia elit proident commodo consequat aute. Magna enim esse tempor incididunt ipsum dolore Lorem cupidatat incididunt.',
                             'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 421895567792,
                             'submitter_id': 421895567792, 'assignee_id': 421895567792, 'organization_id': 361630678631,
                             'group_id': 360022295451, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
                             'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True,
                             'due_at': None, 'tags': ['deserunt', 'enim', 'est'], 'custom_fields': [],
                             'satisfaction_rating': None, 'sharing_agreement_ids': [], 'followup_ids': [],
                             'ticket_form_id': 360003536671, 'brand_id': 360007071491, 'allow_channelback': False,
                             'allow_attachments': True}]}

        data_expected = [{'id': 101, 'created_at': '2021-11-22T15:20:17Z', 'status': 'open', 'priority': None, 'subject': 'in nostrud occaecat consectetur aliquip'}]
        self.assertEqual(
            helper.data_cleaning_ticket(data),
            data_expected
        )

    def test_data_cleaning_ticket_empty(self):
        data = {'tickets': []}
        data_expected = []
        self.assertEqual(
            helper.data_cleaning_ticket(data),
            data_expected
        )

    def test_write_user_domain_name(self):
        domain = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        old_domain = self.test_write_user_domain_name_helper()
        helper.write_user_domain_name(domain)
        new_domain = self.test_write_user_domain_name_helper()
        self.assertEqual(domain, new_domain)
        self.assertNotEqual(new_domain, old_domain)
        helper.write_user_domain_name(old_domain)

    def test_write_user_domain_name_helper(self):
        ln = []
        with open(URI_DOMAIN_DATA_FILE, 'r') as l:
            ln = l.readlines()
        return ln[0]

    def test_read_user_domain_name(self):
        old_domain = self.test_write_user_domain_name_helper()
        domain = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        helper.write_user_domain_name(domain)
        new_domain = helper.read_user_domain_name()
        self.assertEqual(domain, new_domain)
        self.assertNotEqual(new_domain, old_domain)
        helper.write_user_domain_name(old_domain)
