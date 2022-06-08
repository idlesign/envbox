from envbox import Environment
from envbox.utils import cast_type, read_envfile


def test_cast_type():

    assert cast_type('1.a0') == '1.a0'
    assert cast_type('some') == 'some'
    assert cast_type('10') == 10
    assert cast_type('True') is True


def test_read_envfile(datafix_dir):

    env = Environment()
    env['ENVBOXTST_CHANGE'] = 'this'

    entries = read_envfile(datafix_dir / '.env')

    assert len(entries) == 10
    assert entries['ENVBOXTST_MYQUOTED1'] == 'some quoted '
    assert entries['ENVBOXTST_MYQUOTED2'] == 'some "2" quoted'
    assert entries['ENVBOXTST_MYVAL2'] == 'enim'
    assert entries['ENVBOXTST_MYVAL1'] == 'mine'

    assert entries['ENVBOXTST_MYKEY'].splitlines() == [
        '-----BEGIN PGP PUBLIC KEY BLOCK-----',
        'Version: GnuPG v1',
        '',
        'mQENBFoSTEEBCAC5LEn4+Uqd2V0D7/BOnEaUVdlfrpnW++FKK2ZX7OGc7PrW+xfA',
        'NOQ0M+zUiK0xEF7wydsAMBujVQkrDzTQXQSlN1KpkBqkjLAzLpb46FrZi+3Da/3J',
        '2XbrJeMDQMngxmP8p0zU6OAYFk4KzhLx0+7IKR2HC6lAJjIxHmVHk2VYFQ==',
        '=UHGy',
        '-----END PGP PUBLIC KEY BLOCK-----',
    ]
    assert entries['ENVBOXTST_MULTI2'] == 'here\nthere'
    assert entries['ENVBOXTST_MULTI3'] == 'three\nfour=4"5\nfive '
    assert entries['ENVBOXTST_NONMULTI'] == '"nobrake\\n'

    assert entries['ENVBOXTST_OTHER'] == 'mine this $VAL enim'

    del env['ENVBOXTST_CHANGE']
