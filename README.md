<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/syanification/Gino">
    <img src="gino.png" width="300" height="300">
  </a>

  <h3 align="center">Gino</h3>

  <p align="center">
    The TDQL Powered Gin Playing AI
    <br />
    <a href="https://github.com/syanification/Gino"><strong>Explore the project »</strong></a>
    <br />
    
<div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Gino uses temporal difference Q learning in order to find optimal strategy for a simplified version of the popular card game Gin! This simplified version of the game of gin uses only cards 2-8 and 3 of the 4 suits. This change was necessary due to the limitations of TDQL as the state space grows exponentially with every additional card added to the deck. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

How to try for yourself:

### Prerequisites

* Python 3

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/syanification/Gino.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. The QTable is too large to store on github so you will need to train it yourself. To do this use the following line at the bottom of TDQL.py with a value that is suitable for your preferences. For reference I trained Gino for ~2.1 billion iterations. The rough time it takes on my machine for each magnitude of training is given in comments at the bottom of the file.
  ```
  t.train(YOUR_ITERATIONS)
  ```
2. Run TDQL.py
  ```
  py TDQL.py
  ```
3. If you want to test it against a random agent you can run arena.py
```
py arena.py
```



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Riley Roberts - syanification@gmail.com

Project Link: [https://github.com/syanification/Gino](https://github.com/syanification/Gino)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to thank the following resources, without them this project would not have been possible.

* [Gin Rummy Optimal Meld Finder](https://gist.github.com/yalue/2622575)
* [Best README Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>