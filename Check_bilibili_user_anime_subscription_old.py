import requests;
import sys;

f = open ("temp.txt", "w+", encoding = "utf-8");

UTFU1 = "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword=";
UTFU2 = "https://api.bilibili.com/x/space/acc/info?mid=";
url = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid=";
headers = {'User-agent':'Mozilla/5.0'};

choice = int (input ("Would you like to search [1]Username or [2]Uid?  Type in '1' or '2'.  Input = "));

if (choice == 1):
    username = input ("username = ");
    UTFU1 += username;
    Ures = requests.get (url = UTFU1, headers = headers);
    Ures.encoding = "utf-8";
    Uloc1 = Ures.text.find ('"type":"bili_user"');
    if (Uloc1 == -1):
        print ("Cannot find this user.");
        f.close ();
        sys.exit (1);
    Uloc1 += 25;
    Uloc2 = Ures.text.find (",", Uloc1);
    uid = Ures.text[Uloc1:Uloc2];

elif (choice == 2):
    uid = input ("uid = ");
    UTFU2 += uid;
    Ures = requests.get (url = UTFU2, headers = headers);
    Ures.encoding = "utf-8";
    Uloc1 = Ures.text.find ('"name":');
    if (Uloc1 == -1):
        print ("Some unknown errors have occurred.");
        f.close ();
        sys.exit (1);
    Uloc1 += 8;
    Uloc2 = Ures.text.find ('"', Uloc1);
    username = Ures.text[Uloc1:Uloc2];

else:
    print ("The entered number cannot be recognized.");
    f.close ();
    sys.exit (1);

f.write ("username = " + username + ", ");
f.write ("uid = " + uid + ":\n");

times = 0;
head = 0;

while (True):
    times += 1;
    FU = url + uid + "&pn=" + str (times);
    res = requests.get (url = FU, headers = headers);
    res.encoding = "utf-8";
    exist = res.text.find ('"season_type_name":"番剧"');
    if (exist == -1):
        if (times == 1):
            print ("User privacy settings are not public.");
            f.write("User privacy settings are not public.");
        break;
    head = 0;
    while (True):
        loc1 = res.text.find ('"season_type_name":"番剧"', head);
        if (loc1 == -1):
            break;
        loc1 += 33;
        loc2 = res.text.find ('"', loc1);
        f.write (res.text[loc1:loc2] + "\n");
        head = loc2 + 1;
f.write ("\n\n");
print ("Finished.");

f.flush ();
f.close ();
sys.exit (0);