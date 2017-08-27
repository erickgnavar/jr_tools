#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `jr_tools` package."""


import unittest
from click.testing import CliRunner

from jr_tools import cli


class JasperReportsToolsTestCase(unittest.TestCase):
    """Tests for `jr_tools` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'run_report' in result.output
        help_result = runner.invoke(cli.main, ['run_report', '--help'])
        assert help_result.exit_code == 0
