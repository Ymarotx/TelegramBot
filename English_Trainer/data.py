# from googletrans import Translator
#
# tr = Translator()
# text = tr.translate(text='приходи',dest='en')
# print(text)


# file = open('english_dict.txt', 'r')
# a = file.read()
# # print(a)
# lists = a.split(';')
# list_en = []
# list_ru = []
# end_dict = {}
# for i in lists:
#     try:
#         a = i.split(':')
#         end_dict[a[0].strip()] = a[1].strip()
#     except:
#         pass
# print(end_dict)


file = open('exm1.txt', 'r')
a = file.read()
file = open('exm2.txt', 'r')
b = file.read()
for i in range(len(a.split(' '))):
    text = a.split(" ")[i] + "==" + b.split(" ")[i]
    print(text)

