# Braddel mat mengem Avatar
Use the microphone to chat with my Avatar in luxembourgish on OpenAI ; luxembourgish text and speech answer with my voice.    
The primary purpose of this customized version is to integrate the schreifmaschinn.lu API for Luxembourgish speech recognition and optimize ChatGPT to deliver responses in accurate Luxembourgish. The main challenge lies in training a new voice with enhanced Luxembourgish TTS, ensuring compatibility with the HeyGen interactive Avatar.

To run the code in a terminal in your local environment, with NextJS / React installed :
```
git clone https://github.com/mbarnig/Braddel_mat_mengem_Avatar.git
cd Braddel_mat_mengem_Avatar
npm install
npm run dev
```
Display the application in your browser at localhost:7860     
If the port is already running, stop it with `npx kill-port 7860`.      
If an error is thrown at session start, check if files or folders which should be ignored in the git (for example folder schreifmaschinn) are not present in the local project folder.    
