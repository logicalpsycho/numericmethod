from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

Charactor = ["천사","뱀","사자","말","거짓","그리핀","매료","검","까마귀","새","철학","수사학","논리학","미래","진실","인간",""]
Class = {0:"없음",1:"왕",2:"왕자",3:"공작",4:"후작",5:"백작"}
Classes = ["왕","왕자","공작","후작","백작"]
#포라스
def DescriptData():
    file = open("description", "r", encoding='UTF8')
    strings = file.readlines()
    Datas = {}
    level = 1
    StringData = []
    for i in strings:
        if i.count(":") < 1:
            break
        data = i.split(":")
        Datas[data[0]] = {}
        ClassLevel = 1
        for j in Classes:
            if data[1] == j:
                Datas[data[0]]["Class"] = ClassLevel
            ClassLevel += 1
        if Datas[data[0]].get("Class") is None:
            Datas[data[0]]["Class"] = 0
        Datas[data[0]]["Charactor"] = data[2]
        Datas[data[0]]["Level"] = level
        level += 1
        StringData.append(data[2])
    file.close()
    return Datas, StringData

def Compare(King,Other):
    CData = {}
    tfidf_vectorizer = TfidfVectorizer()
    for j in Other:
        CData[j] = {}
        for i in King:
            if King[i]["Level"]<Other[j]["Level"]:
                tfidf_matrix = tfidf_vectorizer.fit_transform((King[i]["Charactor"],Other[j]["Charactor"]))
                cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                CData[j][i] = cos_similar[0][0]
            else:
                tfidf_matrix = tfidf_vectorizer.fit_transform((King[i]["Charactor"],Other[j]["Charactor"]))
                cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                CData[j][i] = 0
                if cos_similar > 0.2:
                    CData[j][i] = cos_similar[0][0]


    return CData

def Classified():
    Data, Strings = DescriptData()
    King = {}
    Other = {}
    OtherKing = {}
    for i in Data:
        if Data[i]["Class"] == 1:
            King[i] = Data[i]
        if Data[i]["Class"] > 1:
            Other[i] = Data[i]
    CompareData = Compare(King,Other)
    for i in Other:
        max_key = max(CompareData[i], key=CompareData[i].get)
        OtherKing[i] = [max_key,CompareData[i][max_key]]
        if OtherKing[i][1]<0.09:
            OtherKing[i] = ["",0]
    Influence = {}
    for i in OtherKing:
        if Influence.get(OtherKing[i][0]) is None:
            Influence[OtherKing[i][0]] = 1
        else:
            Influence[OtherKing[i][0]] += 11
    print(Influence)
    print(OtherKing)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit(Strings)
    print(tfidf_matrix)

Classified()
