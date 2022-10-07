## tf 1.9
```
pip install tensorflow==1.9 tensorflow-gpu==1.9
conda install cudatoolkit=9.2
conda install cudnn
pip install keras==2.2.0
pip install matplotlib==3.2
pip install numpy==1.14.5
pip install opencv-python==3.4.0
```

```
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
```


## TF 1.14
```
pip install tensorflow-gpu==1.14
conda install cudatoolkit=10.0
conda install cudnn
pip install keras==2.2.5
pip install numpy==1.16.5
pip install matplotlib==3.4
pip install opencv-python==3.4.2.17
```