# -*- coding: utf-8 -*-
import warnings

import pytest

from deprecated import classic


class MyDeprecationWarning(DeprecationWarning):
    pass


_PARAMS = [None,
           ((), {}),
           (('Good reason',), {}),
           ((), {'reason': 'Good reason'}),
           ((), {'version': '1.2.3'}),
           ((), {'action': 'once'}),
           ((), {'category': MyDeprecationWarning}),
           ]


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecated_function(request):
    if request.param is None:
        @classic.deprecated
        def foo():
            pass

        return foo
    else:
        args, kwargs = request.param

        @classic.deprecated(*args, **kwargs)
        def foo():
            pass

        return foo


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecated_class(request):
    if request.param is None:
        @classic.deprecated
        class Foo(object):
            pass

        return Foo
    else:
        args, kwargs = request.param

        @classic.deprecated(*args, **kwargs)
        class Foo(object):
            pass

        return Foo


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecated_method(request):
    if request.param is None:
        class Foo(object):
            @classic.deprecated
            def foo(self):
                pass

        return Foo
    else:
        args, kwargs = request.param

        class Foo(object):
            @classic.deprecated(*args, **kwargs)
            def foo(self):
                pass

        return Foo


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecated_static_method(request):
    if request.param is None:
        class Foo(object):
            @staticmethod
            @classic.deprecated
            def foo():
                pass

        return Foo.foo
    else:
        args, kwargs = request.param

        class Foo(object):
            @staticmethod
            @classic.deprecated(*args, **kwargs)
            def foo():
                pass

        return Foo.foo


def test_classic_deprecated_function__warns(classic_deprecated_function):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecated_function()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated function (or staticmethod)" in str(warn.message)


def test_classic_deprecated_class__warns(classic_deprecated_class):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecated_class()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated class" in str(warn.message)


def test_classic_deprecated_method__warns(classic_deprecated_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = classic_deprecated_method()
        obj.foo()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated method" in str(warn.message)


def test_classic_deprecated_static_method__warns(classic_deprecated_static_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecated_static_method()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated function (or staticmethod)" in str(warn.message)


def test_should_raise_TypeError():
    try:
        classic.deprecated(5)
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_warning_msg_has_reason():
    reason = "Good reason"

    @classic.deprecated(reason=reason)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
        warn = warns[0]
        assert reason in str(warn.message)


def test_warning_msg_has_version():
    version = "1.2.3"

    @classic.deprecated(version=version)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
        warn = warns[0]
        assert version in str(warn.message)


def test_warning_is_ignored():
    @classic.deprecated(action='ignore')
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
        assert len(warns) == 0


def test_specific_warning_cls_is_used():
    @classic.deprecated(category=MyDeprecationWarning)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
        warn = warns[0]
        assert issubclass(warn.category, MyDeprecationWarning)
