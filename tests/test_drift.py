import drift


def test_definition():
    assert drift.Drift


def test_get_change_ids():
    drifter = drift.Drift('.')
    assert drifter


class Commit(object):
    def __init__(self, message):
        self.message = message


def extract_id_helper(message, change_id):
    commit = Commit(message)
    c, cid = drift.Drift._extract_change_id(commit)
    assert c is commit
    assert cid == change_id


def test_extract_id():
    extract_id_helper('Message', None)
    change_id = 'Iaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    extract_id_helper('messsage\nchange-id: %s' % change_id, change_id)
    extract_id_helper('m\ne\nsssage\nchange-id: %s\n' % change_id, change_id)
    extract_id_helper('messsage\nChange-Id:%s' % change_id, change_id)
    extract_id_helper('messsage\nchange-ID: %s' % change_id, change_id)
    extract_id_helper('messsage\nCHANGE-id:%s' % change_id, change_id)
    change_id = 'bad'
    extract_id_helper('messsage\nchange-ID: %s' % change_id, None)
    extract_id_helper('messsage\nCHANGE-id:%s' % change_id, None)
