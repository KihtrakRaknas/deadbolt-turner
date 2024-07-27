import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from servo import Servo
import config
import urequests


def connect():
    ssid = config.ssid
    password = config.password
    
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    urequests.get(f'https://n.kihtrak.com/?project={config.notibot_project}&title=connected on {ip}').close()


    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection

def parse_query_params(query_string):
    params = {}
    if query_string:
        key_values = query_string.split('&')
        for key_value in key_values:
            key, value = key_value.split('=')
            params[key] = value
    return params

def parse_http_request(data):
    request_lines = data.split(b'\r\n')
    try:
        method, full_path, http_version = request_lines[0].decode().split(' ')
    except:
        return {
            'method': None,
            'path': None,
            'query_params': {},
            'http_version': None,
            'headers': None
        }
    path, query_string = full_path.split('?', 1) if '?' in full_path else (full_path, '')
    query_params = parse_query_params(query_string)

    headers = {}
    for line in request_lines[1:]:
        if line:
            key, value = line.decode().split(': ', 1)
            headers[key] = value

    return {
        'method': method,
        'path': path,
        'query_params': query_params,
        'http_version': http_version,
        'headers': headers
    }


def serve_file_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error: {e}".encode()
    
    
def send_content(client, content):
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content
    try:
        client.send(response)
    except OSError:
        pass
    finally:
        client.close()
        

s1 = Servo(28)
def serve(connection):
    #Start a web server
    s1.free()
    while True:
        client = connection.accept()[0]
        
        try:
            request = client.recv(1024)
        except OSError:
            continue
        parsed_request = parse_http_request(request)
        print(parsed_request)

        if parsed_request["path"] == '/turn':
            if parsed_request["query_params"]["angle"]:
                try:
                    angle = int(parsed_request["query_params"]["angle"])
                    s1.goto(angle/195*1024)
                    sleep(3)
                    s1.free()
                except:
                    pass
        if parsed_request["path"] == '/open':
            s1.goto((20+90)/195*1024)
            sleep(3)
            s1.free()
            urequests.get(f'https://n.kihtrak.com/?project={config.notibot_project}&title=Door opened').close()
            file_content = "done"
        elif parsed_request["path"] =='/close':
            s1.goto(20/195*1024)
            sleep(3)
            s1.free()
            file_content = "done"
        else:
            file_content = serve_file_content("./index.html")
        send_content(client, file_content)
        sleep(1)
        

try:
    ip = connect()
    connection = open_socket(ip)
    sleep(3)
    serve(connection)
except KeyboardInterrupt:
    print("Halted by user")


