import requests;
import sys;

f = open ("temp.txt", "w+", encoding = "utf-8");

UTFU1 = "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword="; #搜索用户url
UTFU2 = "https://api.bilibili.com/x/space/acc/info?mid="; #用户信息页
url = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid="; #用户追番列表
headers = {'User-agent':'Mozilla/5.0'};

choice = int (input ("你想以哪种方式进行找到该用户?\n[1]用户名 [2]用户uid\n"));

if (choice == 1):
    username = input ("用户名: ");
    UTFU1 += username;
    Ures = requests.get (url = UTFU1, headers = headers);
    Ures.encoding = "utf-8";
    Uloc1 = Ures.text.find ('"type":"bili_user"'); #暴力字符串搜索
    if (Uloc1 == -1):
        print ("找不到此用户");
        f.close ();
        sys.exit (1);
    Uloc1 += 25;
    Uloc2 = Ures.text.find (",", Uloc1);
    uid = Ures.text[Uloc1:Uloc2];

elif (choice == 2):
    uid = input ("uid: ");
    UTFU2 += uid;
    Ures = requests.get (url = UTFU2, headers = headers);
    Ures.encoding = "utf-8";
    Uloc1 = Ures.text.find ('"name":'); #暴力字符串搜索
    if (Uloc1 == -1):
        print ("发生了未知错误");
        f.close ();
        sys.exit (1);
    Uloc1 += 8;
    Uloc2 = Ures.text.find ('"', Uloc1);
    username = Ures.text[Uloc1:Uloc2];

else:
    print ("输入的字符不能被识别");
    f.close ();
    sys.exit (1);

f.write ("用户名: " + username + ", ");
f.write ("uid: " + uid + ":\n");

pages = 0;
head = 0;

while (True):
    pages += 1; #页码+1
    FU = url + uid + "&pn=" + str (pages);
    res = requests.get (url = FU, headers = headers);
    res.encoding = "utf-8";
    exist = res.text.find ('"season_type_name":"番剧"'); #暴力字符串搜索
    if (exist == -1):
        if (pages == 1):
            print ("用户隐私设置未公开");
            f.write("用户隐私设置未公开");
        break;
    head = 0;
    while (True):
        loc1 = res.text.find ('"season_type_name":"番剧"', head); #从前一次搜索到的地方往后搜索
        if (loc1 == -1): #当前页面番剧扫描完毕跳出循环
            break;
        loc1 += 33;
        loc2 = res.text.find ('"', loc1);
        f.write (res.text[loc1:loc2] + "\n");
        head = loc2; #记录当前搜索的地方
f.write ("\n\n");
print ("完成");

f.flush ();
f.close ();
sys.exit (0);
