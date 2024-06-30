#!/usr/bin/env python3
import sys
import os
from typing import List


custom_node_list_url = "https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json"


def get_custom_node_list():
    import requests
    response = requests.get(custom_node_list_url)
    if response.status_code == 200:
        return response.json().get('custom_nodes', [])
    return []


def more_custom_nodes():
    custom_node_list = get_custom_node_list()
    custom_node_all = []
    for item in custom_node_list:
        all_url = item['reference']
        dir_name = all_url.split('/')[-1].replace('.git', '')
        custom_node_all.append({
            "label": item['title'],
            "description": item['description'],
            "cmd": f"git clone {item['reference']} /root/ComfyUI/custom_nodes/{dir_name}"
        })
    return custom_node_all


menu = [
    {
        "label": "ComfyUI",
        "description": "ComfyUI",
        "sub": [
            {
                "label": "安装自定义节点",
                "description": "install custom nodes",
                "sub": [
                    {
                        "label": "安装翻译节点",
                        "description": "install AIGODLIKE-ComfyUI-Translation",
                        "cmd": "git clone https://github.com/AIGODLIKE/AIGODLIKE-ComfyUI-Translation /root/ComfyUI/custom_nodes/AIGODLIKE-ComfyUI-Translation"
                    },
                    {
                        "label": "更多自定义节点",
                        "description": "install custom nodes",
                        "sub": more_custom_nodes
                    }
                ]
            },
            {
                "label": "启动ComfyUI",
                "description": "start up comfyui",
                "cmd": "python /root/ComfyUI/main.py"
            },
            {
                "label": "安装ComfyUI",
                "description": "install comfyui",
                "cmd": "git clone https://github.com/comfyanonymous/ComfyUI /root/ComfyUI"
            },
            {
                "label": "安装ComfyUI(Manager|Translation)",
                "description": "install comfyui",
                "cmd": '''git clone https://github.com/comfyanonymous/ComfyUI /root/ComfyUI;
                    git clone https://github.com/AIGODLIKE/AIGODLIKE-ComfyUI-Translation /root/ComfyUI/custom_nodes;
                        git clone https://github.com/ltdrdata/ComfyUI-Manager /root/ComfyUI/custom_nodes'''
            },
            {
                "label": "更新ComfyUI",
                "description": "update comfyui",
                "cmd": "git -C /root/ComfyUI pull"
            },
        ]
    },
    {
        "label": "更新版本",
        "description": "更新版本",
        "cmd": "git -C /root/autodl-scripts pull"
    },
    {
        "label": "使用代理",
        "description": "在autodl中使用代理",
        "cmd": "source /etc/network_turbo"
    },
    {
        "label": "停止代理",
        "description": "停止代理",
        "cmd": "export http_proxy=;export https_proxy="
    }
]


if __name__ == '__main__':

    try:
        import inquirer
    except ImportError:
        os.system('pip install inquirer')
        import inquirer

    current_labal = 'main'

    def get_current_menu(_menu):
        if current_labal == 'main':
            return _menu
        for item in _menu:
            if item['label'] == current_labal:
                return item['sub']

        for item in _menu:
            if 'sub' in item:
                sub_menu = get_current_menu(item['sub'])
                if sub_menu:
                    return sub_menu
        return None

    while True:
        choices = []
        current_menu = get_current_menu(menu)

        # 判断是否是函数，如果是函数则执行
        if callable(current_menu):
            current_menu = current_menu()
        for item in current_menu:
            choices.append(item['label'])
        if current_labal != 'main':
            # 增加返回选项在开头
            choices.insert(0, '返回')
        questions = inquirer.List(
            current_labal, message=item["description"], choices=choices,)
        answers1 = inquirer.prompt([questions])
        selected_label = answers1[current_labal]
        if selected_label == '返回':
            current_labal = 'main'
        else:
            for item in current_menu:
                if item['label'] == selected_label:
                    if 'cmd' in item:
                        print(f"执行命令: {item['cmd']}")
                        os.system(item['cmd'])
                    if 'sub' in item:
                        current_labal = selected_label
                    break
