


# Autometero
Integrate AI to automatically send messages and schedule dates by learning and mimicking the user's messaging style, ensuring that automated messages are personalized and contextually appropriate.

# Personalized Messaging Through Style Mimicry
* The AI learns and adapts to the user’s unique messaging style, capturing tone, phrasing, and preferences. By mimicking these characteristics, the system ensures that outgoing messages feel personal and authentic, maintaining a natural flow of conversation.

<img width="2056" alt="Screenshot 2024-09-18 at 12 06 06 PM" src="https://github.com/user-attachments/assets/77bcceab-abec-4c69-9440-fbde10bd0695">

# Contextually Relevant Responses
* AI analyzes past interactions and context, tailoring responses to fit the specific situation. This allows the system to send replies or initiate conversations that feel timely, appropriate, and aligned with ongoing communication threads.

<img width="2056" alt="Screenshot 2024-09-18 at 12 06 39 PM" src="https://github.com/user-attachments/assets/1eef0003-d079-4bcc-882a-868c28000a16">

# Automated Date Scheduling
* Beyond messaging, the AI can set up dates based on user availability and preferences. This feature further enhances the convenience by managing time and event coordination efficiently, without the need for direct input from the user.

# Enhanced User Experience
* With automated, AI-generated messages that closely resemble the user’s typical communication style, the system delivers a seamless and personalized experience, ensuring that interactions remain engaging and relevant even when automated.





# To SSH into the azure vm
ssh azureuser@104.42.212.81

# To ssh tunnel the vm to locally
ssh -L 5555:127.0.0.1:5555 azureuser@104.42.212.81

# If connection to emulator not working, do these
docker container restart androidemu
adb connect 127.0.0.1:5555 # on the arm vm
appium # on the armvm

# To ssh tunnel just the appium server (This shouldn't be needed as the port 4723 is already exposed from azure)
ssh -L 4723:127.0.0.1:4723 azureuser@104.42.212.81

# To access the emulator
scrcpy

# In case device doesn't show up in adb
adb connect 127.0.0.1:5555

# Run these commands if device isn't running
sudo modprobe binder_linux devices="binder,hwbinder,vndbinder"
sudo modprobe ashmem_linux

# Running the docker container
docker run -itd --privileged \
 --name androidemu \
 -v ~/data:/data \
 -p 5555:5555 \
 redroid/redroid:11.0.0-latest

docker run -itd --privileged \
 --name androidemu2 \
 -v ~/data:/data \
 -p 5555:5555 \
 redroid/redroid:14.0.0-latest

# Removing the docker container
docker container rm -f androidemu

# Check what's running on docker
docker ps -a

#Start the container
docker container start androidemu
docker container stop androidemu
docker container restart androidemu

#Running process in the background
https://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session
tmux

#Tmux stuff
# Creating new session with name bob
tmux new -s bob
tmux ls
tmux a
ctrl b + d
tmux a -t 0
tmux kill-session -t bob

ctr b + % // for new window


# How to use screen
screen -XS <session-id> quit
screen -ls
screen -r 

# Nginx stuff
# After code change run this command
sudo systemctl restart backend

sudo systemctl restart nginx

sudo systemctl daemon-reload


sudo systemctl stop backend
sudo systemctl disable backend

