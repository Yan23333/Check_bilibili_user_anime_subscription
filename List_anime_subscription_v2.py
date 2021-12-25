import requests;
import json;
import sys;

f = open ("temp.txt", "w+", encoding = "utf-8");

UTFU1 = "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword="; #搜索用户url
UTFU2 = "https://api.bilibili.com/x/space/acc/info?mid="; #用户信息页
url = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid="; #用户追番列表
headers = {'User-agent':'Mozilla/5.0'};

input_choice = input ("你想以哪种方式进行找到该用户?\n[1]用户名 [2]用户uid (受限于b站搜索机制, 使用用户名搜索的结果可能与预期不一致)\n");

if (input_choice == "1"):
    username = input ("用户名: ");
    UTFU1 += username;
    Ures = requests.get (url = UTFU1, headers = headers);
    Ures.encoding = "utf-8";
    Udata = json.loads (Ures.text);
    if (Udata["data"]["numResults"] == 0):
        print ("找不到此用户");
        f.close ();
        sys.exit (1);
    uid = str (Udata["data"]["result"][0]["mid"]);

elif (input_choice == "2"):
    uid = input ("uid: ");

else:
    print ("输入的字符不能被识别");
    f.close ();
    sys.exit (1);

UTFU2 += uid;
Pres = requests.get (url = UTFU2, headers = headers);
Pres.encoding = "utf-8";
Pdata = json.loads (Pres.text);
if (Pdata["code"] != 0):
    print ("找不到此用户");
    f.close ();
    sys.exit (1);
f.write ("用户名: " + Pdata["data"]["name"] +", uid: " + str (Pdata["data"]["mid"]) + ", 性别: " + Pdata["data"]["sex"] + ";\n\n追番列表:\n");

pages = 0;
records = 0;

while (True):
    pages += 1;
    FU = url + uid + "&pn=" + str (pages);
    res = requests.get (url = FU, headers = headers);
    res.encoding = "utf-8";
    data = json.loads (res.text);
    if (data["code"] == 53013):
        print ("用户隐私设置未公开");
        f.write("用户隐私设置未公开");
        break;
    for i in range (0, len (data["data"]["list"])):
        records += 1;
        f.write (str (records) + ". " + data["data"]["list"][i]["title"] + "\n");
    if (data["data"]["pn"] * 15 >= data["data"]["total"]):
        break;
f.write ("\n\n");
print ("完成! (数据已输入到同目录下的temp.txt)");

f.flush ();
f.close ();
sys.exit (0);
