import operator
import numpy as np
import itertools
import collections

# Ciphertext
word = "HRDKHUBHAAMAEQMTMZSHGBAKFUBHAASYRXUNKYUAATQCTLUTOGEWVAJGVEIIYTKIOTQRXXQVSQLISVVOCNGCUXPKPIUBOHTVKCFKWNJSEZYSSUTUOESIXKAPVFXNZHAOQTLCGYJVAEHLNNKEESQMKSHKKDFCNZSRHRDKHSDKFXVPTGMKRUPZBIKEVNYEKXMFXKFYMWYUDZDENEWNKDAOUXGPCXZDLCSNFGCMCSNUAOJDBLQTAHEWYZCHQJYKSNUWOKQKONZGOKDXGUXKEMWQMCFGUEAVKHDIIATCHVTGYMGKJMLNPCNAYKMIRWEETIYQKELEGLQOVKISFNUDAJQIQYBXQTMZSHGBAKFZRCNWRSODAFKKXWGAZGDBIUDDHCUDFRFOVSZXADSHYSGLTQBMNEMKDCFSOZSRDYLIHIAXCMGMFEIDNZKOVJEOIEFNWWQEDRLZYZIZXADSHYSGLJYFWDUAKSIOGOZOXWYPBUFEPNBIRJUJNDZJJYMURKNCIKPWLRMRIAGVSXTYNIWPROHLDHQOMBEKZURQCLQOVKISFNUAFQBHGPCLHZTPJVPXIZKLQSNVKIJAEITTNVSVWNFYVATDEMKDCTGIHKZTVGZYXTYQEDBACFMNCAHRDKHSDKFXZXXGMJOSLPSZBMOILMMWRALAFFMNXXDYFBIYQVVOHSWKGBIRJGTBYQLKIJAEQBTAXGFGAVUIJADHQKLFWRJXYFVIGGQZNBHSUIYOZALSKIABLWQNXNXKOAJAIKHXODXWORVDOGBMHOPLQJZALQJZALIKTKLENZHQAVYUEUFEVLUXHGOWNMGWXUIAHGQOMNCKFQLIPBNKVWDLNGMJCOBFKIGBYWPAHMMPQLUTOGECXITZVVAJEOIDCNWMFNLOBGQXCYFWQFWVXWRKWYGBFHJVLBAWBOUQEKHZHSZZIZARYITDCLQFPGBTJMQVSQLIHPEJONCYMZWTVJVZOBOMOHPSXMPUKVAGXIPOQUQUQBCKXZJSZAHEWYHAEMKOJCCCFBEUKVNCAWANSNXISVVOWHQGQFBGWKQEGBIFRGIZUJQWIMFANTGBHWGVAGXIPOQUQTTRMWDHDGRFENKYPZVCLNQAUBTZSRYGVGOWSVROENABMZTOHZRQFUEVPLLIODEYRYLUTOGPYAFHJFIVOSFMPBSHLEKWYWJYTFYETAZQCRFTFHOMACOQVTWKLKYMGIMQDSYNWMFNIEITWMBVVWANBQFVUSKZOTLCCWABAGHWZBZHRDKHDTUOMUUUGQICHNUUQFJYUCQUO"

dic = {}
# Ciphertext를 int 변환 결과를 담을 list
to_int = []

# Monogram frequency 및 normalized monogram frequency
mono = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 0.4, 2.4, 6.7, 1.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]
mono_normalized = [float(k/np.sum(mono)) for k in mono ]

d = 5
m = 257

# Ciphertext의 bigram frequency 확인
for idx,letter in enumerate(word):
    tmp = word[idx:idx+2]
    #print(tmp)
    if tmp in dic.keys():
        dic[tmp]+=1
    else:
        dic[tmp] =1
print(sorted(dic.items(), key=operator.itemgetter(1),reverse=True))

# Text의 scoring function
def IML(col):
    return sum([mono_normalized[i]*np.log2(mono[i]) for i in col]) * -1

# Ciphertext를 int 배열로 변환
for i in range(0, len(word)):
    to_int.append(ord(word[i]) - ord('A'))

# d번째 값들 묶음의 frequency analysis
for j in range(0, d):
    tmp = []
    for k in range(0+j, len(word), d):
        tmp.append(word[k])
    print(collections.Counter(tmp))

string_blocks = []
int_blocks = []

# Ciphertext를 5개씩 257개의 block으로 나눔
for k in range(0,len(word), d):
    string_blocks.append(word[k:k+d])
    int_blocks.append(to_int[k:k+d])

# 각 column의 Score를 담을 I_set
I_set = np.full((1,d),-1*np.inf, dtype=float)
I_set = I_set[0]
print(I_set)

# 루프를 돌 26^5개의 column vector들을 생성
X_array = list(itertools.product(range(0,26), range(0,26),range(0,26), range(0,26), range(0,26)))
del X_array[0] #모두 0인 column vector는 지워줌

# Decryption을 위한 function
def decoder(key):
    ans = ""
    for i in range(0,m):
        tmp = [k%26+ord('A') for k in np.dot(int_blocks[i], key)]
        for j in range(d):
            ans += chr(tmp[j])
    print(ans)

# Block을 string으로 바꿔주는 function
def changeTostr(block):
    ans = ""
    tmp_fun = [k+ord('A') for k in block]
    for j in range(len(tmp_fun)):
        ans+=chr(tmp_fun[j])
    return(ans)

cnt=0
# inverse key matrix의 랜덤 초기화
Key_mat = np.array([[10, 10, 12, 24, 13],
                    [9, 22, 16, 6, 1],
                    [0, 0, 17, 22, 2],
                    [8, 21, 10, 25, 10],
                    [17, 4, 9, 1, 16]])

# Text의 scoring function
def IML(col):
    return sum([mono_normalized[i]*np.log2(mono[i]) for i in col]) * -1

# 모든 X_array에 대해 scoring function을 계산해 가장 높은 column들을 Key_mat에 넣어줌
for element in X_array:
    tmp = []
    for to_intblock in int_blocks:
        tmp.append(np.dot(to_intblock, element)%26)
    iml = IML(tmp)
    for j in range(0,d):
        if I_set[j] < iml:
            Key_mat[:,j] = element
            I_set[j] = iml
            print(Key_mat)
            print(cnt)
            print(I_set)
            break
    cnt+=1

print(Key_mat)
# 5!개의 column permutation 생성 및 decrypt
perms = np.array(list(itertools.permutations(Key_mat.T)))
for ky in perms:
    ky = ky.T
    decoder(ky)