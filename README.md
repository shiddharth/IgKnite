# Veron1CA
<img src="readme_assets/asset1.webp"><br><br>
An open source Discord moderation bot with spontaneous modding capabilities and some extra powers like handling the beat with features of a music bot.

![GitHub](https://img.shields.io/github/license/shiddharth/Veron1CA?color=blue&style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/shiddharth/Veron1CA?color=blue&style=for-the-badge)
![GitHub watchers](https://img.shields.io/github/watchers/shiddharth/Veron1CA?color=blue&style=for-the-badge)

## Feature Highlights
Now this is where things get interesting...
<blockquote>
Veron1CA is the combination of a Discord moderation bot and a music bot. It comes packed with features like built-in swear filter, jailing and so on. Along with a lot of server management and modding capabilities, it can play music too! Useful features like shuffle, loop are also available with it. If you want to increase your experience with swear filter, Veron1CA also comes with an expandible database of unwanted words.
</blockquote>

<i>Learn more from [the official website here!](https://shiddharth.github.io/Veron1CA)</i>

## Setup
If you wanna host Veron1CA on your own computer or hosting service, then follow the steps mentioned below. You can always go a lil' bit nerdy and make your own path!
* Clone the repository.
```
git clone https://github.com/shiddharth/Veron1CA.git
```
* Create a `.env` file on the project directory to keep the tokens and command prefix in.
```
cd Veron1CA && touch .env
```
* Type the following in the `.env` file and save:
```
TOKEN=yourtokenhere
COMMAND_PREFIX=yourprefixhere
OWNER_ID=yourIDhere
```
* After setting up the bot secrets appropriately, open up your Terminal in the project directory. Make sure you have Python and Poetry installed for the upcoming step:
```
python -m poetry install
```
* This will installed all dependencies from the `poetry.lock` file. Now if you wanna host it on your project, type the command shown below:
```
python main.py
```

<i>Now you're ready to rock!</i>

#### and if you wanna go the cloud way...
As Veron1CA's code is optimized for [Replit.com](https://replit.com), it's recommended to create a new repository there and host the bot on it. You can, alternatively, hack the code for yourself and host it on other platforms like [DisCloud!](https://discloudbot.com/)

## Licence
<blockquote>
MIT License

Copyright (c) 2021 Anindya Shiddhartha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</blockquote>
