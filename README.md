# Artificial_Stock_Market

#### 1.教学文件位于``tutorials``文件夹下，下载后可以在本地用jupyter打开，在coding上无法预览，想直接观看可移步我的[Github](https://github.com/jeffmxh/jupyter_notebook/blob/master/Artificial%20Market/Trader_basic.ipynb)，有时会加载失败多刷新几次即可。

#### 2.两个基础的类位于``utils``目录下

+ ``Trader_basic.py`` 定义了基本的交易者类，每个交易者初始化时会接受一个初始资产值，并根据一个指定的股价将资产随机分配一部分进入股市
+ ``Market.py`` 定义了市场的结构，初始化时传入定义的交易者类，以及交易者的数量，``.step()``方法会产生交易

#### 3.对基础交易者类的扩展方法

可以参考``Advanced_Trader.py``中的方式，对生成订单的过程重写即可，然后参照``demo.py``中的方式调用这些类进行仿真模拟。
