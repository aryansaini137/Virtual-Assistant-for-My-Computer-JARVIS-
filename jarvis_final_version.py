from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pytz
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import os
import wx
import wikipedia
import wolframalpha
import subprocess
import requests, json
import random,os
import cx_Oracle
import smtplib
import pyautogui as pg
import pyperclip
from bot import fetch_reply
from twilio.rest import Client
from twilio.rest.api import Api
engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume',1)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("good morning")
		speak("right now it's "+str(hour)+"am sir")
	elif hour>=12 and hour<18:
		speak("good afternoon")
		speak("right now it's "+str(hour)+"pm")
	else:
		speak("good evening")
		speak("right now it's "+str(hour)+"pm")
	return hour

def takeCommand():
	r= sr.Recognizer()
	with sr.Microphone() as source:
		print("listening...")
		audio=r.listen(source,phrase_time_limit=7)

	try:
           print("recognizing...")
           query = r.recognize_google(audio,language= 'en-in')
           print("YOU SAID:", query)

	except Exception as e:

		  print("Say that again plz.....")
		  return "none"

	return query

def search_web(input):



	if 'in youtube' in input.lower() or 'on youtube' in input.lower():
		speak("Opening in youtube")
		if 'search for' in query:
		    query1=query.split('search for')
		elif 'play' in query:
		    query1=query.split('play')
		query1=query1[1].split('in youtube')
		webbrowser.open("https://www.youtube.com/results?search_query=" + ''.join(query1))
		return

	elif ' in google' in input.lower() or 'on google' in input.lower():
		speak("This that i found ")
		query1=query.split('search for')
		query1=query1[1].split('on google')
		webbrowser.open("https://www.google.com/search?sxsrf=ALeKk02KVAdoxXF9ChPkPjAX-E2rMxwFNw%3A1588310459739&source=hp&ei=u7GrXq35KvKO4-EPv8-2oAQ&q="+''.join(query1)+"&oq="+ ''.join(query1)+"&gs_lcp=CgZwc3ktYWIQAzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoHCCMQ6gIQJzoECCMQJzoHCAAQgwEQQzoFCAAQgwFQzVFYwWZgpXFoA3AAeACAAeYLiAH-MJIBCzQtMS4xLjEuMi4xmAEAoAEBqgEHZ3dzLXdperABCg&sclient=psy-ab&ved=0ahUKEwjtwvnF9ZHpAhVyxzgGHb-nDUQQ4dUDCAc&uact=5")
		return


def search_folder(query):
	speak("okay sir    Enter a path as hint ")
	hint = input("Enter the path ")
	speak("Enter name file or folder name ")
	name = input("Enter the name ")

	if 'folder' in query:
		for dirpath,dirname,filename in os.walk(hint):
			if name in dirname:
				speak("yes i found sir")
				break
		speak("opening the folder")
		os.startfile(dirpath)

	elif 'file' in query:
		for dirpath,dirname,filename in os.walk(hint):
			if name in filename:
				speak("yes i found sir")
				break
		speak("opening the file")
		os.startfile(dirpath)

	else:
		speak("does not exist")




class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None,
			pos=wx.DefaultPosition, size=wx.Size(450, 100),
			style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
			 wx.CLOSE_BOX | wx.CLIP_CHILDREN,
			title="JARVIS")
		panel = wx.Panel(self)
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(panel,
		label="Calculation Panel")
		my_sizer.Add(lbl, 0, wx.ALL, 5)
		self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
		self.txt.SetFocus()
		self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		my_sizer.Add(self.txt, 0, wx.ALL, 5)
		panel.SetSizer(my_sizer)
		self.Show()

	def OnEnter(self, event):
		input = self.txt.GetValue()
		input = input.lower()
		if input == '':
			r = sr.Recognizer()
			with sr.Microphone() as source:
				audio = r.listen(source)

			try:
				self.txt.SetValue(r.recognize_google(audio))
			except sr.UnknownValueError:
				print ("cannot understand you")
			except sr.RequestError as e:
				print ("could not request result".format(e))


		else:

			try:
			#wolframalpha
					app_id = "API_KEY"
					client = wolframalpha.Client(app_id)
					res = client.query(input)
					answer = next(res.results).text
					print (answer)
					engine.say(answer)
					engine.runAndWait()

			except:
				pass

MONTHS=["january","february","march","april","may","june","july","august","september","october","november","december"]
DAYS=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAY_EXTENTIONS=["rd","th","st","nd"]
SCOPES = ['GOOGLE_API_LINK_calendar']

def authenticate_google():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day,service):
    # Call the Calendar API
    date = datetime.datetime.combine(day,datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day,datetime.datetime.max.time())
    local_tz=pytz.timezone('Asia/Kolkata')
    date = local_tz.localize(date)
    end_date=local_tz.localize(end_date)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('there is no plan schedule for this day sir')
    else:
        speak("you are having {} event sir ".format(len(events)))
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time=str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time + "pm"

            speak(event["summary"] + "at" +start_time)



def get_date(text):
    text=text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day=-1
    day_of_week=-1
    month=-1
    year = today.year

    if 'tomorrow' in text:
        day = today.day+1
        month = today.month
    if 'day after tomorrow' in text:
        day=today.day+2
        month = today.month
    for word in text.split():
        if word in MONTHS:
            month=MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day=int(word[:found])
                    except:
                        pass


    if month < today.month and month != -1:
        year= year+1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1 or "next" in text:
        curent_day_of_week = today.weekday()
        dif = day_of_week - curent_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >=1:
                dif += 7

        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return "none"

    return datetime.date(month=month, day=day, year=year)


def note(text):
	date=datetime.datetime.now()
	file_name = str(date).replace(":","-") + "-note.txt"
	with open(file_name,"w") as f:
		f.write(text)

	subprocess.Popen(["notepad.exe", file_name])


def weather(text):
	api_key = "weather_API_KEY"

	base_url = "API_openweathermap.org_BASE_url"

	complete_url = base_url + "appid=" + api_key + "&q=" + text

	response = requests.get(complete_url)

	x = response.json()

	if x["cod"] != "404":

		y = x["main"]

		current_temperature = y["temp"] - 273.15
		current_pressure = y["pressure"]
		current_humidiy = y["humidity"]

		z = x["weather"]

		weather_description = z[0]["description"]

		print(" Temperature (in celsius unit) = " +
						str(current_temperature) +
			"\n atmospheric pressure (in hPa unit) = " +
						str(current_pressure) +
			"\n humidity (in percentage) = " +
						str(current_humidiy) +
			"\n description = " +
						str(weather_description))
		speak("weather report")
		speak("Temperature is "+str(current_temperature)+ " celsius")
		speak("atmospheric pressure is "+str(current_pressure)+" hPa")
		speak("humidity is "+str(current_humidiy)+"percentage")
		speak("According to me sir "+str(weather_description))
	else:
		print(" City Not Found ")
		speak("sir i can't found this city name in my list")


def open1(query):
	if 'open youtube' in query:
		speak('opening youtube')
		webbrowser.open("https://www.youtube.com/om")
	elif 'open google'in query:
		speak("opening google now")
		webbrowser.open("https://www.google.com/")
	elif 'open instagram' in query:
		speak("opening instagram")
		webbrowser.open("instagram.com")

	elif 'open facebook' in query:
		speak("opening facebook")
		webbrowser.open("facebook.com")
	elif 'open amazon' in query:
		speak("opening amazon shopping")
		webbrowser.open("https://www.amazon.in/?ref_=nav_custrec_signin&")
	elif 'open flipkart' in query:
		speak("opening flipkart")
		webbrowser.open("https://www.flipkart.com/")
	return

def NewsFromBBC():
	main_url = "NEWS_API_KEY"
	open_bbc_page = requests.get(main_url).json()
	article = open_bbc_page["articles"]
	results = []

	for ar in article:
		results.append(ar["title"])

	for i in range(len(results)):
		try:
			print(i + 1, results[i])
		except:
			pass



	speak("sir today top news headline is")
	speak(results[0])

def search_(find):
	flag=0
	try:
		con = cx_Oracle.connect('system/1234@localhost')
		cursor = con.cursor()
		cursor.execute("select * from email")
		records = cursor.fetchall()
		for record in records:
			a,b = record
			if a in find:
				flag=1
				try:
					Send_Email(a,b)

				except Exception as e:
					speak("error {} sending email failed".format(e))
					print(e)
				break
		if flag==0:
			speak("sir i doesn't have email id can you provide me please")
			name=input("  Name:- ")
			email_id=input("  Email_ID:- ")
			speak("thankyou sir")
			query = "insert into email values(" + "'" + name + "'" + ',' + "'" + email_id +"'" + ')'
			cursor.execute(query)
			con.commit()
			search_(find)



	except cx_Oracle.DatabaseError as e:
		print("There is a problem with Oracle", e)
		speak("There is a problem with Oracle")

	finally:
		if cursor:
			cursor.close()
		if con:
			con.close()

	return

def Send_Email(a,b):
	speak("what should i say sir")
	content=takeCommand().lower()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.login('EMAIL_ID','EMAIL_PASSWORD')
	server.sendmail('EMAIL_ID',b,content)
	speak("Email has been send")
	server.close()

def copy_():
    pg.hotkey("ctrl",'c')
    tob=pyperclip.paste()
    return tob
def sc_():
    date=datetime.datetime.now()
    file_name1 = "E:\\jarvis_file\\"+str(date).replace(":","-")+"sc.png"
    myScreenshot = pg.screenshot()
    myScreenshot.save(file_name1)
    return file_name1
def whatsapp_():
    x=copy_()
    print(x)
    sid='SID_KEY'
    token='TOKEN_KEY'
    client = Client(sid, token)
    form_whatsapp_number='TWILIO_NUMBER'
    to_whatsapp_number='YOUR_WHATSAPP_NUMBER'
    body=x
    client.messages.create(to=to_whatsapp_number,from_=form_whatsapp_number,body=body)
    return



def command(query,number):
    if query =="none":
        return

    elif 'bye' in query or 'goodbye' in query :
        speak('ok sir')
        speak('closing all system')
        speak('disconnecting to server')
        speak('going  offline')
        speak("goodBye , you know where to find me" )
        exit();

    elif 'folder in system' in query or 'find a file'in query:
        search_folder(query)


    elif 'open' in query:
        open1(query)
    elif 'news' in query:
        if 'top' in query:
            NewsFromBBC()
        else:
            speak("where are some detail")
            webbrowser.open("https://timesofindia.indiatimes.com/")
    elif 'music' in query:
        speak("okay opening my personal favorite spotify ")
        os.chdir(r"C:\Users\USER_NAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
        os.system("start Spotify")
        os.chdir(r"E:\AL-code")
    elif 'search' in query or 'play' in query :
        search_web(query)
    elif 'open an app' in query:
        speak("ok which app you like to open")
        f='start '+takeCommand().lower()
        if os.system(f) == 0:
            speak("opening")
        else:
            speak("I cannot access")


    elif 'plan' in query or "do i have " in query:
        service=authenticate_google()
        if get_date(query) =="none":
            speak("sir i didn't get the date right can you speak it again")
            return
        else:
            get_events(get_date(query),service)

    elif 'a note' in query or "remember" in query:
        speak("i am ready boss")
        text =takeCommand().lower()
        note(text)

    elif 'weather' in query:
        if 'find' in query or 'city' in query:
            speak("which city weather do you like to find")
            text=takeCommand().lower()
            weather(text)
        else:
            weather("dehradun")

    elif 'email' in query or 'send an email' in query:
        speak("ok boss")
        search_(query)


    elif 'calculation panel' in query or 'calculator'in query:
        speak("opening calculation panel")
        app = wx.App(True)
        frame = MyFrame()
        app.MainLoop()

    elif 'read' in query:
        speak('ok sir')
        tob=copy_()
        speak(tob)
    elif 'screenshot' in query:
        speak('ok sir')
        f=sc_()
        speak('screenshot has been taken sir do you want to see it')
        if 'yes' in takeCommand().lower():
            os.startfile(f)
        else:
            speak("ok sir")
    elif 'whatsapp' in query or 'text' in query:
        whatsapp_()
        speak("It has been send sir you can check your whatsapp")



    else:
        reply = fetch_reply(query,number)
        if not reply in ["I didn't get that sir. Can you say it again?","I missed that."]:
            print(reply)
            speak(reply)
        else:

            try:

                try:
                #wolframalpha
                        app_id = "wolframalpha_API_KEY"
                        client = wolframalpha.Client(app_id)
                        res = client.query(query)
                        answer = next(res.results).text
                        print (answer)
                        speak(answer)

                except:
                #wikipedia
                        #input = input.split(' ')
                        #input = " ".join(input[2: ])
                        print (wikipedia.summary(query,sentences=2))
                        speak(wikipedia.summary(query, sentences=2))
            except:
                pass

    return


if __name__ =="__main__":
    if 'jarvis' in takeCommand().lower():
        d = random.choice(['o hello sir','yes boss','at you command sir','i hope your day is going nice sir'])
        speak(d)
        hour=wishMe()
        while True:
            query =takeCommand().lower()
            if 'whatsapp mode' in query:
                speak("starting whatsapp mode")
                os.system('python bot1.py')
            else:
                command(query,0000)
