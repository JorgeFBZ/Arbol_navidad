def web_page():
    if led_verde.value() == 1:
        gpio_verde_state="ON"
    else:
        gpio_verde_state="OFF"
        
    if led_azul.value() == 1:
        gpio_azul_state="ON"
    else:
        gpio_azul_state="OFF"
        
    if led_rojo.value() == 1:
        gpio_rojo_state="ON"
    else:
        gpio_rojo_state="OFF"
        
    html = """<html>

<head>
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Helvetica;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
            background-color: darkgreen;
        }

        h1 {
            color: #8a1515;
            padding: 2vh;
            font-size: 2.5rem;
            background-color: darkgreen;
        }

        p {
            font-size: 1.5rem;
            background-color: darkgreen;
        }
        hr{
            width: "100%";
            height: 25px;
            margin: 0;
            border: 0;
            background-color:darkgreen;        
        }

        .button {
            display: inline-block;
            background-color: #e7bd3b;
            border: none;
            border-radius: 4px;
            color: white;
            padding: 16px 40px;
            text-decoration: none;
            font-size: 30px;
            margin: 2px;
            cursor: pointer;
        }

        .button2 {
            background-color: #4286f4;
        }
    </style>
</head>

<body>
    <h1>ESP Web Server</h1>
    <hr style="background-color:#8a1515; height: 10px;">
    <p>Verde: <strong>""" + gpio_verde_state + """</strong></p>
    <p><a href="/?led_v=on"><button class="button">ON</button></a></p>
    <p><a href="/?led_v=off"><button class="button button2">OFF</button></a></p>
    
    <hr>
    <p>Azul: <strong>""" + gpio_azul_state + """</strong></p>
    <p><a href="/?led_a=on"><button class="button">ON</button></a></p>
    <p><a href="/?led_a=off"><button class="button button2">OFF</button></a></p>
    
    <hr>
    <p>Rojo: <strong>""" + gpio_rojo_state + """</strong></p>
    <p><a href="/?led_r=on"><button class="button">ON</button></a></p>
    <p><a href="/?led_r=off"><button class="button button2">OFF</button></a></p>
    <hr>
    <p><strong>Efecto: </strong> </p>
    <p><a href="/?led_ef=on"><button class="button">ON</button></a></p>
    <p><a href="/?led_ef=off"><button class="button button2">OFF</button></a></p>
</body>

</html>"""
    return html

def led_pwm(led,delay):
    global ciclo
    led.start(0)
    n=0
    while n < ciclo:
        sleep(delay)
        for duty in range(0,1024):
            led.duty(duty)
            sleep(0.005)
        for duty in range(1023,0,-1):
            led.duty(duty)
            sleep(0.005)
        n+1
        print (f"Ciclo: {n}")
    print ("Efecto acabado")
                    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_v_on = request.find('/?led_v=on')
    led_v_off = request.find('/?led_v=off')
    
    led_a_on = request.find('/?led_a=on')
    led_a_off = request.find('/?led_a=off')
    
    led_r_on = request.find('/?led_r=on')
    led_r_off = request.find('/?led_r=off')
    
    led_ef_on = request.find('/?led_ef=on')
    led_ef_off = request.find('/?led_ef=off')
    
    if led_v_on == 6:
        print('LED Verde ON')
        led_verde.value(1)
    if led_v_off == 6:
        print('LED Verde OFF')
        led_verde.value(0)
        
    if led_a_on == 6:
        print('LED Azul ON')
        led_azul.value(1)
    if led_a_off == 6:
        print('LED Azul OFF')
        led_azul.value(0)

    if led_r_on == 6:
        print('LED Rojo ON')
        led_rojo.value(1)
    if led_r_off == 6:
        print('LED Rojo OFF')
        led_rojo.value(0)
    
    if led_ef_on == 6:
        print('Efecto ON')
        led.pwm(pwm_rojo, randint(0,5))
        led.pwm(pwm_verde, randint(0,5))
        led.pwm(pwm_azul, randint(0,5))
    if led_ef_off == 6:
        print('Efecto OFF')
        led_verde.value(0)
        led_rojo.value(0)
        led_azul.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
