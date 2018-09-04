
## Game State Design
// A is self
### A state
- global score: {A, B, C, D}
- round score(4): {A, B, C, D}
- round sates(4): {play, give B, give C, give D}
- hand cards(52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
- A played cards (52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
- B played cards (52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
- C played cards (52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
- D played cards (52): {club 2-A, diamond 2-A, heart 2-A, spade 2-A}
### Game state
state history = state * 14 
