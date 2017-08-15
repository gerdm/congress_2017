import pyqrcode

testqr = pyqrcode.create("dY = df/dt dt + df/dx dX + d2f/dx2 (dX)2")
testqr.png("test_example.png", scale=30)
