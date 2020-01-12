import pyautogui, time, pickle, random, os
from pyowm import OWM

api_key = os.environ["OWM_API_KEY"]
owm = OWM(api_key)

with open("rhizome.p", "rb") as f:
	text = pickle.load(f)
	rhizome_text = ["The two of us wrote Anti-Oedipus together. Since each of us was several, there was already quite a crowd."]
	rhizome_text.extend(text)


def slow_click():
	time.sleep(1)
	pyautogui.mouseDown()
	time.sleep(.3)
	pyautogui.mouseUp()	

def open_fb():
	pyautogui.click(x=280, y=872) # this clicks the browser icon (on the dock at bottom)
	time.sleep(2)
	pyautogui.click(x=165, y=83) # this clicks the browser bar where you type the url
	time.sleep(.5)
	pyautogui.click(x=165, y=83) # this clicks it again just in case
	time.sleep(.5)
	fbsite = [char for char in "https://www.facebook.com"]
	fbsite.append('enter')
	pyautogui.typewrite(fbsite, interval=0.1) # thype the url and press enter
	time.sleep(10)

def find_post():
	try:
		coord = pyautogui.center(pyautogui.locateOnScreen("post.png", confidence=.8, grayscale=True))
		pyautogui.moveTo(coord.x/2, coord.y/2)
		return True, coord
	except:
		return False, None

def find_background():
	try:
		coord = pyautogui.center(pyautogui.locateOnScreen("color.png", confidence=.85, grayscale=True))
		pyautogui.moveTo(coord.x/2, coord.y/2)
		return True, coord
	except:
		return False, None

def select_background():
	img_num = list(range(1,10))
	random.shuffle(img_num)
	for i in img_num:
		try:
			coord = pyautogui.center(pyautogui.locateOnScreen(f"bg{i}.png", confidence=.75, grayscale=False))
			pyautogui.moveTo(coord.x/2, coord.y/2)
			return True, coord
		except:
			pass
	return False, None

def write_post():
	pyautogui.moveTo(530, 240) # This clicks the box where you would type a status 
	slow_click()
	text, get_background = get_text()
	post = [char for char in text]
	time.sleep(1)
	pyautogui.typewrite(post, interval=0.04)
	time.sleep(30)
	if get_background:
		found, point = find_background()
		if found:
			pyautogui.moveTo(point.x/2, point.y/2)
			slow_click()
			time.sleep(1)
			found2, point2 = select_background()
			if found2:
				pyautogui.moveTo(point2.x/2, point2.y/2)
				slow_click()
				time.sleep(1)
	found, pt = find_post()
	while not found:
		pyautogui.scroll(-2)
		time.sleep(1)
		found, pt= find_post()
		time.sleep(1)
	time.sleep(1)
	pyautogui.moveTo(pt.x/2, pt.y/2)
	slow_click()
	pyautogui.moveTo(40,40)
	time.sleep(10)

def close_fb():
	pyautogui.click(x=280, y=872, button='right') # this right (i.e. second) clicks the browser icon (on dock at bottom)
	time.sleep(1)
	pyautogui.moveTo(300, 790) # this clicks "close" so you close the browser
	slow_click()
	time.sleep(1)

def get_text():
	place = random.choice(['Brooklyn, US', 'Boston, US', 'San Fancisco, US', 'Los Angeles, US', 'Brooklyn, US', 'Brooklyn, US', 'Paris, FR', 'London, GB', 'Rio de Janeiro, BR', 'Santiago, CL', 'Berlin, DE', 'Istanbul, TR', 'Athens, GR', 'Minneapolis, US'])
	city = place.split(",")[0]
	coin = random.random()
	global rhizome_text
	try:
		if coin < 0.05:
			text = "PEAK BUSHWICK (Morgan L stop) FEBRUARY SUBLET. Chill spot, chill price. DM for pics"
			text += random.choice(["!", ".", " :-)", " :)", "..."])
			return text, random.choice([False, False, True])
		elif coin > .45 and len(rhizome_text) > 0:
			text = rhizome_text.pop(0)
			with open("rhizome.p", "wb") as f:
				pickle.dump(rhizome_text, f)
			return text, random.choice([False, False, False, False, False, False, True])
		else:
			w = owm.weather_at_place(f'{place}').get_weather()
			units = random.choice(['celsius', 'kelvin', 'fahrenheit'])
			temp, status = str(w.get_temperature(units)['temp']), w.get_detailed_status()
			text = random.choice(["Hey everyone,\ni love you so much.\n", "hiya everyone\nilysm\n", "O my! everyone\n", "This just in ppl:\ni love you! Also,\n", "me again everyone\n", "Eyy I LOVE YOU SO MUCH\n","me:\neveryone:\nme: "])
			text += f"its {temp} degrees {units} with {status} in {city}"
			return text, random.choice([False, True])
	except:
		text = random.choice(["Hey", "Aloha", "Sup"])
		text += f" everyone!\n Much love to you from Brooklyn,\n have a beautiful day :-)"
		return text, True
	
if __name__ == '__main__':
	post_time = time.time()
	i = 0
	time.sleep(1)
	while True:
		i+=1
		if time.time() > post_time:
			open_fb()
			write_post()
			close_fb()
			post_time = post_time + 7200
		else:
			print(f"{i}")
			pyautogui.moveTo(50, 50, duration=2) # this is just a radom out of the way place to click so that the computer doesn't sleep.
			time.sleep(2.5)
			pyautogui.mouseDown()
			time.sleep(.3)
			pyautogui.mouseUp()
			pyautogui.moveTo(40, 40)
			time.sleep(10)
