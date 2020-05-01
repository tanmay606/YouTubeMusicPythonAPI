import threading
from time import sleep
from selenium import common
from selenium.webdriver import Chrome;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;

class YoutubeMusic(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
        self.FirstTime = True;
        self.IncreaseTime = 30;
        self.DecreaseTime = 30;
        self.user_agent = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
        self.options = Options();
        self.CompletelyLoaded = True;
        self.options.add_argument(self.user_agent);
        self.options.add_argument('--headless');
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--log-level=3')
        self.Browser = Chrome(r'c:\windows\chromedriver.exe',options=self.options);
        #our browser is read to shoot.
    def HelpMenu(self):
        ProgramBanner="""

        [>] Youtube Music Command Line Application.
        
        Written In Python, Using Selenium Framework.

        Written By : Tanmay Upadhyay
        Email : kevinthemetnik@gmail.com
        Instagram : _tanmay_upadhyay_


        [IN MAIN MENU ]
        1.) Simply Put Song Name

        Special Commands : 

        2.) =forward  : Move Current Video Backward ,For Specific Time (=forward:time in sec EG: =forward:35)
        3.) =backward : Move Current Video Backward, For Specific Time (=forward:time in sec EG: =backward:35)
        4.) =restart : It Will Restart The Current Video.
        5.) =pause : It Will Pause The Current Video.
        6.) =play : It Will Play The Pause Video.
        7.) =refresh : It Will Refresh The Page.
        8.) =quit : Closes The Program.
        9.) =? / =HELP / =help : Help.

        [IN SONG SELECTION MENU ]

        9 : Back To Main Menu.
        """
        self.FirstTime = False
        print(ProgramBanner);
    def NavigateYoutube(self,MusicName):
        #!t Will Navigate On Youtube Website.
        self.MusicName = MusicName;
        self.CompletelyLoaded = False
        print("[Loading %s On Youtube . . . ]"%self.MusicName);
        self.Browser.get("https://m.youtube.com/results?search_query=%s"%self.MusicName);
        self.Browser.implicitly_wait(5);
    def ListVideos(self):
        self.Counter = 1;
        self.Videos = [];
        for eachVid in range(1,4):
            self.xpath = "/html/body/ytm-app/div[3]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4/span"%eachVid;
            self.EachVideo = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.XPATH,self.xpath)))
            self.EachVideo=self.EachVideo.text;
            #self.EachVideo = self.Browser.find_element_by_xpath('/html/body/ytm-app/div[3]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4/span'%eachVid).text;
            self.Videos.append(self.EachVideo);
        for eachVid in self.Videos:
            print("[%d]: %s"%(self.Counter,eachVid));
            self.Counter += 1;
    def RefreshPage(self):
        #!In Case Of Error Refresh Can Be Done.
        self.CurrentPage = self.Browser.current_url;
        self.Browser.get(self.CurrentPage);
        print("Page Refreshed.")
    def PlayVideo(self,VideoID):
        #Finally Plays Video.
        #!VIDEO PLAY CODE HERE
        self.VideoPlay = '//*[@id="app"]/div[3]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[%d]/div/div/a/h4/span'%VideoID;
        self.Video = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.XPATH,self.VideoPlay)));
        sleep(2)
        self.Video.click()

        self.VideoTitle = WebDriverWait(self.Browser,5).until(EC.presence_of_element_located((By.CLASS_NAME,'slim-video-metadata-title')));
        #self.VideoTitle = self.Browser.find_element_by_class_name('slim-video-metadata-title'); #!To Fetch Video Title.
        self.VideoTitle = self.VideoTitle.text; 
        print('[Playing %s Youtube Now... ]'%self.VideoTitle);
        self.CompletelyLoaded = True;
        self.RefreshPage();
        self.GetUrl = self.Browser.find_element_by_css_selector('video.video-stream.html5-main-video');
        #self.GetUrl = WebDriverWait(self.Browser,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'video.video-stream.html5-main-video')));
        self.GetUrl = self.GetUrl.get_attribute("currentSrc");
        self.Browser.get(self.GetUrl)
    def MoveForward(self):
        #!Time In Seconds. [ Default 30 Sec ]
        self.Browser.execute_script("document.getElementsByTagName('video')[0].currentTime += %s"%self.IncreaseTime)
    def MoveBackwards(self):
        #!Time In Seconds. [ Default : 30 Sec] 
        self.Browser.execute_script("document.getElementsByTagName('video')[0].currentTime += %s"%self.DecreaseTime)
    def RestartVideo(self):
        #!Restart Current Video.
        self.CurrentVideoUrl = self.GetUrl;
        self.Browser.get(self.CurrentVideoUrl);
        pass
    def Pause(self):
        self.Browser.execute_script("document.getElementsByTagName('video')[0].pause()");
        pass
    def Play(self):
        self.Browser.execute_script("document.getElementsByTagName('video')[0].play()");
        pass
    def Close(self):
        self.Browser.close();
        exit(1)
    def ThreadStatus(self):
        print(threading.enumerate())


x=YoutubeMusic()
while True:
    if(x.FirstTime):
        x.HelpMenu()
    contentName = input("\n [Music Name / CMD ] ")
    if(len(contentName) == 0):
        continue
    elif(contentName == "=quit" or contentName == "=QUIT"):
        x.Close()
    elif(contentName == "=help" or contentName == "=HELP" or contentName == "=?"):
        x.HelpMenu()
    elif(contentName == "=refresh" or contentName == "=REFRESH"):
        x.RefreshPage()
    elif(contentName == "=Restart" or contentName == "=restart" or contentName == "=RESTART"):
        x.RestartVideo()
    elif(contentName == "=play" or contentName == "=PLAY"):
        x.Play()
    elif(contentName == "=pause" or contentName == "=PAUSE"):
        x.Pause()
    elif("=forward" in contentName or "=FORWARD" in contentName):
        if(":" not in contentName):
            x.MoveForward()
        else:
            Ftime = contentName.split(":")[1]
            if(len(Ftime) == 0):
                x.MoveForward()
            else:
                x.IncreaseTime = Ftime
                x.MoveForward()
    elif("=backward" in contentName or "=backward" in contentName):
            if(":" not in contentName):
                x.MoveBackwards()
            else:
                Ftime = contentName.split(":")[1]
                if(len(Ftime) == 0):
                    x.MoveBackwards()
                else:
                    x.DecreaseTime = Ftime
                    x.MoveBackwards()
    else:
        try:
            x.NavigateYoutube(contentName)
            x.ListVideos()
            contentchoice = int(input("=> "))
            if(contentchoice == 0):
                #!If no input is provided regarding music it will take 1st music out of list.
                x.PlayVideo(1)
            elif(contentchoice == 9):
                #!It will load previous page.
                x.NavigateYoutube(contentName)
            else:
                x.PlayVideo(contentchoice)
        except common.exceptions.ElementClickInterceptedException:
            print("Unknown Error: Please Try Again.")
        except ValueError:
            x.NavigateYoutube(contentName)
            x.ListVideos()