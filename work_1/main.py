# import sys
# import re
#
# def calculate_similarity(original_file, plagiarized_file):
#     with open(original_file, 'r', encoding='utf-8') as file1, open(plagiarized_file, 'r', encoding='utf-8') as file2:
#         original_text = file1.read()
#         plagiarized_text = file2.read()
#
#         # 去除标点符号和空格
#         original_text = re.sub(r'[^\w\s]', '', original_text)
#         plagiarized_text = re.sub(r'[^\w\s]', '', plagiarized_text)
#
#         # 转为小写
#         original_text = original_text.lower()
#         plagiarized_text = plagiarized_text.lower()
#
#         # 计算重复率
#         total_words = len(original_text.split())
#         common_words = 0
#
#         for word in plagiarized_text.split():
#             if word in original_text.split():
#                 common_words += 1
#         print(plagiarized_text.split())
#         print(original_text.split())
#         similarity = common_words / total_words * 100
#         return similarity
#
# def save_similarity(similarity, output_file):
#     with open(output_file, 'w', encoding='utf-8') as file:
#         file.write(f'重复率：{similarity:.2f}%')
#
# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print('请输入正确的命令行参数：原文文件路径、抄袭版文件路径、输出文件路径')
#         sys.exit(1)
#
#     original_file = sys.argv[1]
#     plagiarized_file = sys.argv[2]
#     output_file = sys.argv[3]
#
#     similarity = calculate_similarity(original_file, plagiarized_file)
#     save_similarity(similarity, output_file)
#     print(f'重复率：{similarity:.2f}% 已保存到 {output_file}')


import jieba
import gensim
import sys
import re



# 获取指定路径的文件内容
def get_file_contents(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


# 将读取到的文件内容先进行jieba分词，然后再把标点符号、转义符号等特殊符号过滤掉
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[0-9\u4e00-\u9fa5]", tags)):
            result.append(tags)
        else:
            pass
    return result


# 传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


if __name__ == '__main__':
    if len(sys.argv) != 4:
            print('请输入正确的命令行参数：原文文件路径、抄袭版文件路径、输出文件路径')
            sys.exit(1)

    path1 = sys.argv[1]  # 论文原文的文件的绝对路径（作业要求）
    path2 = sys.argv[2]  # 抄袭版论文的文件的绝对路径
    save_path = sys.argv[3]  # 输出结果绝对路径
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    print("文章相似度： %.4f" % similarity)
    # 将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.4f" % similarity)
    f.close()

