from __future__ import print_function, unicode_literals

import wee_slack
import pytest


@pytest.mark.parametrize('case', (
    {
        'input': "foo",
        'output': "foo",
    },
    {
        'input': "<!channel>",
        'output': "@channel",
    },
    {
        'input': "<!everyone>",
        'output': "@everyone",
    },
    {
        'input': "<!group>",
        'output': "@group",
    },
    {
        'input': "<!here>",
        'output': "@here",
    },
    {
        'input': "<@U407ABLLW|@othernick>: foo",
        'output': "@alice: foo",
        'ignore_alt_text': True,
    },
    {
        'input': "foo <#C407ABS94|otherchannel> foo",
        'output': "foo #otherchannel foo",
    },
    {
        'input': "foo <#C407ABS94> foo",
        'output': "foo #general foo",
    },
    {
        'input': "url: <https://example.com|example> suffix",
        'output': "url: https://example.com (example) suffix",
    },
    {
        'input': "url: <https://example.com|example with spaces> suffix",
        'output': "url: https://example.com (example with spaces) suffix",
    },
    {
        'input': "url: <https://example.com|example.com> suffix",
        'output': "url: example.com suffix",
        'auto_link_display': 'text',
    },
    {
        'input': "url: <https://example.com|different text> suffix",
        'output': "url: https://example.com (different text) suffix",
        'auto_link_display': 'text',
    },
    {
        'input': "url: <https://example.com|different text> suffix",
        'output': "url: https://example.com (different text) suffix",
        'auto_link_display': 'url',
    },
    {
        'input': "url: <https://example.com|example.com> suffix",
        'output': "url: https://example.com suffix",
        'auto_link_display': 'url',
    },
    {
        'input': "<@U407ABLLW|@othernick> multiple unfurl <https://example.com|example with spaces>",
        'output': "@othernick multiple unfurl https://example.com (example with spaces)",
    },
    {
        'input': "try the #general channel",
        'output': "try the #general channel",
    },
    {
        'input': "<@U407ABLLW> I think 3 > 2",
        'output': "@alice I think 3 > 2",
    },
    {
        'input': "<!subteam^U407ABLLW|@dev> This is announcement for the dev team",
        'output': "@dev This is announcement for the dev team"
    }
))
def test_unfurl_refs(case, realish_eventrouter):
    wee_slack.EVENTROUTER = realish_eventrouter
    wee_slack.config.unfurl_auto_link_display = case.get('auto_link_display')

    result = wee_slack.unfurl_refs(
        case['input'],
        ignore_alt_text=case.get('ignore_alt_text', False)
    )
    assert result == case['output']
