# Components
## Website
- user can create accounts
  - creator or fan
- creator can create giveaways
- can specify prizes for giveaways and time for when link is valid
- can generate qr code for giveaway
- fans can scan qr code and enter in the giveaway in the contest time
- else it just shows a countdown
- creator can access a list of winners and just people who entered after the giveaway is over
## Sprinkle
### Hardware
- only fans in a certain distance can enter giveaway
  - can use creator phone or raspberry pi beacon
### CockroachDB + Google Cloud
- use cockroachDB as database hosted on Google Cloud
# Expected behaviour
- qr code + website
- creator can just put qr code on their booth
- if you scan qr code, goes to website which tells you about the giveaway
- at some time specified by creator a winner will be chosen
  - go to booth at the time and scan qr code
  - selects someone for a reward
