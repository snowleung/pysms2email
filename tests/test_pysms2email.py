import sms2email

def test_build_content():
    date = sms2email.message_date(1)
    test_data = [(1, 'author', 'text')]
    assert '''Author:author\nTEXT:\ntext\n'''+str(date)+'''\n\n\n''' == sms2email.build_content(test_data)

def test_run_diagnostic():
    assert sms2email.run_diagnostic()
