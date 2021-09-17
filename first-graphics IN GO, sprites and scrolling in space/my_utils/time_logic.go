package my_utils

import (
	"fmt"
	"os"
	"os/exec"
	"time"
)

var (
	deci_seconds = 0
	Hours_       = 0x0
	Minutes_     = 0x0
	Seconds_     = 0x0
)

const TEST_DURATION = 5 //* In seconds

func Test_efficient_timer() { //!Use capital letter to make it function PUBLIC
	//ch := make(chan int, 1000) //initial buffer called with cap()
	end := time.After(TEST_DURATION * time.Second)
	seconds_ticks := time.Tick(time.Second) //NewTicker

	c := exec.Command("cmd", "/c", "cls")
	c.Stdout = os.Stdout
	c.Run()
	now := time.Now()
	for {
		select {
		case <-seconds_ticks:
			fmt.Printf("\033[20;10H\033[32m%s\033[0m\033[H", "TEST")
			fmt.Println("Current Time:", time.Now().Format(time.RFC1123))
			t := time.Now()
			Hours_, Minutes_, Seconds_ = t.Hour(), t.Minute(), t.Second() //?%02d

		case <-end:
			fmt.Printf("\033[31;1m%s\033[0m", "OVER\n")
			fmt.Fprint(c.Stdout, "\r \r")
			return
			//panic(err)
		default:

			now = time.Now()
			deci_seconds = now.Nanosecond() / 1e8
			fmt.Printf("\033[2;50H\033[34m%d\033[0m\033[H", deci_seconds)
			time.Sleep(1 * time.Millisecond)

		}

	}
}
