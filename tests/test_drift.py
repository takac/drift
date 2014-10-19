import drift
import mock


def test_definition():
    assert drift.Drift
    drifter = drift.Drift('.')
    assert drifter


def extract_id_helper(message, change_id):
    commit = mock.MagicMock(message=message)
    cid = drift.Drift._extract_change_id(commit)
    assert cid == change_id


def test_extract_id():
    extract_id_helper('Message', None)
    change_id = 'Iaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    extract_id_helper('messsage\nchange-id: %s' % change_id, change_id)
    extract_id_helper('m\ne\nsssage\nchange-id: %s\n' % change_id, change_id)
    extract_id_helper('messsage\nChange-Id:%s' % change_id, change_id)
    extract_id_helper('messsage\nchange-ID: %s' % change_id, change_id)
    extract_id_helper('messsage\nCHANGE-id:%s' % change_id, change_id)
    extract_id_helper('messsage\nCHANGE-id:%s\nBug: 13131'
                      % change_id, change_id)
    extract_id_helper("This can cause docs jobs to fail if\n"
                      "warnings.\n\n"
                      "Change-Id: I71f941e2a639641a662a163c682eb86d51de42fb\n"
                      "Related-Bug: #1368910",
                      "I71f941e2a639641a662a163c682eb86d51de42fb")
    change_id = 'bad'
    extract_id_helper('messsage\nchange-ID: %s' % change_id, None)
    extract_id_helper('messsage\nCHANGE-id:%s' % change_id, None)
    extract_id_helper('messsage\nCHANGE-id:%s\nBug: fff' % change_id, None)


def test_get_change_ids():
    drifter = drift.Drift('.')
    drifter.repo = mock.MagicMock()

    change_id = 'Iaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa%s'
    message = ('Message here...\nChange-Id: %s' % change_id)
    not_id_message = ('Message here... %s' % change_id)
    commits = [mock.MagicMock(message=message % i) for i in range(5)]
    commits.extend(mock.MagicMock(message=not_id_message % i)
                   for i in range(5))
    commits.extend(mock.MagicMock(message=message % i) for i in range(5, 10))

    drifter.repo.iter_commits.return_value = commits
    result = drifter.change_ids('master')
    drifter.repo.iter_commits.assert_called_once_with('master')
    assert len(result) == 10
    for idx, i in enumerate(sorted(result)):
        assert i == change_id % idx
