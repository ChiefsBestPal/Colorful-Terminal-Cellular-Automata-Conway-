package main

//! eventually, import "testing" and read docs about projects

import (
	"fmt"
	_ "image/png"
	"log"
	"strconv"
	"sync"
	"time"

	Utils "first-graphics/my_utils"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

//TODO CHEAT SHEET:https://ebiten.org/documents/cheatsheet.html
//TODO DO FIRST TUTORIALS https://github.com/hajimehoshi/ebiten/wiki/Tutorial%3AScreen%2C-colors-and-squares
// var square *ebiten.Image

// func update(screen *ebiten.Image) error {

// 	// Fill the screen with #0F0000 color
// 	screen.Fill(color.NRGBA{0x0f, 0x00, 0x00, 0xff})

// 	// Display the text though the debug function
// 	ebitenutil.DebugPrint(screen, "Our first game in Ebiten!")
// 	if square == nil {
// 		// Create an 16x16 image
// 		square, _ = ebiten.NewImage(16, 16, ebiten.FilterNearest)
// 	}

// 	// Fill the square with the white color
// 	square.Fill(color.White)

// 	// Create an empty option struct
// 	opts := &ebiten.DrawImageOptions{}

// 	// Draw the square image to the screen with an empty option
// 	screen.DrawImage(square, opts)

// 	return nil
// }
//*affine transformation matrix (general):
// matrix; [[ a b tx] [c d ty] [0 0 1]], vect; [x y 1]
// = [[ax +by + tx] [cx + dy + ty] [1]]
//*common; translating matrix:
// matrix; [[1 0 tx] [0 1 ty ] [0 0 1]], vect; [x y 1]
// = [[x+tx] [y+ty] [1]]
//*scale; [[1 0 tx][0 1 ty][0 0 1]] * vect
//*rot; [[cos -sin 0][sin cos 0] [0 0 1]] * vect
//*2 affine transform matrix give another one; so do combinations of trans, scale, rot

const ( //*This is ENUM
	NUMBER_OF_SPRITES = 11
	sprites_on_screen = 10 //hh:mm:ss:c

	spriteWidth  = 43
	spriteHeight = 66

	screenWidth  = 640
	screenHeight = 480

	margin = (screenWidth - (sprites_on_screen * spriteWidth)) / 2.0 //?
)

var (
	img                 *ebiten.Image
	DigitsSpritesImages [NUMBER_OF_SPRITES]*ebiten.Image
	DigitsSpritesPaths  = [NUMBER_OF_SPRITES]string{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "sep"}
)

var err error
var opts *ebiten.DrawImageOptions

type Clock interface{}

type Game struct {
	count int
}

var formatted_time string

func my_timer() {
	Utils.Test_efficient_timer()
}

type MyDynamicTime struct {
	seconds int
	minutes int
	hours   int
	mux     sync.Mutex
}

func init() {

	//"Converting Paths to Images\n--->\t Last path/image should be a seperator")
	for spriteImageix, spriteName := range DigitsSpritesPaths {

		path := fmt.Sprintf("DigitalCharsSprites/%s.png", spriteName)
		img, _, err = ebitenutil.NewImageFromFile(path)
		if err != nil {
			log.Fatal(err)
		}
		DigitsSpritesImages[spriteImageix] = img
	}

	//TODO to avoid drawing the same seps everytime !!! VVVVVV
	// sepImage := DigitsSpritesImages[NUMBER_OF_SPRITES-1]
	// numOfsep := (NUMBER_OF_SPRITES % 2) + 2 //because we have format aa:bb:cc:dd
	// for sep_ix := 0; sep_ix < numOfsep; sep_ix++ {
	// 	opts = &ebiten.DrawImageOptions{}
	// 	opts.GeoM.Translate(float64(margin+(sep_ix*3+2)), float64(screenHeight)/2) //always the mod 3 corners of sprites on screen
	// 	tmp_screen.DrawImage(sepImage, opts)
	// }

}

func (g *Game) Update() error {

	var my_time MyDynamicTime

	t := time.Now()
	my_time.hours, my_time.minutes, my_time.seconds = t.Hour(), t.Minute(), t.Second()
	deci_seconds := t.Nanosecond() / 1e7

	formatted_time = fmt.Sprintf("%02d:%02d:%02d:%01d", my_time.hours, my_time.minutes, my_time.seconds, deci_seconds)
	//* FOR Draw()

	return nil

}

func (g *Game) Draw(screen *ebiten.Image) {
	opts = &ebiten.DrawImageOptions{} //reset opts
	opts.GeoM.Translate(margin, float64(screenHeight)/2.0)
	for screen_pos_ix, digit_runes := range formatted_time {

		if screen_pos_ix%3 != 2 { //TODO if sprite is not a sep (which will be pre-rendered in init())
			DigitsSpritesImages_ix, _ := strconv.Atoi(string(digit_runes))      //sprite_ix here happens to be their actual repr, as we are working with digits
			screen.DrawImage(DigitsSpritesImages[DigitsSpritesImages_ix], opts) //previous_x + spriteWidth//!

		} else {
			screen.DrawImage(DigitsSpritesImages[NUMBER_OF_SPRITES-1], opts)
		}
		opts.GeoM.Translate(float64(spriteWidth), 0.0)
	}

}

func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return 640, 480
}

func main() {
	ebiten.SetWindowSize(screenWidth*2, screenHeight*2)
	ebiten.SetWindowTitle("Render an image")
	if err := ebiten.RunGame(&Game{}); err != nil {
		log.Fatal(err)
	}

	//TODO a io.Reader for bytes in a matrix
	//TODO a single png containing all sprites and use SubImage(Rect)

	//*RUNNING THE CODE BELLOW WITH AUTOMATIC DEPENDENCIES WILL DO TESTS FOR FANCY DYNAMIC TIME PRINTING
	// go my_timer()
	// var my_time MyDynamicTime
	// counter, prev := 0, 0 // to check prev

	// my_time.mux.Lock()
	// for {
	// 	prev = my_time.seconds
	// 	my_time.seconds = Utils.Seconds_
	// 	my_time.minutes = Utils.Minutes_
	// 	my_time.hours = Utils.Hours_
	// 	time.Sleep(50 * time.Millisecond) //delay to allow other goroutine to run
	// 	if prev != my_time.seconds {
	// 		counter++
	// 		fmt.Println("WADSADADADSADSA")
	// 	}
	// 	if counter > 10 {
	// 		my_time.mux.Unlock() //not defer...
	// 		break
	// 	}
	// }
	// return

}
