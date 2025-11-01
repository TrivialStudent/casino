[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]






<h1 align="center">All In Santos</h3>

  <p align="center">
    A sleek, modern online casino to satisfy all your gambling needs!
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#top-contributors">Top Contributors</a></li>
    <li><a href="#contribution-log">Contribution Log</a></li>
  </ol>
</details>



## About The Project

<img width="1676" height="891" alt="image" src="https://github.com/user-attachments/assets/5c3d8015-6d73-4370-a7a2-0c72add95517" />



**All In Santos** is an online casino web application built with Flask that brings classic casino games to the browser with a focus on simplicity, security, and engaging gameplay.

Players can create accounts, manage virtual wallets, and bet games, all within a persistent, data-driven environment powered by Python.




<p align="right">(<a href="#readme-top">back to top</a>)</p>




### Built With

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Core Technologies:**
- **Python 3.7+** - Backend logic and game algorithms
- **Flask** - Web framework and routing
- **bcrypt** - Password encryption and security
- **Jinja2** - Dynamic HTML templating
- **HTML5/CSS3** - Frontend structure and styling

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

We know you are eager to dive in, here is how to get set up!


## Prerequisites

Make sure you have Python installed on your system:
* Python 3.7 or higher

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/TrivialStudent/casino
   ```
2. Navigate to the project directory
   ```sh
   cd repo_name
   ```
3. Create a virtual environment
   ```sh
   python -m venv .venv
   ```
4. Activate the virtual environment
   - On Windows:
   ```sh
     .venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```sh
     source .venv/bin/activate
   ```
5. Install required Python packages
   ```sh
   pip install -r requirements.txt
   ```
6. Navigate inside src and run the application
   ```sh
   cd src
   python main.py
   ```
7. Open your browser and click on the Flask app link displayed in the terminal (typically `http://127.0.0.1:5000/`)



<!-- ROADMAP -->
## Roadmap

- [X] Create Blackjack Backend
- [X] Flask app backend
- [X] Create main web app pages (log in, sign up, menu, stats, game window)
- [ ] Add more games
    - [ ] Roullette
    - [ ] Slot machines
- [ ] Add Leaderboard

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Top contributors:

<a href="https://github.com/TrivialStudent/casino/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TrivialStudent/casino" alt="contrib.rocks image" />
</a>


### Sprint 1 Contribution Log

| Date | Alan | Loli | Angelina | Lorcan                                                                                                                                                     |
|:----:|:-----|:-----|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Role** | **Chief Frontend Architect & Cross-Platform Synergy Coordinator** | **User Interface Optimization Specialist & Debug Infrastructure Lead** | **Visual Systems Engineer & Template Architecture Consultant** | **Project Lead & Chief Architect of Backend Infrastructure, Security Paradigms, Statistical Visualization Frameworks & Repository Documentation Strategy** |
| **10/13** | SRS document | SRS and documentation | Use Case Diagram | Blackjack implementation, secure login with hashed passwords, Flask webapp setup, Class diagram                                                            |
| **10/14** | Fixed filepath issues for Mac, improved UI significantly | Debugged Sign in and Log in base UI | Improved login UI | Stats page (charts, balance, win ratio)                                                                                                                    |
| **10/15** | Menu & profile pages, deposit page | - | - | Added gifs, integrated stats page                                                                                                                          |
| **10/16** | Navbar & responsive grid | Enhanced login & signup pages with styles | UI template improvements | Created README.md, improved sign-in/login UI, added custom flash warnings                                                                                  |
| **Summary** | UI/UX, Pages, Cross-platform fixes | Frontend styling, Debugging | UI templates, Diagrams | Backend logic, Security, Stats, Documentation                                                                                                              |

### Sprint 2 Contribution Log 

| Date | Alan | Loli                                            | Angelina | Lorcan |
|:----:|:-----|:------------------------------------------------|:---------|:-------|
| **Role** | **Frontend Developer & UI/UX Designer** | **Documentation & Requirements Specialist**                                           | **Backend Integration & Data Specialist** | **Project Lead, Backend Architecture & Game Development** |
| **10/27** | - | SRS updates and refinements                     | - | Pygame window & obstacle rendering, preferred name feature & player class refactor |
| **10/28** | - | -                                               | Net value system, balance to homepage | Plinko ball physics, flash message cleanup, slot→plinko gif, PR merges |
| **10/29** | - | -                                               | - | Preferred name glitch fix, branch merging |
| **10/30** | - | SRS documentation                               | - | Plinko game finalized, Flask integration in progress |
| **10/31** | Auto-login after signup | -                                               | - | Pygame window size fixes |
| **11/1** | Blackjack UI/UX overhaul | SRS revisions                                   | - | Dynamic balance updates (JS), JSON cache fix, Plinko integration, prevent concurrent instances, README updates, merge coordination |
| **Summary** | Blackjack redesign, UX improvements | -                                               | Net value tracking, homepage balance | Full Plinko game (Pygame), JSON fixes, preferred name system, documentation |
### Important Notes
### Plinko
* After pressing play, a window will open in the background. You may have to move other tabs around to see it!
* After a Plinko round, balance will not be instantly updated. Please allow for a few seconds and navigate to a new page to refresh the JSON cache.

### Navigation
* To navigate home from deposit, stats, or blackjack pages, either:
  - Click "All In Santos" in the top left, or
  - Click the dropdown menu in the top right, then click the house icon


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-url]: https://github.com/TrivialStudent/casino/graphs/contributors
[forks-url]: https://github.com/TrivialStudent/casino/network/members
[stars-url]: https://github.com/TrivialStudent/casino/stargazers
[issues-url]: https://github.com/TrivialStudent/casino/issues
[license-url]: https://github.com/TrivialStudent/casino/blob/master/LICENSE.txt

[contributors-shield]: https://img.shields.io/github/contributors/TrivialStudent/casino.svg?style=for-the-badge
[forks-shield]: https://img.shields.io/github/forks/TrivialStudent/casino.svg?style=for-the-badge
[stars-shield]: https://img.shields.io/github/stars/TrivialStudent/casino.svg?style=for-the-badge
[issues-shield]: https://img.shields.io/github/issues/TrivialStudent/casino.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/TrivialStudent/casino.svg?style=for-the-badge
[product-screenshot]: images/screenshot.png
