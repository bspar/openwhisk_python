#!/usr/bin/env python3

from url_generator import UrlGenerator

urls0 = ['https://localhost/api/v1/namespaces/_/' + x for x in (
    'actions',
    'actions?skip=1&limit=2',
    'actions/n+A+m+E',
    'actions/n+A+m+E?blocking=False',
    'actions/n+A+m+E?overwrite=True',

    'activations',
    'activations?name=docs=True&n+A+m+E',
    'activations?skip=1&limit=2',
    'activations?since=77&upto=99999999',
    'activations/activation_id',
    'activations/activation_id/logs',
    'activations/activation_id/result',

    'packages',
    'packages?public=True',
    'packages?skip=1&limit=2',
    'packages/n+A+m+E',
    'packages/n+A+m+E?overwrite=True',

    'rules',
    'rules?skip=1&limit=2',
    'rules/n+A+m+E?state=disabled',
    'rules/n+A+m+E?overwrite=True',

    'triggers',
    'triggers?skip=1&limit=2',
    'triggers/n+A+m+E?state=disabled',
    'triggers/n+A+m+E?overwrite=True')]


# print(urls0)

gen = UrlGenerator()
urls1 = [
    gen.url_action(),
    gen.url_action(skip=1, limit=2),
    gen.url_action('n A m E'),
    gen.url_action('n A m E', blocking=False),
    gen.url_action('n A m E', overwrite=True),

    gen.url_activation(),
    gen.url_activation(name='n A m E', docs=True),
    gen.url_activation(skip=1, limit=2),
    gen.url_activation(since=77, upto=99999999),
    gen.url_activation('activation_id'),
    gen.url_activation('activation_id', 'logs'),
    gen.url_activation('activation_id', 'result'),

    gen.url_package(),
    gen.url_package(public=True),
    gen.url_package(skip=1, limit=2),
    gen.url_package('n A m E'),
    gen.url_package('n A m E', overwrite=True),

    gen.url_rule(),
    gen.url_rule(skip=1, limit=2),
    gen.url_rule('n A m E', state='disabled'),
    gen.url_rule('n A m E', overwrite=True),

    gen.url_trigger(),
    gen.url_trigger(skip=1, limit=2),
    gen.url_trigger('n A m E', state='disabled'),
    gen.url_trigger('n A m E', overwrite=True)]


for x, y in zip(urls0, urls1):
    print('\n'.join((x, y)))
    assert x == y
