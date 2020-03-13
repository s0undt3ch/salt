# -*- coding: utf-8 -*-
'''
    tests.unit.context_test
    ~~~~~~~~~~~~~~~~~~~~
'''
# Import python libs
from __future__ import absolute_import
import salt.ext.tornado.stack_context
import salt.ext.tornado.gen
from salt.ext.tornado.testing import AsyncTestCase, gen_test
import threading
import time

# Import Salt Testing libs
from tests.support.unit import TestCase
from salt.ext.six.moves import range

# Import Salt libs
import salt.utils.json
from salt.utils.context import ContextDict, NamespacedDictWrapper


class ContextDictTests(AsyncTestCase):
    # how many threads/coroutines to run at a time
    num_concurrent_tasks = 5

    def setUp(self):
        super(ContextDictTests, self).setUp()
        self.cd = ContextDict()
        # set a global value
        self.cd['foo'] = 'global'

    def test_threads(self):
        '''Verify that ContextDict overrides properly within threads
        '''
        rets = []

        def tgt(x, s):
            inner_ret = []
            over = self.cd.clone()

            inner_ret.append(self.cd.get('foo'))
            with over:
                inner_ret.append(over.get('foo'))
                over['foo'] = x
                inner_ret.append(over.get('foo'))
                time.sleep(s)
                inner_ret.append(over.get('foo'))
                rets.append(inner_ret)

        threads = []
        for x in range(0, self.num_concurrent_tasks):
            s = self.num_concurrent_tasks - x
            t = threading.Thread(target=tgt, args=(x, s))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        for r in rets:
            assert r[0] == r[1]
            assert r[2] == r[3]

    @gen_test
    def test_coroutines(self):
        '''Verify that ContextDict overrides properly within coroutines
        '''
        @salt.ext.tornado.gen.coroutine
        def secondary_coroutine(over):
            raise salt.ext.tornado.gen.Return(over.get('foo'))

        @salt.ext.tornado.gen.coroutine
        def tgt(x, s, over):
            inner_ret = []
            # first grab the global
            inner_ret.append(self.cd.get('foo'))
            # grab the child's global (should match)
            inner_ret.append(over.get('foo'))
            # override the global
            over['foo'] = x
            inner_ret.append(over.get('foo'))
            # sleep for some time to let other coroutines do this section of code
            yield salt.ext.tornado.gen.sleep(s)
            # get the value of the global again.
            inner_ret.append(over.get('foo'))
            # Call another coroutine to verify that we keep our context
            r = yield secondary_coroutine(over)
            inner_ret.append(r)
            raise salt.ext.tornado.gen.Return(inner_ret)

        futures = []

        for x in range(0, self.num_concurrent_tasks):
            s = self.num_concurrent_tasks - x
            over = self.cd.clone()

            f = salt.ext.tornado.stack_context.run_with_stack_context(
                salt.ext.tornado.stack_context.StackContext(lambda: over),  # pylint: disable=W0640
                lambda: tgt(x, s/5.0, over),  # pylint: disable=W0640
            )
            futures.append(f)

        wait_iterator = salt.ext.tornado.gen.WaitIterator(*futures)
        while not wait_iterator.done():
            r = yield wait_iterator.next()  # pylint: disable=incompatible-py3-code
            assert r[0] == r[1]  # verify that the global value remails
            assert r[2] == r[3]  # verify that the override sticks locally
            assert r[3] == r[4]  # verify that the override sticks across coroutines

    def test_basic(self):
        '''Test that the contextDict is a dict
        '''
        # ensure we get the global value
        assert dict(self.cd) == \
            {'foo': 'global'}

    def test_override(self):
        over = self.cd.clone()
        over['bar'] = 'global'
        assert dict(over) == \
            {'foo': 'global', 'bar': 'global'}
        assert dict(self.cd) == \
            {'foo': 'global'}
        with over:
            assert dict(over) == \
                {'foo': 'global', 'bar': 'global'}
            assert dict(self.cd) == \
                {'foo': 'global', 'bar': 'global'}
            over['bar'] = 'baz'
            assert dict(over) == \
                {'foo': 'global', 'bar': 'baz'}
            assert dict(self.cd) == \
                {'foo': 'global', 'bar': 'baz'}
        assert dict(over) == \
            {'foo': 'global', 'bar': 'baz'}
        assert dict(self.cd) == \
            {'foo': 'global'}

    def test_multiple_contexts(self):
        cds = []
        for x in range(0, 10):
            cds.append(self.cd.clone(bar=x))
        for x, cd in enumerate(cds):
            assert 'bar' not in self.cd
            with cd:
                assert dict(self.cd) == \
                    {'bar': x, 'foo': 'global'}
        assert 'bar' not in self.cd


class NamespacedDictWrapperTests(TestCase):
    PREFIX = 'prefix'

    def setUp(self):
        self._dict = {}

    def test_single_key(self):
        self._dict['prefix'] = {'foo': 'bar'}
        w = NamespacedDictWrapper(self._dict, 'prefix')
        assert w['foo'] == 'bar'

    def test_multiple_key(self):
        self._dict['prefix'] = {'foo': {'bar': 'baz'}}
        w = NamespacedDictWrapper(self._dict, ('prefix', 'foo'))
        assert w['bar'] == 'baz'

    def test_json_dumps_single_key(self):
        self._dict['prefix'] = {'foo': {'bar': 'baz'}}
        w = NamespacedDictWrapper(self._dict, 'prefix')
        assert salt.utils.json.dumps(w) == '{"foo": {"bar": "baz"}}'

    def test_json_dumps_multiple_key(self):
        self._dict['prefix'] = {'foo': {'bar': 'baz'}}
        w = NamespacedDictWrapper(self._dict, ('prefix', 'foo'))
        assert salt.utils.json.dumps(w) == '{"bar": "baz"}'
