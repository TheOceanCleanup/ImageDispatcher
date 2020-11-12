from directipparser.utils.parser import Parser
import pytest


def test_parser_v1(example_data_v1):
    for example in example_data_v1:
        db_objs = Parser.parse(example)

        for db_obj in db_objs:
            assert 'latitude' in db_obj.__dict__
            assert 'longitude' in db_obj.__dict__
            assert 'timestamp' in db_obj.__dict__

        assert len(db_objs) == 20
