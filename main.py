import Levenshtein
from lxml import etree
import requests


def get_dom_tree(html: str):
    dom = etree.HTML(html)
    res = traverse(dom)
    return res

# 遍历dom树
def traverse(node):
    string = ''
    single = ["a", 'img', 'meta', 'link', 'script']
    for p in node.iterchildren():
        # 遍历当前节点下的所有子节点
        if isinstance(p.tag, str):
            # 过滤掉注释等乱七八糟的内容
            if p.tag == "br":
                continue
            if len(p) > 0:
                string += f"<{p.tag}>{traverse(p)}</{p.tag}>"
            elif p.tag in single:
                string += f"<{p.tag}>"
            else:
                string += f"<{p.tag}></{p.tag}>"
    return string

# 计算汉明距离
def hamming_distance(str1, str2):
    diff = 0
    for ch1, ch2 in zip(str1, str2):
        diff += bin(ord(ch1) ^ ord(ch2)).count('1')
    return diff

def compare_tree_structure(tree1, tree2):
    """比较两个dom树的相似度"""
    distance = Levenshtein.distance(tree1, tree2)
    max_distance = max(len(tree1), len(tree2))
    similarity = 1 - (distance / max_distance)
    return similarity


if __name__ == '__main__':
    raw = requests.get("https://beyoglueye.com/jvi.aspx?pdir=beyoglu&plng=eng&list=pub")
    tree1 = get_dom_tree(raw.text)
    raw = requests.get("https://www.baidu.com/")
    tree2 = get_dom_tree(raw.text)
    compare_tree_structure(tree1,tree2)
