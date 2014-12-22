# -*- coding: utf-8 -*-
'''Unit tests for ckan/logic/converters.py.

'''
import nose
import unittest
import ckan.logic.converters as converters


eq_ = nose.tools.eq_


class TestRemoveWhitespaceConverter(unittest.TestCase):
    def test_leading_space(self):
        string = '  http://example.com'
        expected = 'http://example.com'
        converted = converters.remove_whitespace(string, {})
        self.assertEqual(expected, converted)

    def test_trailing_space(self):
        string = 'http://example.com  '
        expected = 'http://example.com'
        converted = converters.remove_whitespace(string, {})
        self.assertEqual(expected, converted)

    def test_space_between(self):
        string = 'http://example.com/space between url '
        expected = 'http://example.com/space between url'
        converted = converters.remove_whitespace(string, {})
        self.assertEqual(expected, converted)

    def test_not_a_string(self):
        string = 12345
        converted = converters.remove_whitespace(string, {})
        self.assertEqual(string, converted)


class TestConvertToExtras(unittest.TestCase):

    def test_convert_to_extras_output_unflattened(self):

        key = ('test_field',)
        data = {
            ('test_field',): 'test_value',
        }
        errors = {}
        context = {}

        converters.convert_to_extras(key, data, errors, context)

        eq_(data[('extras', 0, 'key')], 'test_field')
        eq_(data[('extras', 0, 'value')], 'test_value')

        assert not ('extras',) in data

        eq_(errors, {})

    def test_convert_to_extras_with_added_extras_output_unflattened(self):
        """
        See https://github.com/ckan/ckan/issues/2150 for origin of this
        test.

        tl;dr - the existence of the ('extras', ) key/value pair brought about
        by customizing a data set with named metadata fields stored as extras
        (as outlined in the CKAN docs) interfered with the unflattening
        process.
        """

        data = {
            ('foo', ): 'bar',
            ('baz', ): 'quux',
            ('extras',): [{'key': 'foo', 'value': u'bar'},
                          {'key': 'baz', 'value': u'quux'}, ],
            ('extras', 0, 'key'): u'qwe',
            ('extras', 0, 'value'): u'qwe',
            ('extras', 1, 'key'): u'wer',
            ('extras', 1, 'value'): u'wer',
        }
        errors = {}
        context = {}

        converters.convert_to_extras(('foo',), data, errors, context)
        converters.convert_to_extras(('baz',), data, errors, context)

        eq_(data[('extras', 0, 'key')], 'qwe')
        eq_(data[('extras', 0, 'value')], 'qwe')
        eq_(data[('extras', 1, 'key')], 'wer')
        eq_(data[('extras', 1, 'value')], 'wer')
        eq_(data[('extras', 2, 'key')], 'foo')
        eq_(data[('extras', 2, 'value')], 'bar')
        eq_(data[('extras', 3, 'key')], 'baz')
        eq_(data[('extras', 3, 'value')], 'quux')

        assert not ('extras',) in data

        eq_(errors, {})

    def test_convert_to_extras_output_unflattened_with_correct_index(self):

        key = ('test_field',)
        data = {
            ('test_field',): 'test_value',
            ('extras', 0, 'deleted'): '',
            ('extras', 0, 'id'): '',
            ('extras', 0, 'key'): 'proper_extra',
            ('extras', 0, 'revision_timestamp'): '',
            ('extras', 0, 'state'): '',
            ('extras', 0, 'value'): 'proper_extra_value',
        }
        errors = {}
        context = {}

        converters.convert_to_extras(key, data, errors, context)

        eq_(data[('extras', 0, 'key')], 'proper_extra')
        eq_(data[('extras', 0, 'value')], 'proper_extra_value')
        eq_(data[('extras', 1, 'key')], 'test_field')
        eq_(data[('extras', 1, 'value')], 'test_value')

        assert not ('extras',) in data

        eq_(errors, {})
