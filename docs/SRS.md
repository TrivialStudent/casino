# Software Requirements Specification

## Purpose
The purpose of this project is to create a multi-game casino web application that’s easy for players to navigate through: either creating an account, or managing a virtual wallet (withdrawing/transferring/depositing virtual credits), or placing bets. Additionally, the platform would be storing user data, including their account and wallet information.

## Scope
- Persistent JSON data  
- Functioning balance system and virtual wallet (transaction history/view balance/deposit virtual credits/withdraw)  
- User account actions (registration/authentication/management)  
- Games/betting integration (place bets, settle results)

---

## Overall Description

### User Characteristics
**A new gambler**  
Needs to be introduced to gambling. Wants clear introduction to each game, to have vivid visualization.

**The casual gambler**  
Needs a quick and easy way to release stress. Only wants it to take a few clicks to get into a game.

**The professional gambler**  
Needs a system to track wins and losses and display statistics for each game. Wants persistent log in.  
Wants hardest challenges.

### Constraints
- The game must be able to contain multiple users  
- No real money (virtual credits only)  
- Users' data must be hidden and secure from others  
- The game is only going to be single-player  

---

## Non-functional Requirements
- **Persistence:** All user information should be stored in a JSON file  
- **Feedback:** The system should provide the statistics and status of the user’s bets  
- **Integrity:** The system does not provide any user data to external sources  
- **Usability:** The system should provide clear instructions for the user  

---

## User Stories / Requirements

### User Story 1: Account Creation and Simplicity
**As a gambler**, I want a game that explains the rules simply with low-stakes options so I can learn without losing a lot of money. I also want to be able to register, log in, and manage my profile so that I can authenticate and use the casino services securely.

**Acceptance Criteria:**
- Given the gambler looks for simplicity, each game should have a tutorial that walks through the mechanics. The rules and potential payouts of each game should be visible.  
- Given the gambler wants to learn without losing money, there should be a ‘practice’ mode which could be optionally used to get better at games that don’t involve virtual money.  
- Given the user needs secure authentication, when valid username, password, and age are provided, the system creates a user record with an ID and a balance of 500 credits. If the username already exists, return an error.  

---

### User Story 2: Variety of Games and Virtual Wallet
**As a gambler**, I want to be able to log in to my account and have access to a place where I can play a variety of games and manage my virtual finances.

**Acceptance Criteria:**
- Given the gambler seeks diversity, the game lobby prominently displays a wide range of games, indicating newly added or popular ones.  
- Given the gambler may have a created account, the system should allow logging in to continue with the saved balance and stats.  
- Given the gambler needs awareness of financial state, there should be a virtual wallet that shows balance and allows deposit/withdrawal of virtual credits.  

---

### User Story 3: Game Analytics
**As a gambler**, I want access to high-stakes tables and participate in exclusive games, so I can use my skills to compete with difficult players and maximize my winnings.

**Acceptance Criteria:**
- The game offers VIP games/tournament mode that are high-stakes for the best players.  
- Game analytics are available to track my win/loss ratio, stats, and betting history.  
- Given the gambler wants to maximize their winnings, the system should always be able to show updated statistics for the user to see their progress.  
