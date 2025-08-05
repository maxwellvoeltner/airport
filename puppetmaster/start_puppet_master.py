from time import sleep

from pitop import Pitop

if __name__ == "__main__":
    pitop = Pitop( )
    miniscreen = pitop.miniscreen
    while True:
        if miniscreen.select_button_is_pressed:
            print( 'test' )
        sleep( 0.2 )

