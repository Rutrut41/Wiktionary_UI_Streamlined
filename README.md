# Wiktionary Language-Specific UI Wrapper

**Live Demo:** [rutrut41.pythonanywhere.com](https://rutrut41.pythonanywhere.com/)  
*(The site has not been stress-tested; if it runs slowly, you can fork the project and host it locally with an IDE like PyCharm.)*

---

## Overview

This project is a **UI wrapper for Wiktionary** that allows you to select a specific language and view only the word results for that language. It streamlines the page layout, making the information more **readable and user-friendly**.  

This is a UI wrapper for Wiktionary.com that allows you to select the specific language that you are interested in seeing word results for, and returns only the information for that speicific language.  
It also (in my opinion) makes the resulting page look much more readable and understandable.  
Wiktionary is a very powerful tool for linguists and language enthusiasts alike, especially when getting a quick reference for a word's etymology.  
But on the normal Wiktionary site, when you look up a given word, you will get the results for ALL the languages in which that word exists.  
For example, if you want to look up the word ["Ya" on the normal Wiktionary site](https://en.wiktionary.org/wiki/ya), it shows the results for ya in **all** languages that that word exists in.
That's why I made this wrapper, in order to make a powerful website's information much more accessible and streamlined for users. And when I say users, that includes myself, as since I started making this app about a month ago in my free time, I have consistently been using it when I want to: 1) check the etymology of a word, 2) for reference while reading academic linguistic papers, and 3) when I am getting better at a language I'm learning. 

---

![Description](NEW_NEW_SCRGRAB_GOOD.gif)

## Features

- Select a **specific language** from a dropdown menu and see only that language’s entry.  
- Hyperlinks to:
  - Other words within the wrapper site  
  - Other languages within the wrapper (works ~80–90% of the time)  
  - External links (e.g., Wikipedia or third-party sites) open normally in your browser  
- Makes the results **more readable and streamlined**, ideal for:
  1. Checking word etymology  
  2. Academic linguistic research  
  3. Language learning reference  

---

## Known Issues / TODO

- When clicking a hyperlink that leads to a **different language**, the page updates correctly, but the dropdown in the search bar **resets to English**.  
  - Goal: Keep the dropdown set to the current page’s language.

---

## Usage

1. Open the live site: [rutrut41.pythonanywhere.com](https://rutrut41.pythonanywhere.com/)  
2. Type a word in the search bar.  
3. Select the desired language from the dropdown.  
4. View the cleaned-up entry for that language only.

> Tip: If a hyperlink leads outside Wiktionary, use your browser's back button or bookmark this wrapper for easy navigation back.

---

## Development Notes

- Built in Python (server-side logic not included here).  
- UI improvements and bug fixes are ongoing.  
- Feedback and contributions are welcome.



## Credits & Licensing

This project is a UI wrapper for [Wiktionary](https://www.wiktionary.org/), which is the source of all word definitions, etymologies, and other linguistic content displayed in this app.  

All Wiktionary content is licensed under **Creative Commons Attribution–ShareAlike (CC BY-SA 3.0 / 4.0)**.  

- **Attribution:** All content is provided by Wiktionary. You can access the original pages at [https://www.wiktionary.org/](https://www.wiktionary.org/).  
- **Share-Alike:** Any extracted or modified Wiktionary content must remain under **CC BY-SA**.  

## Ways to Support the Creator of this App
If you like this project, you can:

[**Donate Via PayPal**](https://www.paypal.me/QKurmaskie)  
**Or**  
[**Buy Me a Coffee**](https://buymeacoffee.com/qkurmaskier) 
