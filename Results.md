# Results.md

Movements To do:
 - Simple Finger tap and vertical line
 - Block follower and move leader
 - Box Lift
 - Fast ossiclations 

## Local - no feedback - (Baseline)
Notes: since there is no feedback there is no way to feel if the mirror bot is doing anything or stuck

## Local - with feedback
Notes: feedback is felt, after the controller is taken away, leader moves to follower position 

## Remote - no feedback 

### Delays: 0ms 10ms 25ms
### Packet loss: 0% 1% 10%
Notes:
D - P
0 - 0: Same as baseline
10+2.25 - 0: Virtually same as baseline, but diff in graph
25+5.25 - 0: Virtually same as baseline, but diff in graph.... a bit difficult to lift the box
100+10.25 - 0: Noticeable delay, everything is harder 


0 - 1.25: Almost the same, but sometimes in very fast motion, delay can be seen due to dropped packets
0 - 10.25: Considerable delay in action caused by packet loss, and the movement is very fast on follwer due to this

10+2.25 - 1.25: Delay is slightly noticeable, still fairly easy to do tasks 
25+5.25 - 1.25: Delay is slightly worse, tasks are do-able but would not be recommended in high precission tasks
25+5.25 - 5.25: Delay is slightly worse, tasks are do-able but would not be recommended in high precission tasks


## Remote - with feedback

### Delays: 0ms 5ms 10ms 15ms 25ms
### Packet loss: 0% 1% 5% 10% 25%
Notes:
D - P
0 - 0: Box can be felt, leader reaches follower pos
10+2.25 - 0: Force is felt even when no obstacle is there, due to delay
25+5.25 - 0: Force is felt even when no obstacle is there, everything goes haywire when fast motions are there

0 - 1.25: Similar to baseline
0 - 10.25: High Force Felt due to packet loss, motion of follower is very lagy and sudden

10+2.25 - 1.25: Operable, virtually close to baseline
25+5.25 - 1.25: Goes crazyyy for fast motions
25+5.25 - 5.25: Goes crazyyy for fast motions, hard to lift box as the follower keeps losing contact (vibrations)
