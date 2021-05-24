围绕PlatON社区[https://scan.platon.network/node]
简单的领取收益和将收益委托到节点的一个脚本
本人节点Dragon_Node多委托谢谢。代码如有问题请随时联系我792963711@qq.com。 
一切皆可计算。
PlatONet社区节点，微信:PlatONPlanet


sudo apt-get update&& sudo apt-get install gcc && sudo apt-get install python3.6-venv tmux git -y && git clone  https://github.com/zhanglonglongSH/PlatonDelegate.git&& cd ~/PlatonDelegate && python3 -m venv venv&& source ./venv/bin/activate && pip3 install -r requirements.txt
然后修改delegate.py里面的配置。

##启动节点
 tmux new -s delegate -d ~/PlatonDelegate/venv/bin/python3  delegate.py

##查看启动状态
  tmux attach -t delegate   【查看完成后 ctrl+b 然后按d退出】
