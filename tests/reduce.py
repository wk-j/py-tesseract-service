from functools import reduce


def create_detail(texts):
    title, text = texts
    return f"<detmails>{title}<summary>\n\n```\n{text}\n```\n\n</summary></details>"


texts = [("aaa", "a---"), ("bbb", "b---")]

result = [create_detail(x) for x in texts]
print(result)
