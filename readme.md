
## Game State Design
// A is self
### A state
- game score(4): {A, B, C, D}
- deal score(4): {A, B, C, D}
- exposed AH(4): {A, B, C, D}
- round state(4): {give B, give C, give D, play}
- first card in round(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
- A hand cards(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A} // -1 picked; 0 no card; 1 have card
- B hand cards(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A} // -1 picked; 0 unknown; 1 received card
- C hand cards(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A} // -1 picked; 0 unknown; 1 received card
- D hand cards(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A} // -1 picked; 0 unknown; 1 received card
### Game state
Total 16 state histories
- Init with received cards
- Passed cards (the same as up if no needs to pass)
- Exposed card (the same as up if no one expose A Heart)
- Played round 1
- Played round 2
- Played round ...
- Played round 13 (deal over)
