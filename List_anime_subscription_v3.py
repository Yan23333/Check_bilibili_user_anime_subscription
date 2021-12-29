# 练习用class写得花里胡哨的

import requests;
import json;
import sys;
import os;

f = open ("data.txt", "w+", encoding = "utf-8");
headers = {"User-agent":"Mozilla/5.0"};

class GetUid (object):
    def __init__ (self):
        pass;
    def UN (self):
        url = "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword=";
        username = input ("用户名: ");
        url += username;
        res = requests.get (url = url, headers = headers);
        res.encoding = "utf-8";
        data = json.loads (res.text);
        if (data["data"]["numResults"] == 0):
            print ("找不到此用户");
            f.close ();
            sys.exit (1);
        uid = str (data["data"]["result"][0]["mid"]);
        return uid;
    def ID (self):
        uid = input ("uid: ");
        return uid;

class GetData (object):
    def __init__ (self, uid):
        self.uid = uid;
    def BasicUserProfile (self):
        url = "https://api.bilibili.com/x/space/acc/info?mid=";
        url += self.uid;
        res = requests.get (url = url, headers = headers);
        res.encoding = "utf-8";
        data = json.loads (res.text);
        if (data["code"] != 0):
            print ("找不到此用户");
            f.close ();
            sys.exit (1);
        f.write ("用户名: " + data["data"]["name"] +", uid: " + str (data["data"]["mid"]) + ";\n\n追番列表:\n");
    def bangumi (self):
        pages = 0;
        records = 0;
        while (True):
            pages += 1;
            url = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid=";
            url = url + self.uid + "&pn=" + str (pages);
            res = requests.get (url = url, headers = headers);
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

op_input = GetUid ();
input_choice = input ("你想以哪种方式进行找到该用户?\n[1]用户名 [2]用户uid (受限于b站搜索机制, 使用用户名搜索的结果可能与预期不一致)\n");
if (input_choice == "1"):
    uid = op_input.UN ();
elif (input_choice == "2"):
    uid = op_input.ID ();
else:
    print ("输入的字符不能被识别");
    f.close ();
    sys.exit (1);

op_process = GetData (uid);
op_process.BasicUserProfile ();
op_process.bangumi ();

f.write ("\n\n");
print ("完成! 已自动打开输出的txt文件 (位于同目录下的data.txt)");

f.flush ();
f.close ();
os.system ("data.txt");
sys.exit (0);
