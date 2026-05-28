# Entrius 2025

"""Tests for the DEV_MODE network guard in validator config."""

import os

from gittensor.validator.utils.config import resolve_dev_mode


def test_dev_mode_honored_on_test_network(monkeypatch):
    monkeypatch.setenv('DEV_MODE', '1')
    assert resolve_dev_mode('test') is True
    assert os.environ.get('DEV_MODE') == '1'


def test_dev_mode_honored_on_local_network(monkeypatch):
    monkeypatch.setenv('DEV_MODE', '1')
    assert resolve_dev_mode('local') is True
    assert os.environ.get('DEV_MODE') == '1'


def test_dev_mode_disabled_and_cleared_on_finney(monkeypatch):
    monkeypatch.setenv('DEV_MODE', '1')
    assert resolve_dev_mode('finney') is False
    # Cleared so the maintainer gates (which read os.environ directly) stay enabled.
    assert 'DEV_MODE' not in os.environ


def test_dev_mode_disabled_on_unknown_network(monkeypatch):
    monkeypatch.setenv('DEV_MODE', '1')
    assert resolve_dev_mode('wss://custom.endpoint:443') is False
    assert 'DEV_MODE' not in os.environ


def test_unset_dev_mode_is_noop(monkeypatch):
    monkeypatch.delenv('DEV_MODE', raising=False)
    assert resolve_dev_mode('finney') is False
    assert 'DEV_MODE' not in os.environ
