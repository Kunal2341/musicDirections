# Musicly

**Musicly** is a addon on top of your spotify. While driving is tracks your position and estimated the perfect time to annouce a direction change while giving the perfect listening experience. 

![logo](https://github.com/Kunal2341/musicDirections/blob/main/LOGO/logo.png?raw=true)


# What does it do
Whenever going following transportation directions connected with music, everyone has experienced when the directions are spoken right when the major beat drops of a song resulting in missing the vibrant feeling of the music. 

Musicly smartly decides when to inform the user of the next step in directions based on the flow of the song and its current location in relation to the total directions. This informs the user of the correct directions while also giving an excellent listening experience of the song. 

Intelligentlly informs the user of directions in a timely manner with maintaining excellent listening experience


# Architehcutre
- User inputs `destination`, `transportation_type`, `spotify_user`, and `spotify_pass`. 
- Gets spotify access token
- Gets directions from google API
- User clicks start whenever start driving
	- Calculates approximate time before next inform of directions
		- EX: `264` seconds. `0.9*264 = 237.6` seconds. Add that many seconds to the current time from when user clicked start. 
	- Estimate time to speak directions
	- Gets current location in music 
	- Downloads music calculate periods of time not to intrupt
		- `[[start1, end1],[start2, end2]]`
	- `start1` - current location  = `200` seconds
	- `end1` - current location  = `250` seconds
	- Since `200<237.6<250` 
	- Speak at `200` - `timeSpeakDirections` seconds. 
		- Adjust tempo of speak based on song choice
	- Loop all for next step every 10 seconds
	




# Process of building this program

 - [x] Call directions API 
 - [x] Getting access token of the user
	 - [x] Selenium through website return with access token
 - [x] Call Spotify API and call data (*Return the following*)
	 - [x] Current time
	 - [x] Total Song time
	 - [x] Song Name
	 - [x] Artist's name
	 - [x] Link to song image
	 - [x] ID
 - [x] Download music from a (**SOURCE**)
 - [ ] Find periods of time to not call directions and save in a list
	 - [ ] https://github.com/nlml/bpm
 - [ ] Get current location of user using Java Script
 - [ ] Calculate the distance between current location and next step in route
 - [ ] Calculate time left before turn - proportion of distances and time
 - [ ] Wait till time reached, 0.1 mins before turn and then closest position
 - [x] Vision get location
	 - [ ] Regex
 - [ ] Calculate direction moving
	 - [ ] Call street view API and locate correct image and display on website
 - [ ] FLASK
 - [ ] Speak
	 - [ ] `var  msg  =  new  SpeechSynthesisUtterance('Hello World');`
	 - [ ] `window.speechSynthesis.speak(msg);`
	 - [ ] AMAZON POLLY 
 - [ ] Adjust volume of speak based on song choice
 - [ ] Build Flask
 - [ ] 
# Sources 
https://devpost.com/kunal-aneja101?ref_content=user-portfolio&ref_feature=portfolio&ref_medium=global-nav

https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html

https://towardsdatascience.com/finding-choruses-in-songs-with-python-a925165f94a8

# Contact

**Date Created**: `April 2021`

**Author**: `Kunal Aneja`

**Email**: `kunal.aneja101@gmail.com`