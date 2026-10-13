Auction Strategy Simulator

CPSC 370 Assignment 5

Josh Vaysman and Dylan Massaro

Part 2

| Mechanism | Avg. Revenue | Avg. Winner Utility | Efficiency |
|---|---|---|---|
| First price | 69.7956 | 17.4489 | 1.0000 |
| Second price | 74.3845 | 12.8600 | 0.9580 |

1. Second price. It averaged about 74.4 and first price averaged about 69.8.

2. First price. The winner kept about 17.4 on average and in second price it was about 12.9.

3. Everybody used the same bidding rule, so whoever had the highest value also had the highest bid and won. First price was 100%. Second price shows about 96% but that's just from ties. When two bidders had the same top value the code picked the later one and the check only counts the first one.

Part 3

| Multiplier k | Average Utility | Win Rate |
|---|---|---|
| 0.50 | 0.1715 | 0.0035 |
| 0.75 | 1.1115 | 0.0340 |
| 1.00 | 2.4290 | 0.1745 |
| 1.25 | 0.7895 | 0.3750 |
| 1.50 | -1.8345 | 0.4890 |

4. 1.00, which is just bidding the true value. It got about 2.43.

5. Yes. The win rate went from about 17% at 1.00 up to about 38% at 1.25 and 49% at 1.50.

6. The extra wins are auctions where somebody else's bid was higher than Agent 0's real value. So it wins but it pays more than the item is worth to it and loses money. At 1.50 it had negative utility in about 30% of the auctions and the average dropped to about -1.83.

Part 4

s* = 0.80

Average utility at s* = 3.2898

Win rate at s* = 0.1870

7. If you bid your full value then you pay exactly what the item is worth to you, so you make 0 even when you win. At 1.00 Agent 0 won about 38% of the time and still averaged 0.

8. Because you basically never win. At 0.50 Agent 0 only won about 1% of the auctions so the average utility was only about 0.58.

9. It's how often you win against how much you keep when you win. A higher shade wins more but keeps less each time. A lower shade keeps more but wins less.

10. No. 0.80 was only the best because the other five bidders were bidding 80%. If they bid differently or if there were more or fewer bidders, the best shade would change. A dominant strategy would be the best no matter what the others do.

Part 5

| Bidders | FP Shade | FP Revenue | FP Winner Utility | SP Revenue | SP Winner Utility |
|---|---|---|---|---|---|
| 2 | 0.500 | 35.1385 | 35.1385 | 39.9315 | 30.3455 |
| 4 | 0.750 | 61.5825 | 20.5275 | 63.2695 | 18.8405 |
| 6 | 0.833 | 72.7037 | 14.5407 | 74.3845 | 12.8600 |
| 10 | 0.900 | 83.0173 | 9.2241 | 83.6495 | 8.5920 |

11. It goes up. First price went from about 35 with 2 bidders to about 83 with 10. Second price went from about 40 to about 84.

12. It goes down. First price winner utility went from about 35 to about 9 and second price went from about 30 to about 9.

13. With more bidders there's a better chance somebody else has a value close to yours, so if you shade a lot you get outbid more often. You have to bid closer to your real value to still win.

14. Second price was a little higher every time but the gap kept shrinking. They were about 4.8 apart with 2 bidders and only about 0.6 apart with 10, so they end up almost the same.

Part 6

Bidding rule: bid = min(0.85 * value, 80). Bid 85% of the value but never more than 80.

Average utility = 3.3728

Win rate = 0.2410

15. Yes, but only by a little. It got about 3.37 and the best constant shade (0.80) got about 3.29. The other bidders bid 80% and the highest value is 100, so nobody else can bid more than 80. Bidding above 80 is just paying extra. Capping at 80 saved money on the high values and the win rate stayed the same as plain 0.85.
