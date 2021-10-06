class Dropout:
  def __init__(self, dropout_ratio=0.5):
    self.dropout_ratio = dropout_ratio
    self.mask = None
  
  def forward(self, x, train_flg=True):
    if train_flg:
      self.mask = np.random.randn(*x.shape) > self.dropout_ratio
      # 삭제할 뉴런을 False로 표시
      # x와 형상이 같은 배열을 무작위로 생성하여, 그 값이 dropout_ratio보다 큰 원소만 True로 설정
      return x * self.mask
    
    else:
      return x * (1.0 - self.dropout_ratio)
  
  def backward(self, dout):
    # 순전파 때 신호를 통과시키는 뉴런은 역전파 때도 신호를 그대로 통과시키고,
    # 순전파 때 통과하지 못한 뉴런은 역전파 때도 신호를 차단한다.
    return dout * self.mask
  
