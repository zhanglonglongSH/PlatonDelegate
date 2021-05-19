#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/19 10:34 上午 
# @Author : zhanglonglogn 
# @Version：V 0.1
# @desc
import math
import time
from datetime import datetime
import logging

from client_sdk_python import Web3, HTTPProvider
from client_sdk_python.eth import PlatON
from client_sdk_python.ppos import Ppos

# 设置领取的最小委托lat数
min_withdraw_rewarddeteg_count = 0.5
# 设置收益节点最小含有的lat数
min_withdraw_nodereward_count = 2
# 设置间隔时间
sleep_time_seconds = 60*30
# 设置委托地址信息表

addr_list=[
    {
        # 委托收益信息  bf_privkey：钱包私钥  address：钱包地址
        'benifit_addr_privkey':[
            {'bf_privkey':'92b7294ea5cc7a4de4fada550d1519ef5f5cb009bc2f4e16c5a33987e4607cbbe','address':'lat1nymlzwgnzega44n7krcc6fmg2x2yjfzjkv2e6h'},
            {'bf_privkey':'12cc9fadfe743e4f387ba9effdd5aed438ec3795d5416a203c04a2c49ba5774d6','address':'lat1x7jqhdwydce64q0kmpafzylevxww8ymdvzez8w'},
            {'bf_privkey':'bf2fddfb0215581b21eed8b3dfb9f65f22098cb6135277c40e82c46934b46e2e81','address':'lat1g00wa9vph9hm5y4434gpuutyj2dcxkvy4fzlqy'},
        ],
        # 节点id
        'node_id':"95cae658a18c6b1334a205cdb76599ca810907d8f33f737fa41cbdaba39997112d7f8f46c56c1abcda8d5129eb1d7d494305802300fdd33f10dc6d92f7118574"
    }
]


def deal( ppos, platon, addr_list):
    for addr_obj in addr_list:
        node_id = addr_obj.get("node_id")
        benifit_addr_privkey = addr_obj.get("benifit_addr_privkey")
        for benifit_addr_privkey_obj in benifit_addr_privkey:
            address = benifit_addr_privkey_obj.get("address")
            bf_privkey = benifit_addr_privkey_obj.get("bf_privkey")
            if(Web3.isAddress(address) == True):
                logging.error("错误地址address：".address)
                continue;

            logging.info(f'⏰开始查询委托收益')
            # 获取委托收益
            reword_ret = ppos.getDelegateReward(address)
            if(reword_ret.get('Code') == 0):
                ret_info = reword_ret.get('Ret');
                for nd_if in ret_info:
                    if( nd_if.get('reward') >= min_withdraw_rewarddeteg_count ):
                        ret_withdraw = ppos.withdrawDelegateReward(bf_privkey);
                        logging.info("🕐领取成功！")
            else:
                logging.error(f'🤷‍♂️ Parse error:委托收益获取失败!!')

            logging.info(f'开始查询钱包')
            # 查看钱包剩余币
            remain_lat  = math.floor((platon.getBalance(address)/(10**18)) - 0.4);
            if(remain_lat > min_withdraw_nodereward_count):
                ret_deleg = ppos.delegate(0, node_id, remain_lat*10**18, bf_privkey)
                if(ret_deleg.get('code') == 0):
                    logging.info("🕐委托成功。")
                else:
                    logging.error(f'🤷‍♂️ Parse error:节点地址委托失败!!')

# 设置网络
w3 = Web3(HTTPProvider("http://47.241.98.219:6789"),chain_id=210309);
ppos = Ppos(w3);
platon = PlatON(w3);

while True:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        deal(ppos,platon,addr_list);
        time.sleep(sleep_time_seconds)
    except (TypeError, Exception) as parseErr:
        logging.error(f'🤷‍♂️ Parse error: {parseErr}', print_mode="warning")
        time.sleep(10)


