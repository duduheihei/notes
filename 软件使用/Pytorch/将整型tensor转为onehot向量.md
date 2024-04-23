```python
def onehot(t,nClass):
    onehot = torch.zeros((t.shape[0],nClass)).to(t.device)
    onehot = onehot.scatter_(1,t.unsqueeze(1).long(),1)
    return onehot
```

