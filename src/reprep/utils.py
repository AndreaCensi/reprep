from contracts import new_contract

@new_contract  
def valid_id(s):
    assert isinstance(s, str)
    assert len(s)
    assert not '/' in s     
