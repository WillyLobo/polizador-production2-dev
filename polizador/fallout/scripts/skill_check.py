import sys,tty,os,termios

def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: 'space',
                9: 'tab',
                27: 'esc',
                65: 'up',
                66: 'down',
                67: 'right',
                68: 'left'
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

habilidad_total = float(1)
habilidad_skill = float(1)

def skill_up(habilidad_total, habilidad_skill):
    if habilidad_total <= 0:
        return 0, 0
    
    incrementos = [
        (200, 1/6),
        (175, 1/5),
        (150, 1/4),
        (125, 1/3),
        (100, 1/2),
        (0, 1)
    ]
    
    for limite, incremento in incrementos:
        if habilidad_total > limite:
            habilidad_skill += incremento
            break
    
    habilidad_total += incremento
    return habilidad_total, habilidad_skill

try:
    while True:
        k = getkey()
        if k == 'esc':
            quit()
        elif k == 'space':
            habilidad_total, habilidad_skill = skill_up(habilidad_total, habilidad_skill)
            print(habilidad_total, habilidad_skill)
except (KeyboardInterrupt, SystemExit):
    os.system('stty sane')
    print('stopping.')