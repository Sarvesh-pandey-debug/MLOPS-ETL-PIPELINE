from src.math import addition,subtract
def test_add():
    assert addition(2,3)==5
    assert addition(2,4)==6
    assert addition(2,5)==7
    
def test_add():
    assert subtract(2,3)==-1
    assert subtract(2,1)==1
    assert subtract(2,2)==0   