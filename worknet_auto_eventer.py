import time
import requests
from bs4 import BeautifulSoup

apply_url="http://www.work.go.kr/event/eventApplyProcess.do"
login_url="https://www.work.go.kr:443/member/login.do"
event_url="http://www.work.go.kr/event/eventContent.do?eventNo=514"
main_url="http://www.work.go.kr/seekMain.do"
myid=""
mypwd=""
gift_num=0
count=0
wait_time=0
def auto_apply():
    try:
        params={"custId":myid,"pwd":mypwd,"redirectUrl":"/seekMain.do","custClcd":"P"}
        session=requests.Session()
        site=session.post(login_url,params)
        site=session.get(event_url)
        
        
        temp=0
        suc=0
        while(1):
            temp+=1
            print("문서를 파싱합니다")
            html=BeautifulSoup(site.text,"html.parser")
            if (len(html.find_all("div",class_="state v2")))>0 :
                suc+=1
                token=html.find("input",{"name":"worknetEventToken514'/>"})["value"]
                params={"gov.keis.token.field":"worknetEventToken514'/>","worknetEventToken514'/>":token,"eventNo":"514","eventGiftNo":gift_num,"infoAgreeYn":"Y"}
                session.post(apply_url,params)
                print(str(suc)+" 번째 응모했습니다")
                
                time.sleep(2)
            elif (len(html.find_all("div",class_="state")))>0:
                clock=html.find(id="countdown").text
                if clock.find("분")==-1:
                    wait_time=int(clock[0:clock.find("초")])
                else:
                    wait_time=int(clock[0:clock.find("분")])*60+int(clock[clock.find("분")+2:clock.find("초")])
                print(str(wait_time)+" 초 기다려야 합니다")
                time.sleep(wait_time)
                break;
            else:
                if temp>5:
                    print("프로그램에 이상이 있습니다")
                    break;
                else:
                    time.sleep(3)
    except:
        global count+=1
        print(str(count)+"번 오류 발생했습니다")
        time.sleep(3)
        auto_apply
        
#print(site.text)
myid=input("워크넷 아이디를 입력해주세요: ")
mypwd=input("워크넷 비밀번호를 입력해주세요: ")
gift_num=input("경품 번호를 입력하세요(기어핏은 2번임): ")
while(1):
    print("자동지원 시작합니다")
    
    auto_apply()
    
