from urllib import request, parse
from http import cookiejar
import threading

stu_name = "student1@test.com"
stu_pwd = "password"

tea_name = "teacher1@test.com"
tea_pwd = "password"

admin_name = "admin@test.com"
admin_pwd = "password"

base_url = "https://liqing16-ashen67.cs50.io/"

user_name = stu_name
pwd = stu_pwd


class Performance_test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cj = cookiejar.CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cj))

    def run(self):
        url = base_url + "sessions/login"

        response = self.opener.open(url)
        # page = response.
        line = response.readline()
        key = "authenticity_token"
        token = ""
        while line:
            line = line.decode('utf-8')
            if "form" in line and key in line:
                number = line.find(key)
                line = line[number:]
                token = line.split('\"')[2]
                print(token)
                break
            line = response.readline()

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
            "Referer": "https://liqing16-ashen67.cs50.io/sessions/login",
            "Connection": "keep-alive"
        }

        form = {"utf8": "✓", "authenticity_token": token, "session[email]": user_name,
                "session[password]": pwd, "session[remember_me]": "0", "button": ""}

        data = parse.urlencode(form).encode('utf-8')

        req = request.Request(url, data, headers)

        response = self.opener.open(req)
        r = response.read().decode('utf-8')

        thread = threading.current_thread()
        name = thread.getName()

        print(name, " : ", response.getcode())


if __name__ == '__main__':
    threads = []
    number = 5
    try:
        for i in range(number):
            t = Performance_test()
            # t = threading.Thread(target=Performance_test.login(pt))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        print("all threads finish!!")
    except Exception as e:
        print("some thread failed!!")
