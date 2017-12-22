# OH MY GPU

## What is it?

OH-MY-GPU is a gpu manager on multiserver.

It supports for Windows and Linux :-)

You can use it to look up the usage of GPUs on multiple servers.

```
➜  oh-my-gpu git:(master) ✗ python client.py 
Connecting my-server Successfully
Connecting server-gpu04 Successfully
my-server [0]:
    1 8456 MiB
    0 7429 MiB
=============================
server-gpu04 [1]:
    4 4214 MiB
    0 4124 MiB
    1 99 MiB
    3 99 MiB
    5 99 MiB
    7 99 MiB
    2 8 MiB
    6 8 MiB
=============================
Username	Used GPUs	AVG Memory	Used Memory	Memory List
v-abcde    	8          	6836          	54690        	['1:7209', '1:6682', '1:6772', '1:6682', '1:7209', '1:6682', '1:6772', '1:6682']
v-wukan    	6          	4642          	27852        	['1:4642', '1:4642', '1:4642', '1:4642', '1:4642', '1:4642']
root    	2          	3484          	6969        	['0:3997', '0:2972']
```

## How to use it?

- Clone the code

    Clone the code on the client and the server.

    ```
    git clone https://github.com/wkcn/oh-my-gpu
    ```

### Client

- Run the client

    Make sure that the server application of oh-my-gpu has been deployed on the server. If not, please see 'Deploy the servers' firstly.

    It's easy to run the client, 

    set the server name and the ip into the config.py as the examples.

    run the command: 

    ```
    python client.py
    ```
### Server

- Deploy the server

    Firstly, you should deploy the Server Application on the server.

    Make sure that python(2 or 3) and git are installed.

    The requirements is below:

    ```
    flask
    ```

    You can use `pip` to install it.

    Set the paths of the executable file of python and git into the environment variables.

    For windows, 

    - 1. Open File Explorer, Right Click `This PC` on the left side,and Select Properties.

    - 2. Click `Advanced system settings`

    - 3. Select the Advanced tab and click the `Environment Variables`

    - 4. Add the path into the environment variables `Path`

        Enter the commands `git`, it's available if there is no any error.

        Remember to open the port (**690 port [default]**) on the Windows firewall and the router (if it exists).

    Run the command:

    ```
    python server.py
    ```

Any issue is welcome :-)
