# Wiktionary Language-Specific UI Wrapper

**Live Demo:** [rutrut41.pythonanywhere.com](https://rutrut41.pythonanywhere.com/)  
*(The site has not been stress-tested; if it runs slowly, you can fork the project and host it locally with an IDE like PyCharm.)*

---

## Overview

This project is a **UI wrapper for Wiktionary** that allows you to select a specific language and view only the word results for that language. It streamlines the page layout, making the information more **readable and user-friendly**.  

Wiktionary is a powerful tool for linguists and language enthusiasts, especially for quick references to a word's **etymology**. However, the normal Wiktionary site shows results for **all languages** in which a word exists.  

For example, searching for the word [“Ya” on Wiktionary](https://en.wiktionary.org/wiki/ya) shows entries across multiple languages. This wrapper lets you focus on a single language at a time.

---

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


If you like this project, you can:

[**donate via PayPal**:](https://www.paypal.me/QKurmaskie)
Or
[**Buy Me a Coffee**](https://buymeacoffee.com/qkurmaskier) 
