import tools


def test_config_works_inside_context():
    with tools.Config() as cfg:
        cfg.C['a'] = 1
    with open('config.json', 'r') as fl:
        j1 = tools.json.load(fl)
    with tools.Config() as cfg:
        cfg.C['a'] = 2
    with open('config.json', 'r') as fl:
        j2 = tools.json.load(fl)
    assert j1['a'] != j2['a']
    with tools.Config() as cfg:
        cfg.pop('a')


def test_letter_returns_random_string():
    assert tools.letter() != tools.letter()
