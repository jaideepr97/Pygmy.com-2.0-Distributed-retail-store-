# COMPCI677 - LAB 3 - PYGMY.COM

# HOW TO RUN

1. Create a public-private key pair between your local machine and Edlab.  
2. On the client (local) machine, run the following command:
    ````
    ssh-keygen -t rsa
    ````
3. After this, you will be given the following prompt: 
    ```` 
    Enter file in which to save the key (/home/demo/.ssh/id_rsa):
    ````
4. Press Enter here.  
5. After this you will be given the following prompt:
    ````
    Enter passphrase (empty for no passphrase):
   ````
6. Press Enter here.  
7. Copy the public key to the remote machine. For this you will need the ssh-copy-id command. It is installed by default in most linux variants. It won’t be installed on a Mac. Use the following command to install it if you are on a Mac:
    ````
     brew install ssh-copy-id
   ````
8. Copy the public key using the following command:  
    ````
    ssh-copy-id <username>@elnux.cs.umass.edu
   ````
    where \<username\> is your edlab username. Alternatively, you can also use the following command to paste the key:  
    ````
    cat ~/.ssh/id_rsa.pub | ssh<username>@elnux.cs.umass.edu "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >>  ~/.ssh/authorized_keys"
    ````
9. Enter your password, if prompted.  
10. Now you should be able to login without using a password. Please test that you are able to do so before running the application.  

Create a public-private key pair between Edlab and Edlab:
1. Log in to Edlab as follows:
    ````
    ssh elnux1.cs.umass.edu
   ````
2. Follow the steps from 1 (previous step) with the remote directory as 
elnux2.cs.umass.edu(This is done to enable respawning of servers)
3. Clone the git repo on your edlab machine as well as your local machine.
4. Inside the src/ directory in EdLab machine, run the following command:
    ````
    source venv/bin/activate
    pip3 install -r requirements.txt --user
   ````

In the run_pygmy.sh script in the local machine, make the following changes:  
1. In the \<user\> variable, assign your edlab username.  
2. In the \<remote_path\> give the remote directory where you cloned the repo. This can be done using the pwd command. Make sure to give a ‘/’ at the end of the path.
    ````
    Example: /nfs/elsrv4/users1/grad/aayushgupta/cs677/
    ````
3. Run the script run_pygmy.sh on your local machine using the following commands:
    ````	
   chmod +x run_pygmy.sh
    ./run_pygmy.sh
    ````

